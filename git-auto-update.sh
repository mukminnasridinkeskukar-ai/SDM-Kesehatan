#!/bin/bash
# ============================================
# AUTO-UPDATE GALERI FOTO + GIT COMMIT/PUSH
# ============================================
# Script ini:
# 1. Fetch data dari Cloudinary
# 2. Generate HTML baru
# 3. Commit & push ke Git repository

# Configuration
REPO_DIR="/home/z/my-project"
HTML_FILE="download/galeri-foto-standalone.html"
LOG_FILE="scripts/git-update.log"
# Auto-detect Python (prioritas: venv > system python3 > python)
if [ -x "$REPO_DIR/venv/bin/python" ]; then
    VENV_PYTHON="$REPO_DIR/venv/bin/python"
elif command -v python3 &> /dev/null; then
    VENV_PYTHON="python3"
elif command -v python &> /dev/null; then
    VENV_PYTHON="python"
else
    echo "[$TIMESTAMP] ❌ ERROR: Python not found" >> "$REPO_DIR/$LOG_FILE"
    exit 1
fi
PYTHON_SCRIPT="$REPO_DIR/scripts/bento-masonry-gallery-v4.py"

# Get timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
DATE=$(date "+%Y-%m-%d")

echo "========================================" >> "$REPO_DIR/$LOG_FILE"
echo "[$TIMESTAMP] Starting Git auto-update..." >> "$REPO_DIR/$LOG_FILE"

# Change to repository directory
cd "$REPO_DIR" || {
    echo "[$TIMESTAMP] ❌ ERROR: Cannot access $REPO_DIR" >> "$REPO_DIR/$LOG_FILE"
    exit 1
}

# Step 1: Run Python script to fetch from Cloudinary and generate HTML
echo "[$TIMESTAMP] Step 1: Fetching from Cloudinary..." >> "$REPO_DIR/$LOG_FILE"
$VENV_PYTHON "$PYTHON_SCRIPT" >> "$REPO_DIR/$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$TIMESTAMP] ❌ ERROR: Failed to generate HTML" >> "$REPO_DIR/$LOG_FILE"
    exit 1
fi

# Step 2: Check if there are changes to HTML file
if ! git diff --quiet "$HTML_FILE"; then
    echo "[$TIMESTAMP] Step 2: Changes detected in HTML file" >> "$REPO_DIR/$LOG_FILE"
    
    # Count photos for commit message
    PHOTO_COUNT=$(grep -o '"publicId"' "$HTML_FILE" | wc -l)
    ACTIVITY_COUNT=$(grep -o '"judul":' "$HTML_FILE" | wc -l)
    
    # Step 3: Add to git staging
    git add "$HTML_FILE"
    
    # Step 4: Commit with descriptive message
    git commit -m "🎨 Auto-update Bento+Masonry Gallery v4.0 ($DATE)

📊 Statistik:
• $ACTIVITY_COUNT kegiatan
• $PHOTO_COUNT foto
🔄 Auto-update by cron job
✨ Modern Clean Design"

    # Step 5: Push to remote
    # Auto-detect branch (main or master)
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    git push origin "$CURRENT_BRANCH"
    
    if [ $? -eq 0 ]; then
        echo "[$TIMESTAMP] ✅ SUCCESS: Committed and pushed to Git!" >> "$REPO_DIR/$LOG_FILE"
        echo "[$TIMESTAMP] 📊 Changes: $ACTIVITY_COUNT activities, $PHOTO_COUNT photos" >> "$REPO_DIR/$LOG_FILE"
    else
        echo "[$TIMESTAMP] ⚠️ WARNING: Committed but push failed (check remote)" >> "$REPO_DIR/$LOG_FILE"
    fi
    
else
    echo "[$TIMESTAMP] ℹ️ No changes detected, skipping commit" >> "$REPO_DIR/$LOG_FILE"
fi

echo "" >> "$REPO_DIR/$LOG_FILE"
exit 0

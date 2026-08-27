#!/bin/bash
# ============================================
# AUTO-UPDATE GALERI FOTO + GIT COMMIT/PUSH
# ============================================
# Script ini:
# 1. Fetch data dari Cloudinary
# 2. Generate HTML baru
# 3. Commit & push ke Git repository

# Configuration
REPO_DIR="/home/z/my-project"  # ← Ganti dengan path repository Anda
HTML_FILE="download/galeri-foto-standalone.html"
LOG_FILE="scripts/git-update.log"
VENV_PYTHON="/home/z/my-project/venv/bin/python"
PYTHON_SCRIPT="/home/z/my-project/scripts/bento-masonry-gallery-v4.py"  # ← Modern Bento + Masonry v4.0

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
    git push origin main  # ← Ganti 'main' dengan branch Anda (main/master)
    
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

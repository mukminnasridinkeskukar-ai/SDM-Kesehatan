#!/bin/bash
# ============================================
# SETUP CRON JOB - AUTO UPDATE SETIAP 6 JAM
# ============================================
# Jalankan script ini di SERVER Anda untuk setup otomatis

echo "🔧 Setting up cron job untuk auto-update galeri foto..."
echo ""

# Path configuration
SCRIPT_PATH="/home/z/my-project/scripts/git-auto-update.sh"
CRON_ENTRY="0 */6 * * * $SCRIPT_PATH >> /home/z/my-project/scripts/cron.log 2>&1"

# Check if cron already exists
EXISTING_CRON=$(crontab -l 2>/dev/null | grep "git-auto-update" || true)

if [ -n "$EXISTING_CRON" ]; then
    echo "⚠️  Cron job sudah ada. Mengupdate..."
    # Remove existing entry and add new one
    (crontab -l 2>/dev/null | grep -v "git-auto-update"; echo "$CRON_ENTRY") | crontab -
else
    echo "📝 Menambahkan cron job baru..."
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
fi

echo ""
echo "✅ Cron job berhasil disetup!"
echo ""
echo "📋 Detail Cron Job:"
echo "   ⏰  Jadwal: Setiap 6 jam (00:00, 06:00, 12:00, 18:00)"
echo "   📂 Script: $SCRIPT_PATH"
echo "   📝 Log: /home/z/my-project/scripts/cron.log"
echo ""
echo "📖 Perintah berguna:"
echo "   Lihat cron aktif:     crontab -l"
echo "   Lihat log terakhir:   tail -50 /home/z/my-project/scripts/cron.log"
echo "   Hapus cron job:       crontab -e (hapus baris git-auto-update)"
echo ""
echo "🧪 Test manual sekarang? Jalankan:"
echo "   bash $SCRIPT_PATH"

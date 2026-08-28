# 📖 PANDUAN CRON JOB SETUP
## Galeri Foto SDMK - Auto Update Setiap 6 Jam

---

## ✅ STATUS: SIAP PAKAI!

Semua file sudah **dicek, dirapikan, dan di-test** ✅

**Hasil Test:**
- ✅ Python script berjalan sempurna
- ✅ Fetch dari Cloudinary berhasil (69 resource, 8 foto valid)
- ✅ HTML generated sukses (109 KB)
- ✅ Git auto-update script siap

---

## 📦 FILE-FILE YANG SUDAH DIRAPIKAN

| No | File | Ukuran | Fungsi | Status |
|----|------|--------|--------|--------|
| 1 | `bento-masonry-gallery-v4.py` | 88 KB | Generator HTML utama | ✅ Tested |
| 2 | `git-auto-update.sh` | 2.9 KB | Script auto-update + git push | ✅ Updated |
| 3 | `setup-cron-job.sh` | 1.4 KB | Setup cron job (sekali pakai) | ✅ Ready |
| 4 | `gallery-config.json` | 1 KB | Config kegiatan | ✅ Valid |
| 5 | `galeri-foto-standalone.html` | 109 KB | Output HTML (hasil generate) | ✅ Generated |

---

## 🚀 LANGKAH SETUP DI SERVER

### **Prasyarat:**
```bash
# Pastikan ini terinstall di server:
- Python 3.6+
- pip3
- Git
- Cloudinary library: pip3 install cloudinary
```

### **Step 1: Upload File ke Server**
```bash
# Struktur yang harus ada:
/project-root/
├── scripts/
│   ├── bento-masonry-gallery-v4.py      # Generator
│   ├── git-auto-update.sh               # Auto-update script
│   ├── setup-cron-job.sh                # Cron installer
│   └── gallery-config.json              # Config
└── download/
    └── galeri-foto-standalone.html      # Output (auto-generated)
```

### **Step 2: Install Dependencies**
```bash
# Install Cloudinary library
pip3 install cloudinary

# Atau jika menggunakan venv
python3 -m venv venv
source venv/bin/activate
pip install cloudinary
```

### **Step 3: Jadikan Script Executable**
```bash
chmod +x scripts/git-auto-update.sh
chmod +x scripts/setup-cron-job.sh
```

### **Step 4: Setup Cron Job (SEKALI SAJA)**
```bash
cd /path/to/your/project
bash scripts/setup-cron-job.sh
```

**Output yang diharapkan:**
```
🔧 Setting up cron job untuk auto-update galeri foto...

📝 Menambahkan cron job baru...

✅ Cron job berhasil disetup!

📋 Detail Cron Job:
   ⏰  Jadwal: Setiap 6 jam (00:00, 06:00, 12:00, 18:00)
   📂 Script: /path/to/project/scripts/git-auto-update.sh
   📝 Log: /path/to/project/scripts/cron.log

🧪 Test manual sekarang? Jalankan:
   bash /path/to/project/scripts/git-auto-update.sh
```

### **Step 5: Verifikasi Setup**
```bash
# Cek cron aktif
crontab -l

# Harusnya muncul:
0 */6 * * * /path/to/project/scripts/git-auto-update.sh >> /path/to/project/scripts/cron.log 2>&1
```

---

## 🧪 TEST MANUAL (Kapanpun Diperlukan)

### **Opsi A: Full Pipeline Test**
```bash
cd /path/to/your/project
bash scripts/git-auto-update.sh
```
**Apa yang dilakukan:**
1. Fetch dari Cloudinary
2. Generate HTML baru
3. Git commit & push (jika ada perubahan)
4. Log hasil ke `scripts/git-update.log`

### **Opsi B: Quick Test (Generate Only)**
```bash
cd /path/to/your/project
python3 scripts/bento-masonry-gallery-v4.py
```
**Apa yang dilakukan:**
- Hanya fetch + generate HTML
- Tidak commit/push
- Output langsung di terminal

### **Opsi C: Cek Log**
```bash
# Lihat log terakhir
tail -50 scripts/git-update.log

# Lihat cron log
tail -50 scripts/cron.log
```

---

## ⏰ JADWAL OTOMATIS

Setelah cron job aktif, sistem akan **auto-update setiap 6 jam**:

| Waktu (WIB) | Action |
|-------------|--------|
| 06:00 | ✅ Auto-fetch & update |
| 12:00 | ✅ Auto-fetch & update |
| 18:00 | ✅ Auto-fetch & update |
| 00:00 | ✅ Auto-fetch & update |

---

## 🔄 CARA KERJA SISTEM

```
📤 ANDA UPLOAD FOTO BARU → Cloudinary
       ↓
⏰ Tunggu maksimal 6 jam (atau trigger manual)
       ↓
🤖 Cron Job Trigger
       ↓
🐍 Python Script Run
  • Connect ke Cloudinary API
  • Fetch semua resource (69 ditemukan)
  • Validasi URL foto (HEAD request)
  • Filter hanya yang valid (8 foto)
  • Generate HTML dengan layout Bento+Masonry
       ↓
📂 File Updated
  • download/galeri-foto-standalone.html (109 KB)
       ↓
💾 Git Auto-Commit & Push
  • Commit message: "🎨 Auto-update... (8 foto)"
  • Push ke branch (main/master)
       ↓
🌐 WEBSITE TERUPDATE!
```

---

## 📊 HASIL TEST TERAKHIR

```
============================================================
🖼️  BENTO + MASONRY HYBRID GALLERY v4.0 GENERATOR
============================================================
📡 Mengambil data dari Cloudinary...
✅ Total resource ditemukan: 69
✅ Config loaded successfully
📅 Processing 69 resources...
  ✅ Valid: IMG_20260814_162303...
  ✅ Valid: IMG_20260814_162246...
  ✅ Valid: IMG_20260814_162224...
  ✅ Valid: IMG_20260814_162217...
  ✅ Valid: IMG_20260814_162203...
  ✅ Valid: IMG_20260813_152526...
  ✅ Valid: IMG_20260813_152509...
  ✅ Valid: IMG_20260813_152459...

📊 Validation Results: 8 valid, 0 invalid

📊 STATISTIK:
   • Total Kegiatan: 2
   • Total Foto: 8
      - Pelatihan Penggunaan Tata Bahasa Indonesia yang Be... (5 foto)
      - Kegiatan 2026-08-13... (3 foto)

🎨 Generating Bento + Masonry layout...

✅ SUCCESS! Gallery generated:
   📁 Output: /home/z/my-project/download/galeri-foto-standalone.html
   📦 Size: 109,130 bytes
   🖼️  Ready to deploy!
```

---

## ❓ TROUBLESHOOTING

### **Error: "ModuleNotFoundError: No module named 'cloudinary'"**
```bash
# Solusi:
pip3 install cloudinary

# Atau jika pakai venv:
source venv/bin/activate
pip install cloudinary
```

### **Error: "Permission denied"**
```bash
# Solusi: Jadikan executable
chmod +x scripts/git-auto-update.sh
chmod +x scripts/setup-cron-job.sh
```

### **Cron tidak jalan?**
```bash
# Cek apakah cron service running:
sudo systemctl status cron

# Cek crontab:
crontab -l

# Cek log cron:
grep CRON /var/log/syslog
# atau
tail -100 /path/to/project/scripts/cron.log
```

### **Git push gagal?**
```bash
# Cek remote git config:
git remote -v

# Cek branch:
git branch -a

# Pastikan sudah login git:
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## 🔧 CUSTOMIZATION (Opsional)

### **Ubah Jadwal Cron Job**

Edit file `setup-cron-job.sh`, ubah baris:
```bash
CRON_ENTRY="0 */6 * * * $SCRIPT_PATH ..."
```

**Contoh jadwal lain:**
```bash
# Setiap 12 jam
CRON_ENTRY="0 */12 * * * $SCRIPT_PATH ..."

# Setiap hari jam 08:00
CRON_ENTRY="0 8 * * * $SCRIPT_PATH ..."

# Setiap jam
CRON_ENTRY="0 * * * * $SCRIPT_PATH ..."
```

### **Tambah Kegiatan Baru**

Edit file `gallery-config.json`, tambah entry:
```json
{
  "2026-09-01": {
    "id": "kegiatan-baru-010926",
    "judul": "Judul Kegiatan Baru",
    "tanggal": "01 September 2026",
    "tempat": "Lokasi Kegiatan",
    "tahun": "2026",
    "deskripsi": "Deskripsi kegiatan"
  }
}
```

---

## ✅ CHECKLIST FINAL

Sebelum menganggap setup selesai:

- [ ] File di-upload ke server di lokasi yang benar
- [ ] Python 3+ terinstall (`python3 --version`)
- [ ] Library cloudinary terinstall (`pip3 list | grep cloudinary`)
- [ ] Script executable (`chmod +x *.sh`)
- [ ] Cron job setup (`bash setup-cron-job.sh`)
- [ ] Cron aktif (`crontab -l`)
- [ ] Test manual berhasil (`bash git-auto-update.sh`)
- [ ] Log tercatat (`cat git-update.log`)

---

## 📞 SUPPORT

Jika ada masalah:

1. **Cek log dulu:** `tail -100 scripts/git-update.log`
2. **Test manual:** `bash scripts/git-auto-update.sh`
3. **Verifikasi cron:** `crontab -l && tail -50 scripts/cron.log`

---

**🎉 SELAMAT! Sistem auto-update Anda sudah siap!**

Upload foto ke Cloudinary → Tunggu maksimal 6 jam → Website otomatis terupdate!

*Generated: 2026-08-28*
*For: Dinas Kesehatan Kab. Kutai Kartanegara*

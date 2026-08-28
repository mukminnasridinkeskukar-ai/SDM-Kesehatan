# 📖 PANDUAN LENGKAP - Galeri Foto SDMK GitHub

## 📦 ISI PACKAGE (5 File)

```
galeri-github-final/
│
├── .github/
│   └── workflows/
│       └── auto-update-gallery.yml    ← File 1: Auto-update setiap 6 jam
│
├── scripts/
│   ├── bento-masonry-gallery-v5.py    ← File 2: Generator HTML (v5 terbaru)
│   ├── gallery-config.json            ← File 3: Config kegiatan
│   └── upload-foto-cloudinary.py      ← File 4: Upload foto ke Cloudinary
│
├── download/
│   └── galeri-foto-standalone.html    ← File 5: Output gallery (auto-generated)
│
└── PANDUAN-GITHUB-LENGKAP.md          ← File ini (panduan)
```

---

## ✅ JUMLAH FILE YANG HARUS DI REPO GITHUB: **5 FILE**

| No | File Path di Repo | Fungsi | Wajib? |
|----|-------------------|--------|--------|
| 1 | `.github/workflows/auto-update-gallery.yml` | Auto-update otomatis via GitHub Actions | ✅ WAJIB |
| 2 | `scripts/bento-masonry-gallery-v5.py` | Generator HTML utama (v5) | ✅ WAJIB |
| 3 | `scripts/gallery-config.json` | Config judul/tanggal kegiatan | ⚠️ Recommended |
| 4 | `scripts/upload-foto-cloudinary.py` | Upload foto ke Cloudinary | ⚠️ Opsional (untuk local use) |
| 5 | `download/galeri-foto-standalone.html` | Hasil output gallery | ✅ WAJIB |

---

## 🚀 LANGKAH SETUP (10 Menit Selesai!)

### **Step 1: Buat Repository GitHub** (Kalau belum ada)

1. Buka [github.com/new](https://github.com/new)
2. Nama: `galeri-foto-sdmk` (atau nama lain)
3. Pilih **Private** atau **Public**
4. **JANGGAN centang** "Add a README file"
5. Klik **Create repository**

### **Step 2: Upload 5 File ke Repository**

#### Opsi A: Drag & Drop (Paling Mudah) ⭐

1. Di halaman repository, klik **"uploading an existing file"**
2. **Drag & drop SELURUH folder** `galeri-github-final`
3. Pastikan struktur folder tetap:
   ```
   .github/workflows/auto-update-gallery.yml
   scripts/bento-masonry-gallery-v5.py
   scripts/gallery-config.json
   scripts/upload-foto-cloudinary.py
   download/galeri-foto-standalone.html
   ```
4. Klik **"Commit changes"**

#### Opsi B: Via Git Command Line**

```bash
# Clone repo Anda
git clone https://github.com/USERNAME/galeri-foto-sdmk.git
cd galeri-foto-sdmk

# Copy semua file dari package
cp -r path/to/galeri-github-final/* .

# Commit & push
git add .
git commit -m "🎉 Setup Galeri Foto SDMK with auto-update"
git push origin main
```

### **Step 3: Setup Secrets (Wajib!)** 🔑

1. Di repository, klik **Settings** (pojok kanan atas)
2. Klik **Secrets and variables** → **Actions**
3. Klik **"New repository secret"**
4. Tambahkan **3 secret ini**:

| Name | Value |
|------|-------|
| `CLOUDINARY_CLOUD_NAME` | `cla7jrww` |
| `CLOUDINARY_API_KEY` | `488796372967593` |
| `CLOUDINARY_API_SECRET` | `MvIaCN2zMacCWhJ2f2gJnFev0xw` |

5. Ulangi untuk ketiga secret (total 3x)

### **Step 4: Test Manual (Verifikasi)** ✔️

1. Klik tab **Actions** di repository
2. Klik workflow **"Auto-Update Galeri Foto SDMK"**
3. Klik **"Run workflow"** → **"Run workflow"**
4. Tunggu 1-2 menit...

**Hasil sukses:**
- ✅ Workflow hijau (green checkmark)
- ✅ File `download/galeri-foto-standalone.html` terupdate
- ✅ Ada commit baru "Auto-update Galeri Foto"

---

## 📤 CARA UPLOAD FOTO BARU

### **Opsi A: Pakai Upload Script (Recommended)**

```bash
# Di komputer lokal Anda:
python3 scripts/upload-foto-cloudinary.py foto-baru.jpg

# Atau banyak foto sekaligus:
python3 scripts/upload-foto-cloudinary.py *.jpg
```

**Lalu trigger GitHub Actions** untuk update otomatis!

### **Opsi B: Upload Langsung ke Cloudinary Console**

1. Login [cloudinary.com](https://cloudinary.com)
2. Upload foto dengan preset **`galeri_kegiatan`**
3. Tunggu beberapa menit
4. Trigger GitHub Actions manual

---

## ⏰ SISTEM OTOMATIS SETELAH SETUP

```
📤 ANDA UPLOAD FOTO → Cloudinary
      ↓
⏰ Setiap 6 Jam (08:00, 14:00, 20:00, 02:00 WIB)
      ↓
🤖 GitHub Actions Jalan OTOMATIS
      ↓
🐍 Script v5 Fetch + Generate HTML
      ↓
💾 Auto Commit & Push
      ↓
🌐 WEBSITE TERUPDATE!
```

### Trigger Manual Kapanpun:

1. **Actions** tab → **"Auto-Update Galeri Foto SDMK"**
2. **"Run workflow"** → **"Run workflow"**
3. **1-2 menit langsung update!**

---

## 🌐 DEPLOY KE GITHUB Pages (Opsional)

Agar galeri bisa diakses online gratis:

1. **Settings** → **Pages** (sidebar kiri bawah)
2. Source: **Deploy from a branch**
3. Branch: **main** / root
4. Click **Save**
5. Tunggu 2-3 menit
6. Website live: `https://USERNAME.github.io/NAMA-REPO/`

---

## ❓ TROUBLESHOOTING

### **Workflow tidak muncul di Actions?**
✅ Pastikan folder `.github/workflows/` dan file `.yml` ada

### **Error "Cloudinary API Error"?**
✅ Cek Secrets (Settings → Secrets) - pastikan nilai benar

### **Foto tidak bertambah?**
✅ Upload foto dulu ke Cloudinary, lalu trigger Actions manual

### **File HTML tidak berubah?**
✅ Cek apakah ada perubahan di Cloudinary, trigger ulang Actions

---

## ✅ CHECKLIST FINAL

Sebelum menganggap setup selesai:

- [ ] Repository GitHub dibuat
- [ ] **5 file** di-upload ke repo
- [ ] **3 Secrets** ditambah (`CLOUDINARY_*`)
- [ ] Test manual berhasil (green checkmark)
- [ ] (Opsional) GitHub Pages diaktifkan

---

## 📞 SUPPORT

**File yang dibutuhkan:**
- Generator: `bento-masonry-gallery-v5.py`
- Upload: `upload-foto-cloudinary.py`
- Config: `gallery-config.json`

**Commands berguna:**
```bash
# Generate HTML manual
python3 scripts/bento-masonry-gallery-v5.py

# Upload foto
python3 scripts/upload-foto-cloudinary.py foto.jpg

# Cek log
cat scripts/git-update.log
```

---

**🎉 SELAMAT! Galeri Foto SDMK siap online!**

Upload foto → Trigger Actions → Website auto-update!

*Dibuat untuk Dinas Kesehatan Kab. Kutai Kartanegara*
*Generated: 2026-08-28*
*Version: Final v1.0*

# 📖 PANDUAN SETUP GITHUB - Galeri Foto SDMK

## 📦 ISI PACKAGE (4 File)

```
galeri-github-package/
├── .github/
│   └── workflows/
│       └── auto-update-gallery.yml    ← File 1: GitHub Actions
├── scripts/
│   ├── bento-masonry-gallery-v5.py    ← File 2: Generator HTML
│   └── gallery-config.json            ← File 3: Config Kegiatan
└── download/
    └── galeri-foto-standalone.html    ← File 4: Output Gallery
```

---

## 🚀 LANGKAH SETUP (5 Menit Selesai!)

### **Step 1: Buat Repository GitHub**

1. Buka [github.com/new](https://github.com/new)
2. Nama repository: `galeri-foto-sdmk` (atau nama lain)
3. Pilih **Private** atau **Public**
4. **JANGGAN centang** "Add a README file"
5. Klik **Create repository**

### **Step 2: Upload File ke Repository**

#### Opsi A: Drag & Drop (Paling Mudah)

1. Di halaman repository baru, klik **"uploading an existing file"**
2. Drag & drop FOLDER `galeri-github-package` ini
3. Atau upload file per file:
   - `.github/workflows/auto-update-gallery.yml`
   - `scripts/bento-masonry-gallery-v5.py`
   - `scripts/gallery-config.json`
   - `download/galeri-foto-standalone.html`
4. Klik **"Commit changes"**

#### Opsi B: Via Git Command Line**

```bash
# Clone repository Anda
git clone https://github.com/USERNAME/galeri-foto-sdmk.git
cd galeri-foto-sdmk

# Copy file-file dari package
cp -r path/to/galeri-github-package/* .

# Commit & push
git add .
git commit -m "🎉 Initial setup: Galeri Foto SDMK with auto-update"
git push origin main
```

### **Step 3: Setup Secrets (Wajib!)**

1. Di repository, klik **Settings** (pojok kanan atas)
2. Klik **Secrets and variables** → **Actions**
3. Klik **"New repository secret"
4. Tambahkan **3 secret berikut**:

| Secret Name | Value |
|-------------|-------|
| `CLOUDINARY_CLOUD_NAME` | `cla7jrww` |
| `CLOUDINARY_API_KEY` | `488796372967593` |
| `CLOUDINARY_API_SECRET` | `MvIaCN2zMacCWhJ2f2gJnFev0xw` |

5. Ulangi untuk ketiga secret di atas

### **Step 4: Test Manual (Verifikasi)**

1. Klik tab **Actions** di repository
2. Klik workflow **"Auto-Update Galeri Foto SDMK"**
3. Klik tombol **"Run workflow"** → **"Run workflow"**
4. Tunggu 1-2 menit...

**Hasil yang diharapkan:**
- ✅ Workflow berhasil (green checkmark)
- ✅ File `download/galeri-foto-standalone.html` ter-update
- ✅ Ada commit baru dengan pesan "Auto-update Galeri Foto"

---

## ⏰ SETELAH SETUP... SISTEM OTOMATIS!

```
📤 ANDA UPLOAD FOTO BARU → Cloudinary
      ↓
⏰ Setiap 6 Jam (08:00, 14:00, 20:00, 02:00 WIB)
      ↓
🤖 GitHub Actions Jalan OTOMATIS
      ↓
🐍 Script Fetch + Generate HTML
      ↓
💾 Auto Commit & Push
      ↓
🌐 WEBSITE TERUPDATE!
```

---

## 🔄 TRIGGER MANUAL (Kapanpun Diperlukan)

Butuh update SEKARANG?

1. **Actions** tab → **"Auto-Update Galeri Foto SDMK"**
2. **"Run workflow"** → **"Run workflow"**
3. **1-2 menit langsung update!**

---

## 📊 MONITORING

| Cek Apa? | Dimana? |
|----------|---------|
| Status terakhir | Tab **Actions** → Lihat workflow runs |
| Riwayat commit | Tab **Commits** |
| File output | Tab **Code** → `download/galeri-foto-standalone.html` |

---

## 🌐 DEPLOY KE GITHUB Pages (Opsional)

Agar galeri bisa diakses online:

1. **Settings** → **Pages** (sidebar kiri bawah)
2. Source: **Deploy from a branch**
3. Branch: **main** / root
4. Save
5. Tunggu 2-3 menit
6. Website live di: `https://USERNAME.github.io/galeri-foto-sdmk/`

---

## ❓ TROUBLESHOOTING

### **Workflow tidak muncul di Actions?**
- Pastikan folder `.github/workflows/` benar
- Pastikan file `.yml` ada di dalamnya

### **Error "Cloudinary API Error"?**
- Cek Secrets (Settings → Secrets)
- Pastikan nilai CLOUDINARY_API_SECRET benar

### **File HTML tidak berubah?**
- Upload foto baru ke Cloudinary dulu
- Trigger manual dari Actions tab

---

## ✅ CHECKLIST FINAL

Sebelum menganggap selesai:

- [ ] Repository GitHub dibuat
- [ ] 4 file di-upload (`.yml`, `v5.py`, `config.json`, `html`)
- [ ] 3 Secrets ditambah (`CLOUDINARY_*`)
- [ ] Test manual berhasil (green checkmark)
- [ ] (Opsional) GitHub Pages diaktifkan

---

**🎉 SELAMAT! Sistem auto-update siap!**

Upload foto ke Cloudinary → Tunggu maksimal 6 jam → Website otomatis terupdate!

*Dibuat untuk Dinas Kesehatan Kab. Kutai Kartanegara*
*Generated: 2026-08-28*

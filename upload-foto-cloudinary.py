#!/usr/bin/env python3
"""
===========================================
UPLOAD FOTO KE CLOUDINARY - PAKAI PRESET
===========================================

Gunakan script ini untuk upload foto ke Cloudinary
dengan preset 'galeri_kegiatan' yang sudah dibuat

Cara pakai:
    python3 upload-foto-cloudinary.py <path/ke/foto.jpg>
    
Atau upload banyak foto:
    python3 upload-foto-cloudinary.py *.jpg
    
Author: Auto-generated for Galeri Foto SDMK
"""

import cloudinary
from cloudinary.uploader import upload
import sys
import os
from pathlib import Path

# ============================================
# KONFIGURASI
# ============================================
CLOUD_CONFIG = {
    "cloud_name": "cla7jrww",
    "api_key": "488796372967593",
    "api_secret": "MvIaCN2zMacCWhJ2f2gJnFev0xw"
}

# Upload preset yang sudah dibuat di Console
UPLOAD_PRESET = "galeri_kegiatan"  # ← Sesuaikan dengan nama preset Anda

def setup_cloudinary():
    """Initialize Cloudinary"""
    cloudinary.config(
        cloud_name=CLOUD_CONFIG["cloud_name"],
        api_key=CLOUD_CONFIG["api_key"],
        api_secret=CLOUD_CONFIG["api_secret"]
    )

def upload_single_file(file_path):
    """Upload satu file ke Cloudinary"""
    if not os.path.exists(file_path):
        print(f"   ❌ File tidak ditemukan: {file_path}")
        return None
    
    file_size = os.path.getsize(file_path) / 1024  # KB
    file_name = os.path.basename(file_path)
    
    print(f"   📤 Uploading: {file_name} ({file_size:.1f} KB)")
    
    try:
        result = upload(
            file_path,
            upload_preset=UPLOAD_PRESET,
            use_filename=True,
            unique_filename=False,
            resource_type="image"
        )
        
        print(f"   ✅ Success!")
        print(f"      Public ID: {result.get('public_id', '')}")
        print(f"      URL: {result.get('secure_url', '')[:80]}...")
        print(f"      Size: {result.get('bytes', 0) / 1024:.1f} KB")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    print("=" * 70)
    print("📤 UPLOAD FOTO KE CLOUDINARY")
    print("=" * 70)
    print(f"\n📁 Preset: {UPLOAD_PRESET}")
    print(f"☁️  Cloud: {CLOUD_CONFIG['cloud_name']}")
    
    setup_cloudinary()
    
    # Ambil file arguments
    files_to_upload = []
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            # Support wildcard/glob patterns
            if '*' in arg or '?' in arg:
                import glob
                files_to_upload.extend(glob.glob(arg))
            else:
                files_to_upload.append(arg)
    
    if not files_to_upload:
        print("\n" + "=" * 70)
        print("CARA PAKAI:")
        print("=" * 70)
        print("""
1. Upload satu foto:
   python3 upload-foto-cloudinary.py path/ke/foto.jpg

2. Upload banyak foto:
   python3 upload-foto-cloudinary.py foto1.jpg foto2.jpg foto3.jpg

3. Upload semua foto di folder:
   python3 upload-foto-cloudinary.py /path/to/folder/*.jpg

4. Upload semua JPG dan PNG:
   python3 upload-foto-cloudinary.py /path/to/folder/*.{jpg,png}
""")
        return
    
    # Filter hanya file gambar valid
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    valid_files = []
    
    for f in files_to_upload:
        ext = Path(f).suffix.lower()
        if ext in valid_extensions and os.path.isfile(f):
            valid_files.append(f)
        elif os.path.isdir(f):
            # Jika folder, cari semua gambar di dalamnya
            for root, dirs, files in os.walk(f):
                for file in files:
                    if Path(file).suffix.lower() in valid_extensions:
                        valid_files.append(os.path.join(root, file))
    
    if not valid_files:
        print("\n❌ Tidak ada file gambar valid ditemukan!")
        return
    
    print(f"\n📷 File akan di-upload: {len(valid_files)} file\n")
    
    # Upload setiap file
    success_count = 0
    failed_count = 0
    
    for i, file_path in enumerate(valid_files, 1):
        print(f"\n[{i}/{len(valid_files)}]", end="")
        result = upload_single_file(file_path)
        
        if result:
            success_count += 1
        else:
            failed_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY:")
    print("=" * 70)
    print(f"   ✅ Berhasil: {success_count} foto")
    print(f"   ❌ Gagal: {failed_count} foto")
    
    if success_count > 0:
        print(f"\n🎉 Foto berhasil di-upload ke folder 'galeri-kegiatan'!")
        print(f"\n📝 LANGKAH SELANJUTNYA:")
        print(f"   1. Jalankan generator: python3 bento-masonry-gallery-v5.py")
        print(f"   2. Atau trigger GitHub Actions untuk auto-update")

if __name__ == "__main__":
    main()

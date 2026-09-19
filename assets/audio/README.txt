AUDIO MUSIC PLAYER
===================

Folder ini berisi file audio untuk Music Player (background music).

File yang ada saat ini (step-from-hell.mp3, lagu-02.mp3 ... lagu-05.mp3)
adalah placeholder SILENT berdurasi 30 detik yang otomatis di-generate
agar player bisa langsung berfungsi (progress bar, play/pause, next, dst).

CARA MENGGANTI DENGAN LAGU ASLI:
1. Hapus file placeholder (mis. step-from-hell.mp3).
2. Letakkan file MP3 asli Anda dengan nama yang SAMA, mis:
     step-from-hell.mp3   <- lagu "Step From Hell" asli
     lagu-02.mp3
     lagu-03.mp3
     lagu-04.mp3
     lagu-05.mp3
3. Tidak perlu mengubah kode apapun — player otomatis memakai file baru.

CARA MENAMBAH / UBAH DAFTAR LAGU:
Edit array `playlist` di file:
    assets/js/music-player.js
Cukup tambahkan / ubah objek { title, src } pada array tersebut.

Jika sebuah file MP3 tidak ditemukan, player akan otomatis menampilkan
status "File audio tidak tersedia" untuk lagu tersebut (tidak crash).

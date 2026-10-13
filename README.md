# OSExercise

Praktikum konsep proses Linux untuk kelas: `fork()`, `execlp()`, dan `wait()`.
Materi memakai empat demonstrasi baru dengan konteks petugas label, arsip, dan penulis laporan.
Tidak memuat teks soal ujian atau kunci soal asal.

**[Buka modul PDF](output/pdf/Modul_Konsep_Proses_Linux.pdf)** — 9 halaman dengan penjelasan, kode, hasil eksekusi, screenshot, diskusi, dan tautan repositori.

## Isi

| Folder | Isi |
| --- | --- |
| `src/` | Empat program C untuk praktik |
| `screenshots/` | Lima screenshot tampilan transkrip hasil eksekusi aktual |
| `logs/` | Log mentah PTY, teks keluaran, metadata, dan hasil verifikasi |
| `output/pdf/` | Modul kelas |
| `tools/` | Sumber penyusunan PDF, penangkapan transkrip, dan catatan kelas |

## Menjalankan program di Linux

Gunakan terminal Linux dengan GCC. Pada host Windows, jalankan melalui lingkungan Linux seperti WSL.

```sh
git clone https://github.com/SeedFlora/OSExercise.git
cd OSExercise
mkdir -p bin

for nama in 01_loket_label 02_dua_petugas 03_ganti_program 04_gagal_ganti; do
    gcc -std=c11 -Wall -Wextra -Werror -pedantic "src/$nama.c" -o "bin/$nama"
done

./bin/01_loket_label
./bin/02_dua_petugas
./bin/03_ganti_program
./bin/04_gagal_ganti
```

Program 03 membutuhkan executable `printf` pada `PATH`. Program 04 sengaja mencoba berkas lokal yang tidak tersedia dan berakhir dengan status `2`; program 01–03 pada eksekusi yang disimpan berakhir dengan status `0`.

Jalankan keluaran langsung ke terminal/PTY. Pengalihan ke file atau pipe dapat mengubah penyanggaan stdout. PID dan urutan pesan dapat berubah saat program diulang.

## Bukti eksekusi

Program telah dikompilasi dengan GCC 15.2.0 dan dijalankan pada Linux WSL2 melalui PTY, dengan toolchain Alpine dalam chroot terisolasi. Keempat source lolos kompilasi dengan flag di atas. Program 01 dan 02 juga masing-masing diulang lima kali.

PNG dalam `screenshots/` adalah screenshot halaman browser lokal yang menampilkan transkrip PTY asli. Gambar tersebut bukan screenshot jendela terminal desktop. Log keluaran disimpan; urutan di satu gambar bukan jaminan untuk semua jadwal proses.

## Menyusun kembali materi

`tools/build_pdf.py` menggunakan Python dengan `reportlab` dan `Pillow`, serta font Calibri/Consolas dari Windows. Jalankan dari folder ini dengan `python tools/build_pdf.py`. Script memakai source dan bukti eksekusi yang sudah tersimpan, sehingga tidak menjalankan program C lagi.

`tools/make_screenshots.cjs` menggunakan Node.js dan `playwright`. Browser dapat dipilih melalui `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`; tanpa variabel itu, script memakai Chromium dari Playwright.

`tools/run_experiments.py` adalah harness Windows/WSL untuk lingkungan eksekusi historis. Lokasi toolchain dapat diatur melalui `OS_EXERCISE_TOOLCHAIN_WINDOWS` dan `OS_EXERCISE_TOOLCHAIN_LINUX`. Untuk praktik biasa, gunakan langkah GCC di atas.

## Sumber teknis

- [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html)
- [exec(3)](https://man7.org/linux/man-pages/man3/exec.3.html)
- [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html)
- [stdio(3)](https://man7.org/linux/man-pages/man3/stdio.3.html)

Repositori: [SeedFlora/OSExercise](https://github.com/SeedFlora/OSExercise).

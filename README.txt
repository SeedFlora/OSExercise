LAB KONSEP PROSES LINUX
Materi kelas berbahasa Indonesia - 13 Oktober 2026

Isi paket:
  src/          Empat program C baru untuk demonstrasi konsep.
  bin/          Binary hasil kompilasi Linux Alpine (gunakan source untuk Linux lain).
  logs/         Transkrip mentah PTY, transkrip teks, dan metadata eksekusi.
  screenshots/  Screenshot tampilan transkrip eksekusi aktual di browser lokal.
  output/pdf/   Modul kelas dalam PDF.
  tools/        Skrip reproduksi, sumber penyusunan PDF, catatan diskusi.

Materi memakai konteks loket label, petugas arsip, dan penulis laporan.
Tidak menyertakan lampiran asal, teks soal ujian, rubrik, atau kunci soal ujian.
Semua source menggunakan printf(), fork(), execlp(), wait(), dan return;
tidak menambah fungsi C lain dalam materi.

MENJALANKAN ULANG PADA TERMINAL LINUX
1. Buka terminal di folder ini.
2. mkdir -p bin
3. gcc -std=c11 -Wall -Wextra -Werror -pedantic src/01_loket_label.c -o bin/01_loket_label
4. ./bin/01_loket_label
5. Ulangi langkah kompilasi dan eksekusi untuk source 02, 03, dan 04.
Program 04 sengaja berakhir dengan status 2 setelah execlp() gagal.
Program 03 memerlukan executable printf pada PATH (umumnya tersedia di Linux).
Jalankan langsung pada terminal/PTY; jangan menyalurkan stdout ke pipe atau file.

LINGKUNGAN BUKTI EKSEKUSI
Host Windows; kernel Linux dari WSL2, distribusi docker-desktop.
Toolchain Alpine berada di D:\tmp\konsep-proses-toolchain-20261013.
Path Linux-nya /mnt/host/d/tmp/konsep-proses-toolchain-20261013.
Program dikompilasi dan dijalankan dalam chroot tersebut melalui PTY Linux.
Tidak menggunakan emulasi fork di Windows.
Hasil asli disimpan utuh pada logs/*.pty.log; versi *.txt hanya menormalkan CRLF.
Screenshot menangkap halaman browser lokal yang menampilkan teks hasil asli,
bukan screenshot jendela terminal desktop. Isi keluaran tidak ditulis manual.
PID dan urutan penjadwalan dapat berubah pada pengulangan.

VERIFIKASI
Keempat program lolos kompilasi dengan -Wall -Wextra -Werror -pedantic.
Status program 01, 02, dan 03: 0. Status program 04: 2, sesuai rancangan.
Program 01 dan 02 masing-masing diulang lima kali lagi dan seluruhnya selesai.
Modul PDF memiliki sembilan halaman; halaman terakhir memuat tautan GitHub.
Lima screenshot sudah disisipkan ke PDF dan tersedia sebagai PNG terpisah.

SUMBER TEKNIS
https://man7.org/linux/man-pages/man2/fork.2.html
https://man7.org/linux/man-pages/man3/exec.3.html
https://man7.org/linux/man-pages/man2/wait.2.html
https://man7.org/linux/man-pages/man3/stdio.3.html

"""Build the teaching PDF from fresh source files and verified execution captures."""
from pathlib import Path
import json
import re
import html
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from PIL import Image
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "output" / "pdf" / "Modul_Konsep_Proses_Linux.pdf"
for name, path in [("Body", "calibri.ttf"), ("Bold", "calibrib.ttf"),
                   ("Mono", "consola.ttf"), ("MonoBold", "consolab.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(Path(r"C:\Windows\Fonts") / path)))

W, H = 841.89, 595.28
INK, BLUE, TEAL, PALE, MUTED = map(HexColor, ["#173149", "#13577e", "#007c80", "#edf4f7", "#586c7b"])
C = canvas.Canvas(str(OUT), pagesize=(W,H))
C.setTitle("Praktikum konsep proses Linux - fork, execlp, wait")
C.setAuthor("Materi kelas")
C.setSubject("Demonstrasi baru dengan bukti eksekusi Linux PTY")
PAGES = 9
REPOSITORY_URL = "https://github.com/SeedFlora/OSExercise"
ONLINE_PDF_URL = REPOSITORY_URL + "/blob/main/output/pdf/Modul_Konsep_Proses_Linux.pdf"

def text(s, x, y, size=11, font="Body", color=INK):
    C.setFillColor(color); C.setFont(font, size); C.drawString(x,y,s)

def para(s, x, top, width, size=11, leading=None, color=INK):
    style=ParagraphStyle("p", fontName="Body", fontSize=size, leading=leading or size*1.3,
                         textColor=color, alignment=TA_LEFT)
    p=Paragraph(s,style); _, h=p.wrap(width,1000); p.drawOn(C,x,top-h)
    if top-h < 41:
        raise ValueError(f"Text overflow: {s[:80]} bottom={top-h}")
    return top-h

def page(n, eyebrow, title, sub=""):
    C.setFillColor(white); C.rect(0,0,W,H,fill=1,stroke=0)
    C.setFillColor(TEAL); C.rect(0,H-9,W,9,fill=1,stroke=0)
    text(eyebrow.upper(),42,H-37,9,"Bold",TEAL)
    text(title,42,H-69,25,"Bold")
    if sub: para(sub,42,H-83,W-84,10.5,color=MUTED)
    C.setStrokeColor(HexColor("#d8e4e9")); C.line(42,35,W-42,35)
    text("PRAKTIKUM PROSES LINUX  |  13 Oktober 2026",42,21,8,color=MUTED)
    text(f"{n} / {PAGES}",W-72,21,8,color=MUTED)

def card(x, top, width, height, title, body):
    C.setFillColor(PALE); C.roundRect(x,top-height,width,height,9,fill=1,stroke=0)
    text(title,x+15,top-25,16,"Bold",BLUE)
    para(body,x+15,top-40,width-30,11)

def code(stem,x,top,width,size=9.2,lead=11):
    lines=(BASE/"src"/f"{stem}.c").read_text(encoding="utf-8").splitlines()
    height=len(lines)*lead+26
    if top-height < 44: raise ValueError("Code too tall")
    C.setFillColor(HexColor("#f3f7f9")); C.roundRect(x,top-height,width,height,7,fill=1,stroke=0)
    for i,line in enumerate(lines):
        if pdfmetrics.stringWidth(line,"Mono",size)>width-35:
            raise ValueError(f"Code too wide: {stem}: {line}")
        text(f"{i+1:02}",x+9,top-19-i*lead,7.1,color=MUTED)
        font="MonoBold" if re.search(r"\b(fork|wait|execlp)\(",line) else "Mono"
        text(line,x+29,top-19-i*lead,size,font)
    return top-height

def shot(stem,x,top,width):
    path=BASE/"screenshots"/f"{stem}.png"
    with Image.open(path) as im: sw,sh=im.size
    height=width*sh/sw
    C.drawImage(str(path),x,top-height,width,height,mask="auto")
    return top-height

def note(title,body,x,top,width,size=11):
    text(title,x,top,12,"Bold",BLUE)
    return para(body,x,top-10,width,size)-15

def box(x,y,w,h,label,body):
    C.setFillColor(PALE); C.roundRect(x,y,w,h,7,fill=1,stroke=0)
    text(label,x+12,y+h-22,12,"Bold",TEAL)
    para(body,x+12,y+h-31,w-24,10)

def arrow(x1,y1,x2,y2):
    C.setStrokeColor(TEAL); C.setLineWidth(1.8); C.line(x1,y1,x2,y2)
    if x2>x1: C.line(x2,y2,x2-6,y2+4); C.line(x2,y2,x2-6,y2-4)
    else: C.line(x2,y2,x2-4,y2+6); C.line(x2,y2,x2+4,y2+6)

page(1,"Konsep inti","Satu proses, beberapa alur kerja",
     "Materi kelas dengan contoh baru. Ikuti proses yang mengeksekusi setiap baris, lalu cocokkan dengan bukti praktik.")
card(42,466,241,151,"fork()","Membentuk child baru. Parent dan child melanjutkan setelah pemanggilan dengan nilai kembali berbeda. Variabel biasa berada pada ruang memori masing-masing. [1]")
card(299,466,241,151,"execlp()","Mengganti program pada proses pemanggil. PID tetap; keberhasilan tidak kembali ke kode lama. Nama tanpa slash dicari melalui PATH. Kegagalan mengembalikan -1. [2]")
card(556,466,244,151,"wait(NULL)","Parent mengambil satu child yang berakhir. Jika perlu, parent menunggu. Nilai kembali sukses adalah PID child; -1 berarti gagal. NULL tidak menyimpan status akhir. [3]")
text("Mengenali cabang setelah fork()",42,290,15,"Bold")
for x,label,body in [(42,"nilai > 0","Parent menerima PID child."), (299,"nilai == 0","Child menerima penanda nol.<br/>Penanda ini bukan PID asli child."), (556,"nilai == -1","Gagal membentuk child.<br/>Pisahkan cabang kegagalan.")]:
    box(x,183,241 if x<556 else 244,86,label,body)
text("Tiga pertanyaan saat membaca kode",42,153,15,"Bold")
para("Proses mana yang mencapai baris ini? Apakah proses itu sudah berhenti atau berganti program? Apakah ada wait yang membatasi kapan parent dapat melanjutkan?",42,139,730,12)
para("Ruang lingkup C: printf(), fork(), execlp(), wait(), dan return. Tidak ada tambahan API C pada contoh. [1]-[4] adalah manual resmi Linux yang tercantum pada halaman 8.",42,83,745,9.5,color=MUTED)
C.showPage()

metadata=json.loads((BASE/"logs"/"execution_metadata.json").read_text(encoding="utf-8"))
page(2,"Bukti dan reproduksi","Dijalankan pada Linux melalui PTY",
     "Kompilasi dan keluaran di bawah berasal dari eksekusi aktual, bukan prediksi yang ditulis menjadi hasil.")
y=shot("00_lingkungan",42,465,430)
para("Screenshot halaman browser lokal yang menampilkan transkrip PTY asli. Program C menulis ke terminal Linux; sesudahnya, teks hasil ditampilkan untuk ditangkap sebagai gambar.",42,y-13,430,10,color=MUTED)
top=465
top=note("Lingkungan", "Host Windows; kernel Linux WSL2 pada distribusi docker-desktop. Compiler dan libc Alpine berada dalam chroot terisolasi di drive D. Docker daemon tidak diperlukan.",494,top,305)
top=note("Pemeriksaan", "stdout=terminal-PTY membuktikan keluaran program terhubung ke terminal virtual. Semua contoh memakai newline pada printf. Ini menghindari perbedaan dasar akibat penangkapan langsung melalui pipe. [4]",494,top,305)
top=note("Menjalankan ulang", "Di terminal Linux, buat folder bin. Kompilasi setiap source dengan GCC dan flag pada screenshot, lalu jalankan binarinya langsung. Program 03 memerlukan executable printf pada PATH.",494,top,305)
top=note("Jejak yang disimpan", "Source C, binary Linux, log mentah PTY, teks keluaran, screenshot, serta metadata waktu dan hash tersimpan bersama modul. PID dapat berubah setiap kali dijalankan.",494,top,305,10.5)
text("Waktu eksekusi: "+metadata["time"][:19].replace("T"," ")+" (Asia/Bangkok)",42,66,9.5,color=MUTED)
C.showPage()

page(3,"Demonstrasi 01","Loket label: tugas berbeda, alur berbeda",
     "Child menyelesaikan label lalu return. Parent menunggu sebelum menulis laporan penutup.")
text("Source: src/01_loket_label.c",42,482,10,"Bold",TEAL)
code("01_loket_label",42,469,382,9.1,11.7)
y=shot("01_loket_label",444,482,355)
y=para("Screenshot hasil run pertama; nomor PID adalah nilai yang benar-benar teramati.",444,y-9,355,9.5,color=MUTED)-19
y=note("Cara menelusuri", "Pesan pembukaan terjadi sebelum child terbentuk. Child masuk ke cabang tugas == 0 dan berhenti pada return; laporan penutup hanya dicapai parent.",444,y,355)
y=note("Hubungan urutan", "Petugas telah berakhir sebelum parent melewati wait yang berhasil. Pesan PID parent dan pesan tugas child dapat saling mendahului; screenshot hanya menunjukkan satu jadwal.",444,y,355)
para("Cabang tugas < 0 disediakan, tetapi kegagalan fork tidak dipaksakan dalam eksperimen ini.",42,112,382,10.5,color=MUTED)
C.showPage()

page(4,"Demonstrasi 02","Dua petugas dibuat oleh satu pengawas",
     "Hanya parent mencapai fork kedua. Dua wait mengambil dua child, satu per pemanggilan yang berhasil.")
text("Source: src/02_dua_petugas.c",42,485,10,"Bold",TEAL)
code("02_dua_petugas",42,473,410,8.35,9.8)
y=shot("02_dua_petugas",472,485,327)
y=para("Cocokkan PID label/arsip dengan PID yang dikembalikan oleh setiap wait.",472,y-8,327,9.5,color=MUTED)-17
y=note("Pohon proses", "Parent membuat dua child. Setiap child return sebelum mencapai pekerjaan parent berikutnya. Saat keduanya berhasil terbentuk, ada tiga proses yang terlibat.",472,y,327,10.4)
y=note("Yang dapat berubah", "wait(NULL) dapat mengambil salah satu child yang sudah berakhir. Urutan PID yang diambil tidak wajib sama dengan urutan pembentukan. Laporan akhir menunggu kedua wait berhasil.",472,y,327,10.4)
C.showPage()

page(5,"Demonstrasi 03","Berganti program tanpa membuat child",
     "Contoh ini langsung memanggil execlp. Tidak ada fork pada source ini.")
text("Source: src/03_ganti_program.c",42,482,10,"Bold",TEAL)
code("03_ganti_program",42,469,382,9.3,12.4)
y=shot("03_ganti_program",444,482,355)
y=para("Keluaran Kode pekerjaan berasal dari executable printf pengganti, bukan printf C setelah execlp.",444,y-9,355,10,color=MUTED)-19
y=note("Membaca argumen", "Nama printf pertama adalah executable yang dicari pada PATH. Nama berikutnya menjadi argv[0]. Format dan kode pekerjaan adalah argumen program tersebut; (char *)NULL menutup daftar.",444,y,355,10.5)
y=note("Setelah keberhasilan", "Baris pergantian gagal tidak tercetak. Program lama sudah diganti; kode itu tidak dilanjutkan ketika executable pengganti selesai. Status 0 di screenshot adalah status program pengganti.",444,y,355,10.5)
text("Satu proses, program berubah [2]",42,256,15,"Bold")
box(42,183,382,50,"Sebelum", "Proses menjalankan penulis laporan.")
arrow(233,176,233,165)
box(42,106,382,50,"Sesudah", "Proses yang sama menjalankan executable printf.")
para("PID tetap merupakan sifat execlp yang berhasil menurut manual. Screenshot keluaran ini tidak mengukur PID secara langsung.",42,93,382,9.5,color=MUTED)
C.showPage()

page(6,"Demonstrasi 04","Pergantian gagal: kode lama berlanjut",
     "Jalur lokal diperiksa tidak tersedia sebelum program dijalankan. Percobaan ini sengaja menghasilkan status keluar 2.")
text("Source: src/04_gagal_ganti.c",42,482,10,"Bold",TEAL)
code("04_gagal_ganti",42,469,382,9.2,12.4)
y=shot("04_gagal_ganti",444,482,355)
y=para("Log juga menyimpan pemeriksaan bahwa executable lokal memang tidak ada.",444,y-9,355,10,color=MUTED)-18
y=note("Alur yang terjadi", "execlp tidak dapat menjalankan berkas itu dan kembali dengan -1. printf sesudahnya lalu dijalankan, kemudian return 2 mengakhiri program lama.",444,y,355,10.5)
y=note("Makna status 2", "Angka 2 dipilih oleh source ini untuk menandai jalur gagal. Angka tersebut bukan nilai kembali execlp; nilai kembali fungsi pada kegagalan adalah -1. [2]",444,y,355,10.5)
text("Pisahkan tiga hal",42,242,15,"Bold")
box(42,177,382,45,"Pemanggilan fungsi", "execlp gagal kembali ke kode lama dengan -1.")
box(42,122,382,45,"Pesan keluaran", "Pesan kembali dicetak oleh program lama.")
box(42,67,382,45,"Status program", "return 2 diterima shell sebagai status keluar 2.")
para("Keberhasilan wait(NULL) pada contoh dengan child hanya memastikan child telah berakhir; status tugasnya tidak disimpan. [3]",444,y,355,9.7,color=MUTED)
C.showPage()

page(7,"Pengamatan ulang","Ulangi hasil, periksa batas urutan",
     "Demonstrasi 01 dan 02 masing-masing dijalankan lima kali lagi pada PTY yang sama.")
repeats=(BASE/"logs"/"05_pengulangan.txt").read_text(encoding="utf-8")
parts=re.findall(r"=== (\S+) / run (\d+) ===\n(.*?)(?====|\Z)",repeats,re.S)
assert len(parts)==10
rows=[]
for stem, run, body in parts:
    assert "Status keluar program: 0" in body
    if stem=="01_loket_label":
        assert body.count("Loket label dibuka.")==1
        assert body.count("Petugas: label paket K-31 siap.")==1
        assert body.index("Petugas: label paket K-31 siap.")<body.index("Pengawas: petugas telah berakhir.")
    else:
        lp=re.search(r"PID label = (\d+)",body).group(1)
        ap=re.search(r"PID arsip = (\d+)",body).group(1)
        waits=re.findall(r"Diambil ke-\d: PID (\d+)",body)
        assert len(waits)==2 and set(waits)=={lp,ap}
        assert body.index("paket K-31 siap.")<body.index("kedua petugas telah berakhir.")
        assert body.index("dokumen R-18 siap.")<body.index("kedua petugas telah berakhir.")
        rows.append((run,lp,ap,waits[0],waits[1]))
text("PID yang teramati pada demonstrasi 02",42,464,15,"Bold")
cols=[42,94,195,296,396]
heads=["Run","PID label","PID arsip","wait ke-1","wait ke-2"]
C.setFillColor(BLUE); C.roundRect(42,422,464,29,4,fill=1,stroke=0)
for x,h in zip(cols,heads): text(h,x+10,432,10,"Bold",white)
for i,row in enumerate(rows):
    yy=421-(i+1)*33
    C.setFillColor(PALE if i%2==0 else white); C.rect(42,yy,464,33,fill=1,stroke=0)
    for x,v in zip(cols,row): text(v,x+10,yy+12,10.5,"Mono")
top=464
top=note("Hasil verifikasi", "Empat source lolos kompilasi dengan -Wall -Wextra -Werror -pedantic. Demo 01-03 berakhir dengan status 0; demo 04 berakhir dengan status 2 yang memang dirancang.",534,top,265,10.5)
top=note("Sepuluh run tambahan", "Semua run tambahan selesai dengan status 0. Demo 01 mempertahankan batas child sebelum penutup. Demo 02 mengambil tepat dua PID child sebelum penutup.",534,top,265,10.5)
top=note("Batas bukti", "Data ini memeriksa contoh dan lingkungan yang dipakai. Lima pengulangan tidak membuktikan semua jadwal yang mungkin; jaminan urutan tetap ditentukan oleh alur kode.",534,top,265,10.5)
text("Kenapa memakai terminal? [4]",42,215,15,"Bold")
para("stdout yang diarahkan ke file atau pipe dapat memiliki penyanggaan berbeda. Teks yang belum dikeluarkan sebelum fork dapat ikut tersalin; isi buffer lama sebelum execlp berhasil dapat hilang. Newline dan PTY menjaga fokus percobaan pada alur proses.",42,201,465,11)
para("Logs 05_pengulangan.pty.log mempertahankan byte keluaran asli. Versi .txt hanya menormalkan akhir baris untuk dibaca. Pemeriksaan tidak memaksa kegagalan fork atau menambah fungsi C.",42,113,740,10.5,color=MUTED)
C.showPage()

notes=json.loads((BASE/"tools"/"catatan_kelas.json").read_text(encoding="utf-8"))
page(8,"Diskusi kelas dan sumber","Tandai alur, amati, lalu jelaskan",
     "Pertanyaan berikut memakai demonstrasi baru dalam modul dan tidak disertai kunci jawaban ujian.")
top=470
for item in notes["diskusi"]:
    text(item["id"],42,top,12,"Bold",TEAL)
    top=para(html.escape(item["pertanyaan"]),76,top+3,418,10.7)-20
top=note("Pola praktik", "Baca source dan gambar alurnya sebelum menjalankan program. Simpan prediksi sendiri, bandingkan dengan keluaran, lalu jelaskan batas yang dijamin kode.",42,top,452,10.7)
text("Pegangan saat berdiskusi",533,470,15,"Bold")
top=449
short=["Child melanjutkan setelah fork, dengan penanda kembali nol.",
       "return dari main mengakhiri proses yang menjalankannya.",
       "Satu wait yang berhasil mengambil satu child.",
       "execlp yang berhasil mengganti program dan tidak kembali.",
       "wait(NULL) tidak menyimpan status akhir tugas child."]
for s in short:
    top=para("<b>•</b> "+s,533,top,266,10.5)-9
text("Sumber primer Linux",533,top-6,14,"Bold")
sy=top-26
for i,(label,url) in enumerate([
    ("fork(2)","https://man7.org/linux/man-pages/man2/fork.2.html"),
    ("exec(3)","https://man7.org/linux/man-pages/man3/exec.3.html"),
    ("wait(2)","https://man7.org/linux/man-pages/man2/wait.2.html"),
    ("stdio(3)","https://man7.org/linux/man-pages/man3/stdio.3.html")],1):
    text(f"[{i}] {label} - Linux man-pages",533,sy,10.3,"Bold",BLUE)
    C.linkURL(url,(533,sy-3,799,sy+10),relative=0,thickness=0)
    sy-=22
para("Klik nama manual untuk membuka sumber. Diperiksa pada 13 Oktober 2026. Materi dibuat untuk pengajaran konsep dengan contoh yang berbeda.",533,sy-4,266,9.5,color=MUTED)
C.showPage()
page(9,"Repositori praktik","Kode dan bahan praktik di GitHub",
     "Ambil source, lihat screenshot, dan buka modul terbaru melalui repositori OSExercise.")
card(42,467,757,82,"SeedFlora / OSExercise",REPOSITORY_URL)
C.linkURL(REPOSITORY_URL,(42,385,799,467),relative=0,thickness=0)
text("Ambil dan jalankan di terminal Linux",42,357,15,"Bold")
commands=[
    "$ git clone https://github.com/SeedFlora/OSExercise.git",
    "$ cd OSExercise",
    "$ mkdir -p bin",
    "$ gcc -std=c11 -Wall -Wextra -Werror -pedantic \\",
    "  src/01_loket_label.c -o bin/01_loket_label",
    "$ ./bin/01_loket_label"
]
C.setFillColor(PALE); C.roundRect(42,211,493,128,7,fill=1,stroke=0)
for i,line in enumerate(commands): text(line,57,316-i*16,10.2,"Mono")
para("Perintah di atas adalah panduan reproduksi. Lanjutkan dengan source 02, 03, dan 04. Gunakan terminal langsung agar pengamatan alur tidak tercampur perubahan buffering. Program 04 sengaja menghasilkan status 2.",42,194,493,11)
text("Bahan dalam repositori",42,120,14,"Bold")
para("src/: empat program C; screenshots/: lima tangkapan transkrip; logs/: bukti keluaran dan verifikasi; output/pdf/: modul ini; tools/: sumber penyusunan materi.",42,105,493,10.5)
qr=QrCodeWidget(REPOSITORY_URL)
qr_bounds=qr.getBounds(); qr_width=qr_bounds[2]-qr_bounds[0]; qr_height=qr_bounds[3]-qr_bounds[1]
qr_drawing=Drawing(152,152,transform=[152/qr_width,0,0,152/qr_height,0,0])
qr_drawing.add(qr)
renderPDF.draw(qr_drawing,C,598,193)
para("Pindai untuk membuka GitHub",574,184,225,10.5,color=MUTED)
C.setFillColor(BLUE); C.roundRect(574,110,225,41,7,fill=1,stroke=0)
text("Buka PDF terbaru di GitHub",589,126,11,"Bold",white)
C.linkURL(ONLINE_PDF_URL,(574,110,799,151),relative=0,thickness=0)
para("Klik banner repositori atau tombol PDF untuk membuka bahan daring.",574,91,225,9.5,color=MUTED)
C.showPage()
C.save()
print(OUT)
print(f"PDF created: {PAGES} pages")

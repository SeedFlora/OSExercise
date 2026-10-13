#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("Penulis laporan: mencoba alat lokal.\n");

    execlp("./alat_laporan_tidak_tersedia",
           "alat_laporan_tidak_tersedia", (char *)NULL);

    printf("Penulis laporan: kembali karena exec gagal.\n");
    return 2;
}

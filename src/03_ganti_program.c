#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("Penulis laporan: menyerahkan kendali.\n");

    execlp("printf", "printf", "Kode pekerjaan: %s\n",
           "L-42", (char *)NULL);

    printf("Penulis laporan: pergantian gagal.\n");
    return 2;
}

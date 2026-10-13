#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t petugas = fork();
    if (petugas < 0) {
        printf("Pembentukan petugas label gagal.\n");
        return 1;
    }
    if (petugas == 0) {
        printf("Petugas label: paket K-31 siap.\n");
        return 0;
    }
    printf("Pengawas: PID label = %ld\n", (long)petugas);

    petugas = fork();
    if (petugas < 0) {
        printf("Pembentukan petugas arsip gagal.\n");
        if (wait(NULL) < 0) return 2;
        return 1;
    }
    if (petugas == 0) {
        printf("Petugas arsip: dokumen R-18 siap.\n");
        return 0;
    }
    printf("Pengawas: PID arsip = %ld\n", (long)petugas);

    for (int urutan = 1; urutan <= 2; urutan++) {
        pid_t selesai = wait(NULL);
        if (selesai < 0) {
            printf("Pengawas: penantian gagal.\n");
            return 2;
        }
        printf("Diambil ke-%d: PID %ld\n", urutan, (long)selesai);
    }
    printf("Pengawas: kedua petugas telah berakhir.\n");
    return 0;
}

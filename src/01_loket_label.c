#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    printf("Loket label dibuka.\n");
    pid_t tugas = fork();

    if (tugas < 0) {
        printf("Petugas tambahan tidak terbentuk.\n");
        return 1;
    }
    if (tugas == 0) {
        printf("Petugas: label paket K-31 siap.\n");
        return 0;
    }

    printf("Pengawas: PID petugas = %ld\n", (long)tugas);
    if (wait(NULL) < 0) {
        printf("Pengawas: penantian gagal.\n");
        return 2;
    }
    printf("Pengawas: petugas telah berakhir.\n");
    return 0;
}

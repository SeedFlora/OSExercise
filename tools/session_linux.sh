#!/bin/sh
# This script runs INSIDE the isolated Linux root, attached to a PTY.
set -u
cd /lab || exit 1
case "${1:-}" in
  setup)
    echo '$ uname -srm'
    uname -srm
    echo '$ cat /etc/alpine-release'
    cat /etc/alpine-release
    echo '$ gcc --version | head -1'
    gcc --version | head -1
    echo '$ test -t 1 && echo stdout=terminal-PTY'
    test -t 1 || exit 1
    echo stdout=terminal-PTY
    echo '$ command -v printf'
    command -v printf
    echo '$ /usr/bin/printf "%s\n" executable-tersedia'
    /usr/bin/printf '%s\n' executable-tersedia
    ;;
  demo)
    stem="$2"
    mkdir -p bin
    printf '%s\n' '$ gcc -std=c11 -Wall -Wextra -Werror -pedantic \'
    printf '%s\n' "  src/$stem.c -o bin/$stem"
    gcc -std=c11 -Wall -Wextra -Werror -pedantic "src/$stem.c" -o "bin/$stem" || exit 1
    echo 'Kompilasi: OK (tanpa warning)'
    if [ "$stem" = '04_gagal_ganti' ]; then
      echo '$ test ! -e ./alat_laporan_tidak_tersedia'
      test ! -e ./alat_laporan_tidak_tersedia || exit 1
      echo 'Pemeriksaan: alat lokal memang tidak tersedia'
    fi
    echo "\$ ./bin/$stem"
    "./bin/$stem"
    result=$?
    echo "Status keluar program: $result"
    ;;
  repeats)
    for stem in 01_loket_label 02_dua_petugas; do
      for turn in 1 2 3 4 5; do
        echo "=== $stem / run $turn ==="
        "./bin/$stem"
        result=$?
        echo "Status keluar program: $result"
        test "$result" -eq 0 || exit 1
      done
    done
    ;;
  *) exit 2 ;;
esac

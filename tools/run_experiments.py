"""Execute real Linux C programs through a Linux PTY and retain exact output."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import os
from datetime import datetime
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
TOOLCHAIN = Path(os.environ.get("OS_EXERCISE_TOOLCHAIN_WINDOWS", r"D:\tmp\konsep-proses-toolchain-20261013"))
LINUX_ROOT = os.environ.get("OS_EXERCISE_TOOLCHAIN_LINUX", "/mnt/host/d/tmp/konsep-proses-toolchain-20261013")
STEMS = ["01_loket_label", "02_dua_petugas", "03_ganti_program", "04_gagal_ganti"]
lab = TOOLCHAIN / "lab"
(lab / "src").mkdir(parents=True, exist_ok=True)
(lab / "tools").mkdir(exist_ok=True)
for source in (BASE / "src").glob("*.c"):
    shutil.copy2(source, lab / "src" / source.name)
shutil.copy2(BASE / "tools" / "session_linux.sh", lab / "tools" / "session_linux.sh")
records = []
for name, args in [("00_lingkungan", "setup")] + [(s, f"demo {s}") for s in STEMS] + [("05_pengulangan", "repeats")]:
    command = f"chroot {LINUX_ROOT} /bin/sh /lab/tools/session_linux.sh {args}"
    argv = ["wsl.exe", "-d", "docker-desktop", "--", "script", "-q", "-e", "-c", command, "/dev/null"]
    result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
    (BASE / "logs" / f"{name}.pty.log").write_bytes(result.stdout)
    clean = result.stdout.decode("utf-8").replace("\r\n", "\n").replace("\r", "")
    (BASE / "logs" / f"{name}.txt").write_text(clean, encoding="utf-8")
    (BASE / "logs" / f"{name}.stderr.txt").write_bytes(result.stderr)
    records.append({"name": name, "command": argv, "pty_wrapper_exit": result.returncode,
                    "sha256_raw": hashlib.sha256(result.stdout).hexdigest()})
    print(f"{name}: wrapper exit {result.returncode}")
    print(clean)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace") or clean)
metadata = {"time": datetime.now(ZoneInfo("Asia/Bangkok")).isoformat(),
            "environment": "WSL2 Linux; isolated Alpine chroot; Linux script PTY",
            "toolchain_windows": str(TOOLCHAIN), "toolchain_linux": LINUX_ROOT,
            "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE / "src").glob("*.c")},
            "records": records}
(BASE / "logs" / "execution_metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
for s in STEMS:
    binary = lab / "bin" / s
    (BASE / "bin").mkdir(exist_ok=True)
    shutil.copy2(binary, BASE / "bin" / s)
print("Real execution finished. Raw PTY logs and Linux binaries saved.")

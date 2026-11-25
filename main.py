#!/usr/bin/env python3
"""news-image-20261125 entrypoint.

Copies the pre-rendered entry.png (drawn by render.py at build time)
into the grader's output directory.

Standard library only (os + shutil). Deterministic: every run copies
the same bytes, and the output file is world-readable (mode 0644).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("entry.png missing from repository root: " + SRC)
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)
    print("wrote %s (%d bytes)" % (DST, os.path.getsize(DST)))


if __name__ == "__main__":
    main()

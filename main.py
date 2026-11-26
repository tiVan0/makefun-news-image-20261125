#!/usr/bin/env python3
"""Entrypoint for make.fun news-image-20261125 (Builder A, v2).

Copies the pre-drawn entry.png (built at build time by render.py) into
$MAKEFUN_OUTPUT_DIR/entry.png. Standard library only, no network, no
environment secrets. Deterministic: the same input bytes produce the same
output bytes on every run.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    # Fail loudly on a truncated copy instead of shipping a broken image.
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copied entry.png has the wrong size", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

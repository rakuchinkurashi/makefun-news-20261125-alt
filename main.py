#!/usr/bin/env python3
"""Deliver the entry image to the grader's output path.

The artwork is finished and stored in this repository as `news.png`.
This program copies it to `entry.png` inside the output directory
(`/output`, or `$MAKEFUN_OUTPUT_DIR` when set) with a chunked stream
copy, then confirms the destination holds exactly as many bytes as the
source. The copy is the whole behaviour: the result is a pure function
of the repository contents — no network, no clock, no randomness — so
every run writes the same bytes.
"""

import os
import sys
from pathlib import Path

CHUNK = 128 * 1024


def resolve_paths() -> tuple:
    here = Path(__file__).resolve().parent
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    return here / "news.png", out / "entry.png"


def stream_copy(src: Path, dst: Path) -> int:
    written = 0
    with src.open("rb") as fin, dst.open("wb") as fout:
        while True:
            block = fin.read(CHUNK)
            if not block:
                break
            fout.write(block)
            written += len(block)
    return written


def main() -> int:
    src, dst = resolve_paths()
    if not src.is_file():
        print(f"source image missing: {src}", file=sys.stderr)
        return 1
    with src.open("rb") as handle:
        magic = handle.read(8)
    if not (magic.startswith(b"\x89PNG\r\n\x1a\n")
            or magic.startswith(b"\xff\xd8\xff")):
        print(f"source is not a PNG or JPEG image: {src}", file=sys.stderr)
        return 1
    dst.parent.mkdir(parents=True, exist_ok=True)
    written = stream_copy(src, dst)
    expected = src.stat().st_size
    if written != expected or dst.stat().st_size != expected:
        print(f"copy incomplete: wrote {written} of {expected} bytes",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

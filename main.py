#!/usr/bin/env python3
"""Write the entry image to the output directory.

The entry is a pre-made image held in this repository. This program only
copies it to the path the grader reads, so the output is fully determined
by the repository contents: no network, no randomness, no timestamps, and
two runs write byte-identical files. The copy is verified by comparing the
file sizes of source and target.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "news.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = OUTPUT_DIR / "entry.png"


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit("entry image not found: %s" % SOURCE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    if not TARGET.is_file() or TARGET.stat().st_size != SOURCE.stat().st_size:
        raise SystemExit("entry image copy failed: %s" % TARGET)


if __name__ == "__main__":
    main()

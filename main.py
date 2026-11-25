#!/usr/bin/env python3
"""Write the entry image to /output/entry.png.

THE GLOBAL DISPATCH — one image summing up the world's news of
Wednesday, 25 November 2026. The image is bundled in this repository
as entry.png; this program copies it byte-for-byte to the output path
so the judge sees exactly the bytes shipped here.
"""

import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    size = os.path.getsize(OUTPUT)
    print(f"wrote {OUTPUT}: {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Write the entry image to /output/entry.png.

THE GLOBAL DISPATCH — one image summing up the world's news of
Wednesday, 25 November 2026. The image is bundled in this repository
as entry.png; this program copies it byte-for-byte to the output path
so the judge sees exactly the bytes shipped here.
"""

import hashlib
import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024


def png_dimensions(path):
    """Return (width, height) of a PNG file, rejecting anything else."""
    with open(path, "rb") as fh:
        header = fh.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("output is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    size = os.path.getsize(OUTPUT)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB limit")
    width, height = png_dimensions(OUTPUT)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            f"entry.png is {width}x{height}, over the 1024x1024 limit"
        )
    print(
        f"wrote {OUTPUT}: {width}x{height}, {size} bytes, "
        f"sha256 {sha256_file(OUTPUT)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

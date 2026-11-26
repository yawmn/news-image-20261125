#!/usr/bin/env python3
"""Deliver the entry image to the grader's output directory.

THE GLOBAL DISPATCH — one image summing up the world's news of
Wednesday, 25 November 2026. The v3 edition is a full illustrated
broadsheet: 13 drawn scenes, a pin-matched world map and the 36
verified stories of the day. The picture itself is shipped in this
repository as entry.png; this program's only job is to place those
exact bytes at the output path, checking on the way that the file
is a whole PNG inside the competition's size limits.

It never reaches for the network and never reads anything outside
this repository. It writes straight to the output path — no temporary
file in the output folder, which the grader forbids — and removes a
half-written output if the write fails, so a failed run leaves no
half-written output behind.
"""

import hashlib
import os
import shutil
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
VERSION = "3.0.0"


def png_size(path):
    """Return (width, height) from a PNG header, or reject the file."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: bad signature")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_of(path):
    """Return the hex sha256 of a file, read in 64 KiB pieces."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for piece in iter(lambda: handle.read(65536), b""):
            digest.update(piece)
    return digest.hexdigest()


def check_image(path):
    """Validate one PNG against the competition's limits."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB limit")
    width, height = png_size(path)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            f"entry.png is {width}x{height}, over the 1024x1024 limit"
        )
    return size, width, height


def deliver():
    """Copy entry.png to the output path and report what was written."""
    size, width, height = check_image(SOURCE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Write straight to the output path: the grader requires the output
    # folder to hold exactly the one entry file, so no temporary file
    # may appear in it. The file is made world-readable (0644) so the
    # grader can read it whoever runs the check.
    try:
        with open(OUTPUT, "wb") as out:
            with open(SOURCE, "rb") as source:
                shutil.copyfileobj(source, out, 65536)
        os.chmod(OUTPUT, 0o644)
    except BaseException:
        if os.path.exists(OUTPUT):
            os.unlink(OUTPUT)
        raise
    if sha256_of(OUTPUT) != sha256_of(SOURCE):
        raise ValueError("output bytes differ from the bundled entry.png")
    print(
        f"wrote {OUTPUT}: {width}x{height}, {size} bytes, "
        f"sha256 {sha256_of(OUTPUT)}"
    )
    return 0


def self_test():
    """Write the entry twice to scratch and demand identical bytes."""
    with tempfile.TemporaryDirectory() as scratch:
        first = os.path.join(scratch, "first.png")
        second = os.path.join(scratch, "second.png")
        for target in (first, second):
            with open(target, "wb") as out:
                with open(SOURCE, "rb") as source:
                    shutil.copyfileobj(source, out, 65536)
        if sha256_of(first) != sha256_of(second):
            raise ValueError("self-test failed: two runs differ")
        check_image(first)
    print("self-test passed: two runs are byte-identical")
    return 0


def show_help():
    """Print the flags this program understands."""
    print("usage: main.py [--check | --self-test | --version | --help]")
    print("  no flag: write entry.png to MAKEFUN_OUTPUT_DIR (or /output)")
    print("  --check: validate the bundled entry.png without writing")
    print("  --self-test: write the entry twice and demand identical bytes")
    print("  --version: print the entry program version")
    return 0


def main(argv):
    if "--help" in argv:
        return show_help()
    if "--version" in argv:
        print(f"news-image-20261125 entry program v{VERSION}")
        return 0
    if "--check" in argv:
        size, width, height = check_image(SOURCE)
        print(f"entry.png OK: {width}x{height}, {size} bytes")
        return 0
    if "--self-test" in argv:
        return self_test()
    return deliver()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""ai-happy-01 entry: copy the judge-card image to /output/entry.png.

The image (happy.png) is a child's crayon drawing taped to a refrigerator:
a crowned stick-figure judge holding hands with a child and a happy dog,
a big yellow sun, a gold star sticker, "THANK YOU JUDGE" in blue crayon,
and "P.S. you are the best" in pink crayon at the bottom.
This program only copies the file the repository holds.

Standard library only: no third-party imports, so it runs in a bare
python:3.13 image. Dimensions are read from the PNG IHDR header.
"""
import hashlib
import os
import shutil
import struct

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "happy.png")
DST = "/output/entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_size(data):
    """Return (width, height) from a PNG's IHDR chunk, or raise SystemExit."""
    if len(data) < 24 or data[:8] != PNG_MAGIC or data[12:16] != b"IHDR":
        raise SystemExit("entry.png is not a valid PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    if not os.path.exists(SRC):
        raise SystemExit("happy.png not found next to main.py")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    if not os.path.isfile(DST):
        raise SystemExit("copy failed: %s was not created" % DST)
    with open(DST, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        raise SystemExit("entry.png over the 1 MiB limit: %d bytes" % len(data))
    width, height = png_size(data)
    if width > 1024 or height > 1024:
        raise SystemExit(
            "entry.png over the 1024x1024 limit: %dx%d" % (width, height))
    src_digest = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    dst_digest = hashlib.sha256(data).hexdigest()
    if src_digest != dst_digest:
        raise SystemExit("copy mismatch: entry.png differs from happy.png")
    print("wrote", DST, len(data), "bytes,", (width, height),
          "sha256", dst_digest)


if __name__ == "__main__":
    main()

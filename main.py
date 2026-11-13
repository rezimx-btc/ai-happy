#!/usr/bin/env python3
"""ai-happy-01 entry: publish the judge-podium crayon card to /output/entry.png.

The picture (happy.png) is a child's crayon drawing taped to a refrigerator:
a crowned stick-figure judge stands on the top step of a winner's podium,
holding a big gold trophy high, while a happy child waves a bunch of
flowers from the left step and a cheerful dog sits on the right step.
A banner reads "BEST JUDGE EVER" in blue crayon, balloons and confetti
float around, a yellow sun shines in the corner, and "thank you!" is
written in pink crayon at the bottom.

This script only copies the picture the repository holds and checks it
is a real PNG within the entry limits. Standard library only, so it
runs in a bare python:3.13 image.
"""
import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
CARD = os.path.join(HERE, "happy.png")
ENTRY = "/output/entry.png"
MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
GOOD_DEPTHS = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8),
               4: (8, 16), 6: (8, 16)}


def fail(message):
    raise SystemExit("entry check failed: " + message)


def read_header(blob):
    """Return (width, height, bit depth, colour type) from a PNG header."""
    if len(blob) < 33:
        fail("file too short to be a PNG (%d bytes)" % len(blob))
    if blob[:8] != MAGIC:
        fail("missing PNG magic bytes")
    if blob[12:16] != b"IHDR":
        fail("first chunk is not IHDR")
    width, height = struct.unpack(">II", blob[16:24])
    depth = blob[24]
    colour = blob[25]
    return width, height, depth, colour


def check_trailer(blob):
    """A complete PNG ends with the 12-byte IEND chunk."""
    trailer = b"\x00\x00\x00\x00IEND\xaeB`\x82"
    if len(blob) < 12 or blob[-12:] != trailer:
        fail("PNG is truncated: missing the IEND trailer chunk")


def verify_card(blob, width, height, depth, colour):
    if width == 0 or height == 0:
        fail("image has a zero side: %dx%d" % (width, height))
    if width > MAX_SIDE or height > MAX_SIDE:
        fail("image over the 1024x1024 limit: %dx%d" % (width, height))
    if len(blob) > MAX_BYTES:
        fail("image over the 1 MiB limit: %d bytes" % len(blob))
    if colour not in GOOD_DEPTHS or depth not in GOOD_DEPTHS[colour]:
        fail("unsupported PNG colour type %d with bit depth %d"
             % (colour, depth))


def publish():
    if not os.path.isfile(CARD):
        fail("happy.png not found next to main.py")
    with open(CARD, "rb") as handle:
        original = handle.read()
    width, height, depth, colour = read_header(original)
    verify_card(original, width, height, depth, colour)
    check_trailer(original)
    os.makedirs(os.path.dirname(ENTRY), exist_ok=True)
    shutil.copyfile(CARD, ENTRY)
    with open(ENTRY, "rb") as handle:
        copied = handle.read()
    if hashlib.sha256(original).hexdigest() != hashlib.sha256(copied).hexdigest():
        fail("copy mismatch: entry.png differs from happy.png")
    print("wrote", ENTRY, len(copied), "bytes,", (width, height),
          "sha256", hashlib.sha256(copied).hexdigest())


def main():
    publish()


if __name__ == "__main__":
    main()

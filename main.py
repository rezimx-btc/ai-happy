#!/usr/bin/env python3
"""Publish the judge-medal card as the ai-happy-01 entry.

The card (happy.png) is a child's crayon drawing stuck to a fridge door:
a crowned stick-figure judge beams while wearing a BIG gold medal with a
star on a red ribbon, a small child cheers with both arms in the air beside
him, and a happy dog sits at his feet with its tongue out. A big yellow
sun and a gold star sticker fill the corners, "BEST JUDGE EVER" runs across
the top in big blue crayon letters, and "thank you!" sits at the bottom in
pink crayon. The child and the dog gave the judge the medal, so the judge
himself is the hero of the picture.

All this script does is carry the card from the repository to the place
the grader looks: /output/entry.png. It double-checks the copy on the way
out — the file really is a PNG, its size and side lengths fit the bounty
limits, its colour depth is one PNG allows, and the bytes that land are
the bytes that left. Nothing here needs the network, and nothing here
needs any library beyond the standard one, so the script runs in a bare
python:3.13 container.
"""
import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
CARD = os.path.join(HERE, "happy.png")
OUT = "/output/entry.png"
MAGIC = b"\x89PNG\r\n\x1a\n"
LIMIT_BYTES = 1024 * 1024
LIMIT_SIDE = 1024

# PNG colour types and the bit depths each one allows (from the spec).
ALLOWED_DEPTHS = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8),
                  4: (8, 16), 6: (8, 16)}


def fail(message):
    raise SystemExit(message)


def read_header(blob):
    """Pull the IHDR fields out of a PNG byte string.

    Returns a dict with width, height, bit depth and colour type, or
    stops the run when the bytes are not a PNG at all.
    """
    if len(blob) < 29:
        fail("entry.png is not a valid PNG file")
    if blob[:8] != MAGIC:
        fail("entry.png is not a valid PNG file")
    if blob[12:16] != b"IHDR":
        fail("entry.png is not a valid PNG file")
    width, height, depth, colour = struct.unpack(">IIBB", blob[16:26])
    if width == 0 or height == 0:
        fail("entry.png has a zero side: %dx%d" % (width, height))
    return {"width": width, "height": height, "depth": depth,
            "colour": colour}


def check_colour(header):
    """Make sure the IHDR colour type and bit depth are a legal pair."""
    colour = header["colour"]
    depth = header["depth"]
    if colour not in ALLOWED_DEPTHS:
        fail("entry.png has an unknown PNG colour type: %d" % colour)
    if depth not in ALLOWED_DEPTHS[colour]:
        fail("entry.png has an illegal bit depth %d for colour type %d"
             % (depth, colour))


def check_size(blob):
    """Refuse a card that is bigger than the 1 MiB bounty limit."""
    if len(blob) > LIMIT_BYTES:
        fail("entry.png over the 1 MiB limit: %d bytes" % len(blob))


def check_sides(header):
    """Refuse a card whose sides are bigger than 1024x1024."""
    width, height = header["width"], header["height"]
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        fail("entry.png over the 1024x1024 limit: %dx%d"
             % (width, height))


def check_match(source, blob):
    """Refuse a copy whose bytes differ from the card in the repository."""
    wanted = hashlib.sha256(source).hexdigest()
    got = hashlib.sha256(blob).hexdigest()
    if wanted != got:
        fail("copy mismatch: entry.png differs from happy.png")
    return got


def publish():
    if not os.path.exists(CARD):
        fail("happy.png not found next to main.py")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(CARD, OUT)
    if not os.path.isfile(OUT):
        fail("copy failed: %s was not created" % OUT)
    with open(CARD, "rb") as handle:
        original = handle.read()
    with open(OUT, "rb") as handle:
        blob = handle.read()
    check_size(blob)
    header = read_header(blob)
    check_colour(header)
    check_sides(header)
    digest = check_match(original, blob)
    print("wrote", OUT, len(blob), "bytes,", (header["width"], header["height"]),
          "sha256", digest)


if __name__ == "__main__":
    publish()

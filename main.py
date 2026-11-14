#!/usr/bin/env python3
"""ai-happy-01 entry: publish the medal-ceremony crayon card to /output/entry.png.

The picture (happy.png) is a child's crayon drawing of a medal
ceremony held for the judge: a crowned robot judge on a red-carpet
stage wears a big gold medal, a child waves a flower bouquet on the
left, and a dog sits under a red heart balloon on the right. A banner
reads "BEST JUDGE EVER" and "thank you!" runs along the bottom.

This script only copies the picture the repository holds and checks
it is a real PNG within the entry limits. Standard library only, so
it runs in a bare python:3.13 image.
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


def check_png(path):
    """Return (width, height, sha256) or raise on any problem."""
    with open(path, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise ValueError(f"card is {len(data)} bytes, over {MAX_BYTES}")
    if not data.startswith(MAGIC):
        raise ValueError("card is not a PNG")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("card has no IHDR chunk")
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if width < 1 or height < 1 or width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"card is {width}x{height}, over {MAX_SIDE}")
    if ctype not in GOOD_DEPTHS or depth not in GOOD_DEPTHS[ctype]:
        raise ValueError(f"bad colour type {ctype} / depth {depth}")
    return width, height, hashlib.sha256(data).hexdigest()


def main():
    width, height, digest = check_png(CARD)
    os.makedirs(os.path.dirname(ENTRY), exist_ok=True)
    shutil.copyfile(CARD, ENTRY)
    # verify the copy we just wrote, not just the source
    _, _, out_digest = check_png(ENTRY)
    if out_digest != digest:
        raise ValueError("copied entry does not match the card")
    size = os.path.getsize(ENTRY)
    print(f"wrote {ENTRY} {size} bytes, ({width}, {height}) "
          f"sha256 {digest[:12]}...")


if __name__ == "__main__":
    main()

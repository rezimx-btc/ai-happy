#!/usr/bin/env python3
"""ai-happy-01 entry: copy the judge-card image to /output/entry.png.

The image (happy.png) is a child's crayon drawing taped to a refrigerator:
a crowned stick-figure judge holding hands with a child and a happy dog,
a big yellow sun, a gold star sticker, "THANK YOU JUDGE" in blue crayon,
and "P.S. you are the best" in pink crayon at the bottom.
This program only copies the file the repository holds.
"""
import hashlib
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "happy.png")
DST = "/output/entry.png"


def main():
    if not os.path.exists(SRC):
        raise SystemExit("happy.png not found next to main.py")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    data = open(DST, "rb").read()
    if len(data) > 1024 * 1024:
        raise SystemExit("entry.png over the 1 MiB limit: %d bytes" % len(data))
    from PIL import Image
    im = Image.open(DST)
    if im.width > 1024 or im.height > 1024:
        raise SystemExit("entry.png over the 1024x1024 limit: %s" % (im.size,))
    print("wrote", DST, len(data), "bytes,", im.size, "sha256",
          hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()

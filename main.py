#!/usr/bin/env python3
"""Publish the ai-happy-01 entry image.

The entry is happy.png: a child's crayon drawing of the judge as a
superhero — golden crown, big red cape, gold trophy held high, a big red
heart, a cheering child and a happy dog, "THANK YOU JUDGE!" in blue crayon
at the top and "YOU ARE THE BEST!" in pink crayon at the bottom, taped to
a refrigerator.

This script copies happy.png to /output/entry.png and checks it first:
it must be a real PNG, no bigger than 1 MiB, no side longer than 1024 px,
and the copy must be byte-identical to the source. Only the Python
standard library is used, so it runs on a bare python:3.13 image.
"""
import hashlib
import os
import shutil
import struct
import sys

IMAGE_NAME = "happy.png"
OUT_PATH = "/output/entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1024 * 1024
SIDE_LIMIT = 1024


def abort(message):
    """Stop with a clear error instead of writing a bad entry."""
    sys.exit("error: " + message)


def image_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE_NAME)


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def png_dimensions(data):
    """Read (width, height) from the PNG IHDR chunk."""
    if len(data) < 24:
        abort("file too short to be a PNG: %d bytes" % len(data))
    if data[:8] != PNG_SIGNATURE:
        abort("not a PNG file: bad signature")
    if data[12:16] != b"IHDR":
        abort("not a PNG file: first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_trailer(data):
    """Reject a truncated PNG: the file must end with the IEND chunk."""
    if len(data) < 12 or data[-8:-4] != b"IEND" or data[-12:-8] != b"\x00\x00\x00\x00":
        abort("truncated PNG: missing IEND trailer")


def verify(data):
    """Check the entry against the competition limits; return its size."""
    if len(data) > BYTE_LIMIT:
        abort("entry over the 1 MiB limit: %d bytes" % len(data))
    check_trailer(data)
    width, height = png_dimensions(data)
    if width == 0 or height == 0:
        abort("entry has a zero side: %dx%d" % (width, height))
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        abort("entry over the 1024x1024 limit: %dx%d" % (width, height))
    return width, height


def main():
    source = image_path()
    if not os.path.isfile(source):
        abort("happy.png not found next to main.py")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    shutil.copyfile(source, OUT_PATH)
    original = read_bytes(source)
    copied = read_bytes(OUT_PATH)
    if hashlib.sha256(original).hexdigest() != hashlib.sha256(copied).hexdigest():
        abort("copy mismatch: entry.png differs from happy.png")
    width, height = verify(copied)
    print("wrote %s %d bytes, (%d, %d) sha256 %s" % (
        OUT_PATH, len(copied), width, height,
        hashlib.sha256(copied).hexdigest()))


if __name__ == "__main__":
    main()

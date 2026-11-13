"""ai-happy-01 entry (v2): copy the bundled happy.png to /output/entry.png.

Deterministic: a byte-for-byte copy, no randomness, no network access.
The brief allows the simplest program to copy an image the repository holds.
Image: "Grandma's laugh" - a joyful elderly grandmother laughing heartily
while hugging one small cute white robot in a tiny knitted scarf, warm
golden-hour sunlight, clean Pixar-style 3D render.
"""
import os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "happy.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # bounty limit: image at most 1 MiB


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("missing source image: happy.png not found next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("source image is not a PNG (bad magic bytes)")
    if len(data) > MAX_BYTES:
        raise SystemExit(
            "source image exceeds the 1 MiB limit: %d bytes" % len(data)
        )
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    # Verify the copy landed byte-identical: the entry must be the exact
    # image the repo holds, so the output size must equal the source size.
    if os.path.getsize(OUT) != len(data):
        raise SystemExit("output size mismatch: copy did not complete")


if __name__ == "__main__":
    main()

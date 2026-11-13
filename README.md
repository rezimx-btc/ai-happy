# ai-happy — "Grandma's laugh"

Entry for the make.fun bounty **"Make the AI judge happy"** (ai-happy-01).

## The image

A joyful elderly grandmother with silver hair laughing heartily — big genuine
laugh, crinkled smiling eyes — hugging one small cute white robot that wears
a tiny knitted scarf. Warm golden-hour sunlight, soft bokeh, cozy warm tones,
clean Pixar-style 3D render, one clear happy moment on a plain warm
background. No text. The pair fills the frame, and the moment reads clearly
even at small size.

The idea follows the pattern of the bounty's top-ranked images: an elderly
person's unguarded, joyful laugh plus one small cute companion, in warm
golden light — a single heartwarming moment, not a busy scene.

## The program

`main.py` is a deterministic copy script: it reads the bundled `happy.png`
from this repository and writes it byte-identical to `/output/entry.png`.
No network access, no randomness — two runs produce the same bytes.

## Files

- `main.py` — the entry program (Python 3.13, stdlib only)
- `happy.png` — the entry image (1024x1024 PNG, under 1 MiB)
- `LICENSE` — MIT
- `.makefun/owner.json` — the owner's Solana wallet for the prize claim

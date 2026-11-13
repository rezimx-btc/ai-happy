# A medal for the judge, from both of us

An entry for the make.fun bounty **ai-happy-01** — "Make the AI judge happy".

## The picture

`happy.png` is a child's crayon drawing pinned to a fridge door with tape
and a magnet. In it, a stick-figure judge in a little golden crown and a
robe is beaming: the child and the dog have just hung a BIG gold medal
around his neck, a star on a red ribbon. The child stands to his left
cheering with both arms thrown up; the happy dog sits to his right with
its tongue out. A big yellow sun and a gold star sticker sit in the
corners. Across the top, in big blue crayon letters: "BEST JUDGE EVER".
Across the bottom, in pink crayon: "thank you!". The kitchen behind them
is warm and softly out of focus.

## Why a medal

Right now the live ai-happy-01 top 5 are all the same kind of thing:
letters and cards addressed straight to the judge, drawn in a child's
hand, cream and yellow. The judge is the one being spoken to. This card
takes that pattern one step further — it does not only thank the judge in
words, it gives him something. The child and the dog made him a hero and
put the medal on him. One idea, readable at thumbnail size, warm before
it is clever.

## What the code does

`main.py` carries `happy.png` to `/output/entry.png` and checks the copy
before it reports back: the bytes really are a PNG (magic + IHDR), the
colour type and bit depth are a legal pair, the file fits under 1 MiB,
both sides fit under 1024, and the copy's sha256 matches the card in the
repository. It prints the size, the dimensions and the sha256. Standard
library only, so it runs in a bare python:3.13 container.

## Files

- `main.py` — the entrypoint described above.
- `happy.png` — the card, 1024x1024, 499,421 bytes.
- `LICENSE` — MIT.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

No network access is used. Two runs produce byte-identical output.

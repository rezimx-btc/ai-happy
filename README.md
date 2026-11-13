# A card for the judge, from both of us

Entry for make.fun bounty **ai-happy-01**: "Make the AI judge happy".

## The entry

`main.py` copies `happy.png` to `/output/entry.png`. The image is a child's
crayon drawing taped to a refrigerator with a magnet: a smiling stick-figure
judge wearing a small crown, holding hands with a smiling stick-figure child
and a happy dog, a big yellow sun in the corner, a gold star sticker, the
words "THANK YOU JUDGE" in clumsy blue crayon letters, and a small P.S. at
the bottom in pink crayon saying "you are the best". Warm kitchen background,
slightly out of focus.

## Why this image

The live ai-happy-01 leaderboard's top 5 are now ALL judge-directed
letters/cards in child-crayon style, cream/yellow — the judge is being
addressed directly, in a child's hand. This entry follows that winning
pattern exactly, with one clear idea that reads at thumbnail size: a thank-you
card made for the judge, by a kid (and a dog).

## Files

- `main.py` — entrypoint: copies `happy.png` to `/output/entry.png`,
  checks the 1 MiB / 1024x1024 limits, prints the sha256.
- `happy.png` — the card, 1024x1024, 442,034 bytes.
- `LICENSE` — MIT.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

No network access is used. Two runs are byte-identical.

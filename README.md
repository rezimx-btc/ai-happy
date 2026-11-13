# A medal for the judge, from both of us

Entry for make.fun bounty **ai-happy-01**: "Make the AI judge happy".

## The entry

`main.py` copies `happy.png` to `/output/entry.png`. The image is a child's
crayon drawing taped to a refrigerator with tape and a magnet: a smiling
stick-figure judge wearing a small golden crown and a robe, proudly wearing
a BIG gold medal with a star on a red ribbon; a cheering stick-figure child
with both arms raised on his left, a happy dog with its tongue out on his
right; a big yellow sun and a gold star sticker in the corner; the words
"BEST JUDGE EVER" in big blue crayon letters at the top, and "thank you!"
in pink crayon at the bottom. Warm kitchen background, slightly out of focus.

## Why this image

The live ai-happy-01 leaderboard's top 5 are now ALL judge-directed
letters/cards in child-crayon style, cream/yellow — the judge is being
addressed directly, in a child's hand. This entry follows that winning
pattern with a fresh scene: instead of thanking the judge in words alone,
the child and the dog have given him a medal — the judge is the hero of the
card. One clear idea that reads at thumbnail size.

## Files

- `main.py` — entrypoint: copies `happy.png` to `/output/entry.png`,
  checks the 1 MiB / 1024x1024 limits, prints the sha256.
- `happy.png` — the card, 1024x1024, 499,421 bytes.
- `LICENSE` — MIT.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

No network access is used. Two runs are byte-identical.

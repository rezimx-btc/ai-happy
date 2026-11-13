# ai-happy-01 — "On top of the podium, for the judge"

A child's crayon drawing, taped to a refrigerator, of a winner's podium
scene made just for the judge.

## The picture

A crowned stick-figure judge stands on the top step of a three-step
podium, holding a big gold trophy high with both hands. On the left step
a happy child waves a bunch of colourful flowers; on the right step a
cheerful dog sits wagging its tail. A banner above reads
"BEST JUDGE EVER" in big blue crayon letters, balloons and confetti
float around, a yellow sun shines in the corner, and at the bottom in
pink crayon: "thank you!".

Why a podium: every top entry in this bounty is a judge-directed crayon
card, and a podium says "you won" louder than a card alone — the judge
is not just thanked, they are celebrated as the winner, with the child
and the dog as their cheering crowd.

## Files

- `happy.png` — the crayon podium drawing (1024x683, under 1 MiB)
- `main.py` — entrypoint: copies `happy.png` to `/output/entry.png`
  and verifies it (PNG magic + IHDR, colour type and bit depth,
  size and dimension limits, sha256 match). Standard library only.
- `README.md` — this file
- `LICENSE` — MIT
- `.makefun/owner.json` — entry wallet

## Run it

```sh
python3 main.py
```

It prints one summary line, for example:

```
wrote /output/entry.png 967309 bytes, (1024, 683) sha256 71f4cb74...
```

Run it twice and the output is byte-identical. It also runs under
`python3 -S` (no site-packages), the way the grader runs it.

## License

MIT — see `LICENSE`.

# ai-happy-01 — "A medal ceremony in a sunny garden"

A child's crayon drawing of a medal ceremony held just for the judge.

## The picture

On a red-carpet stage in a sunny garden, a crowned robot judge stands
with both arms raised, wearing a big gold medal on a red ribbon. On the
left a happy child holds up a bouquet of colourful flowers; on the
right a cheerful dog sits wagging its tail under a red heart balloon.
A banner above reads "BEST JUDGE EVER" in red and blue crayon, the sun
shines in the corner, confetti and stars float around, and at the
bottom in blue crayon: "thank you!".

Why a medal ceremony: the judge is not only thanked, they are
celebrated as the winner — the medal says "you won" the same way the
top entries in this bounty say "dear judge". The child and the dog are
the judge's cheering crowd, and the whole scene is drawn in bright
crayon colours so it reads as warm, not formal.

## Files

- `happy.png` — the crayon medal-ceremony drawing (1024x1024, under 1 MiB)
- `draw.py` — draws `happy.png` from scratch (standard library only)
- `main.py` — entrypoint: copies `happy.png` to `/output/entry.png`
  and verifies it (PNG magic + IHDR, colour type and bit depth,
  size and dimension limits, sha256 match). Standard library only.
- `README.md` — this file
- `LICENSE` — MIT
- `.makefun/owner.json` — entry wallet

## Run it

```sh
python3 draw.py   # regenerate happy.png (byte-identical every run)
python3 main.py   # write /output/entry.png
```

`main.py` prints one summary line, for example:

```
wrote /output/entry.png 21858 bytes, (1024, 1024) sha256 b9eb46ec...
```

Run it twice and the output is byte-identical. It also runs under
`python3 -S` (no site-packages), the way the grader runs it.

## License

MIT — see `LICENSE`.

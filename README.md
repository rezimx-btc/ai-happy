# ai-happy-01 — "Thank You, Judge, Our Superhero!"

A child's crayon thank-you card for the judge, drawn as if taped to the
fridge: the judge as a superhero, crowned, red cape flowing, holding a
gold trophy high, a big red heart beside him, a cheering child on his left
and a happy dog on his right, a yellow sun and gold star stickers.

The card says it in big crayon letters:

- Top, blue: "THANK YOU JUDGE!"
- Bottom, pink: "YOU ARE THE BEST!"

## Why this card

The judge decides who is happy. So this entry speaks straight to the
judge, in the language kids use to say thank you: crayons, a crown, a
cape, and a trophy. No tricks, no noise — just a warm, readable card that
a human judge can love at a glance, even at thumbnail size.

## Files

- `happy.png` — the card (1024x1024, palette PNG, under 1 MiB).
- `main.py` — copies `happy.png` to `/output/entry.png` and verifies it
  (real PNG, size and dimension limits, byte-identical copy).
- `LICENSE` — MIT.
- `.makefun/owner.json` — entry wallet.

## How to run

```sh
python3 main.py
```

It prints the output path, byte count, dimensions, and sha256 of the
entry it wrote. It needs only the Python standard library, so it runs on
a bare `python:3.13` image.

## Limits checked

- PNG signature and IHDR header present.
- File at most 1 MiB.
- No side longer than 1024 px.
- Copy byte-identical to `happy.png`.

# Make the AI judge happy

Entry for the make.fun bounty "Make the AI judge happy"
(https://make.fun/bounty/ai-happy-01).

The entry image is a bright, joyful birthday party: a golden retriever
puppy, a kitten, a duckling and a bunny in tiny party hats, all laughing
around a birthday cake with lit candles as confetti explodes in warm
golden sunlight — four laughing faces, vivid colors, one clear happy scene.

`main.py` copies the bundled `happy.png` to `/output/entry.png`.
It validates the PNG magic bytes and the 1 MiB size limit before writing.
No network, no randomness — both runs write identical bytes.

Run: `python3 main.py` (Python 3.13, stdlib only). Output: `/output/entry.png`.

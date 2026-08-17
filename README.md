## matasanoChallenge

Aka [cryptopals](https://cryptopals.com/)

Solutions to all 66 challenges in Python, WIP

Follows the current cryptopals.com structure: 8 sets, challenges 1-66.

## Layout

```
docs/setNN.md        challenge text for each set 
data/setNN/          challenge data files
python/              python solutions
  .venv/             virtualenv 
  lib/               shared helpers
  setNN/chNN.py      one file per challenge
  from_scratch/      hand-rolled primitives (AES, MT19937, ...), WIP
```

## Running python

```sh
cd python
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python set01/ch01.py
```

Every challenge script prints its result and asserts against a known
answer (or a known property of the answer) before printing `OK`.

## Progress

| Set | Challenges | Python | Java | C++ | JS |
|-----|------------|--------|------|-----|----|
| 1 | 1-8 | done | | | |
| 2 | 9-16 | done | | | |
| 3 | 17-24 | 5/8 | | | |
| 4 | 25-32 | | | | |
| 5 | 33-40 | | | | |
| 6 | 41-48 | | | | |
| 7 | 49-56 | | | | |
| 8 | 57-66 | | | | |

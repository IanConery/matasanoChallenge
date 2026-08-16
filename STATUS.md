<!--
PURPOSE: Handoff document. An LLM (or human) reading this file cold should
be able to pick up this project exactly where it left off, with no other
context. Keep this comment at the top and the section structure below
intact when updating; refresh the State and Next steps sections as work
progresses.
-->

# Status

## What this repo is

Solutions to all 66 challenges from [cryptopals.com](https://cryptopals.com)
(a.k.a. the matasano challenge), done **one language at a time** in this
order:

1. **Python** (in progress)
2. Java
3. C++
4. JavaScript

IMPORTANT: the site was restructured. The course is now **8 sets,
challenges 1-66 with continuous numbering**. The classic 12-set / 52-challenge
layout is obsolete — do NOT use it.

- Challenge pages: `https://cryptopals.com/sets/<S>/challenges/<N>`
- Data files: `https://cryptopals.com/static/challenge-data/<N>.txt`
  (no "ch" prefix in the filename)

## Layout

```
docs/setNN.md        challenge text per set (language-neutral source of truth;
                     set01 has titles only, set02+ have full text)
data/setNN/          challenge data files fetched from cryptopals.com
python/
  .venv/             virtualenv (gitignored)
  requirements.txt   pycryptodome
  lib/               shared helpers
  setNN/chNN.py      one file per challenge
  from_scratch/      hand-rolled primitives (see its README), WIP
java/  cpp/  js/     to be created, after python is complete
```

## Conventions (follow these for every new challenge)

- Challenge file: full verbatim challenge text in the module docstring
  (plus the URL), then constants/oracle, `solve()` or attack functions, and
  `main()` which prints the result and asserts a known answer (or a known
  property of the answer) before printing `OK`.
- Shared, reusable helpers go in `python/lib/`, not in challenge files.
- Challenges whose "server" is specified by the challenge text (oracles) get
  a **local oracle** implementing the spec, and the attack runs against it.
- Challenge text for a new set: fetch each page, copy the verbatim text into
  `docs/setNN.md` (with the set intro from `/sets/<S>`) AND into each file's
  docstring.
- Data files: fetch to `data/setNN/challenge_NN.txt` when a set starts.
- Keep the progress table in the root `README.md` in sync with this file.
- Run a challenge: `.venv/bin/python setNN/chNN.py` from `python/`
  (the sys.path shim in each file also allows running from the repo root).

## State

### Python (in progress)

| Set | Status |
|-----|--------|
| 1 (ch01-08) | ch01-ch07 done, all pass; **ch08 pending** |
| 2 (ch09-16) | done, all pass |
| 3 (ch17-24) | not started |
| 4 (ch25-32) | not started |
| 5 (ch33-40) | not started |
| 6 (ch41-48) | not started |
| 7 (ch49-56) | not started |
| 8 (ch57-66) | not started (ECC; the hard set — site calls it "1% of SageMath") |

Libraries built so far (`python/lib/`):

- `crypto.py`: hex/b64, `xor_bytes`, single/repeating-key XOR,
  `hamming_distance`, `guess_key_size`, `score_english`, `pkcs7_pad/unpad`,
  `detect_ecb`
- `aes.py`: `aes_ecb_encrypt/decrypt`, **hand-rolled** CBC
  (`aes_cbc_encrypt/decrypt` — challenge 10 forbids library CBC; only the
  ECB core uses pycryptodome)
- `attacks.py`: `ecb_byte_at_a_time` (shared by ch12 and ch14; read its
  module docstring before modifying)

### Java / C++ / JavaScript

Not started. Old Java experiments were deleted by the user; start fresh.
No JDK or Maven is installed on this machine (and there is no passwordless
sudo) — the Java phase needs a user-local JDK install (e.g. Temurin 21
tarball under `~/.local`) or the user installing one first. C++ will use
CMake + OpenSSL; JS will use Node (v26 available) with no dependencies
(`node:crypto`, `node:fs`).

## Next steps (in order)

1. **`python/set01/ch08.py`** — Detect AES in ECB mode. Data is already at
   `data/set01/challenge_08.txt` (204 hex lines; one line is ECB). Detect by
   duplicate 16-byte blocks within a line (`crypto.detect_ecb` on each
   hex-decoded line).
2. **Set 3 (ch17-24)**: CBC padding oracle, CTR mode, break fixed-nonce CTR
   (substitutions + statistical), MT19937 x4 (implement, crack seed, clone,
   stream cipher). Fetch pages `/sets/3/challenges/17..24` + any data files,
   write `docs/set03.md`, add CTR to `lib/aes.py`, put the MT19937
   implementation in `lib/` so ch22-24 can import it.
3. Sets 4-8, same pattern. Set 4 needs SHA-1/MD4 cores with settable
   initial state (length extension) — good candidates for `from_scratch/`.
   Sets 9-10-era RSA and DSA are pure big-int Python (no library).
4. After all 66 in Python: java/, then cpp/, then js/, reusing the same
   per-set pattern and the shared `data/` + `docs/`.

## Gotchas (learned the hard way)

- **Python `bytes` does not support `^`** — use `crypto.xor_bytes`.
- **ch06**: the normalized-Hamming-distance key-size heuristic picked 5; the
  true key size is 29 ("Terminator X: Bring the noise", Ice Ice Baby lyrics).
  Always verify key-size candidates by full decryption + plaintext scoring.
- **Byte-at-a-time** (ch12/ch14): the candidate byte must land on a block
  END. Real input = `A^k` only; fake input = `A^k + recovered + c`; the
  correct `c` is the argmax of the first-differing-block index (wrong `c`
  corrupts block B, right `c` first differs at >= B+1). A wrong prefix
  offset degenerates to an all-zero recovery — that's the discriminator.
  Full explanation in `lib/attacks.py`.
- **Block-size detection with PKCS#7 padding**: ciphertext length is flat
  between block boundaries; find the first non-zero length delta.
- **Cut-and-paste (ch13)**: the byte math is exact — `email2` must be 13
  chars ("foo@bar.commm") so the profile's first 32 bytes end with `role=`
  (`&uid=10&role=` is 13 bytes), and `email1` puts `admin` at byte 16 with
  `0x0b * 11` filler that doubles as valid PKCS#7 padding for the forged
  ciphertext.
- **ch14**: the random prefix is generated ONCE per oracle instance (fixed
  for the attack's duration), random count 1-32 bytes.
- **ch04**: the winning line decodes to "Now that the party is jumping\n"
  (trailing newline is part of the 60 bytes).
- **ch10 data file** decrypts to Ice Ice Baby with PKCS#7 padding
  (YELLOW SUBMARINE, IV = 16 zero bytes).

## Verification

Every challenge script asserts its known answer and prints `OK`. Run them
all:

```sh
cd python
for f in setNN/chNN.py; do ./.venv/bin/python "$f" | tail -1; done
```

Expected: one `OK` per line, 15 lines currently (ch01-07, ch09-16).

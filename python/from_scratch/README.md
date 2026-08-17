# From scratch

Hand-rolled implementations of crypto primitives, without library help.

Purpose: the main solutions use pycryptodome for speed of progress. This
directory collects from-scratch versions of the primitives as we encounter
them, so the implementations exist in this repo.

Planned, in roughly this order:

- [ ] AES-128 (ECB) — needed conceptually from Set 1 ch07
- [ ] PKCS#7 is already trivial in lib
- [x] MT19937 Mersenne Twister — done in `lib/mt19937.py` (ch 21-24 import it from there)
- [ ] SHA-1 / MD4 / MD5 cores (with settable initial state) — Set 4 length extension
- [ ] DH / RSA / DSA are pure Python big-int math, no library needed
- [ ] Curve arithmetic for Set 8 (ECC)

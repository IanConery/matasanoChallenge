"""Challenge 20: Break fixed-nonce CTR statistically

In the data/set03/challenge_20.txt file find a similar set of Base64'd
plaintext. Do with them exactly what you did with the first, but solve the
problem differently.

Instead of making spot guesses at to known plaintext, treat the collection
of ciphertexts the same way you would repeating-key XOR.

Obviously, CTR encryption appears different from repeated-key XOR, but with
a fixed nonce they are effectively the same thing.

To exploit this: take your collection of ciphertexts and truncate them to a
common length (the length of the smallest ciphertext will work).

Solve the resulting concatenation of ciphertexts as if for repeating-key
XOR, with a key size of the length of the ciphertext you XOR'd.

https://cryptopals.com/sets/3/challenges/20
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, crypto, stream_break

DATA = Path(__file__).resolve().parents[2] / "data" / "set03" / "challenge_20.txt"


def break_statistical(ciphertexts: list[bytes]) -> list[bytes]:
    """Truncate to the shortest ciphertext and break the result as
    repeating-key XOR with key size = that length: transpose into columns
    (one byte from each line), break each column, and undo the transposition.
    Context/case/word refinement resolves the columns frequency alone leaves
    ambiguous (the line-start capitals)."""
    min_len = min(len(ct) for ct in ciphertexts)
    truncated = [ct[:min_len] for ct in ciphertexts]

    keystream = bytearray(min_len)
    for j in range(min_len):
        column = bytes(ct[j] for ct in truncated)
        keystream[j] = max(range(256), key=lambda g: stream_break.column_letter_score(column, g))
    stream_break.refine_keystream(truncated, keystream)

    return [crypto.xor_bytes(ct, keystream) for ct in truncated]


def main() -> None:
    lines = [ln for ln in DATA.read_text().splitlines() if ln.strip()]
    plaintexts = [crypto.b64_decode(ln) for ln in lines]
    key = os.urandom(16)
    ciphertexts = [aes.aes_ctr_encrypt(key, 0, pt) for pt in plaintexts]

    recovered = break_statistical(ciphertexts)
    for pt in recovered:
        print(pt.decode())

    expected = [pt[: len(recovered[0])] for pt in plaintexts]
    assert recovered == expected
    print("OK")


if __name__ == "__main__":
    main()

"""Challenge 11: An ECB/CBC detection oracle

Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a
function that generates a random key and encrypts under it.

The function should look like:

    encryption_oracle(your-input)
    => [MEANINGLESS JIBBER JABBER]

Under the hood, have the function append 5-10 bytes (count chosen randomly)
before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under
CBC the other half (just use random IVs each time for CBC). Use rand(2) to
decide which to use.

Detect the block cipher mode the function is using each time. You should end
up with a piece of code that, pointed at a block box that might be encrypting
ECB or CBC, tells you which one is happening.

https://cryptopals.com/sets/2/challenges/11
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, crypto


def encryption_oracle(data: bytes, reveal_mode: bool = False):
    """Encrypt data under a fresh random key in ECB or CBC (50/50)."""
    key = os.urandom(16)
    prefix = os.urandom(random.randint(5, 10))
    suffix = os.urandom(random.randint(5, 10))
    plaintext = crypto.pkcs7_pad(prefix + data + suffix)

    if random.randrange(2) == 0:
        ciphertext = aes.aes_ecb_encrypt(key, plaintext)
        mode = "ECB"
    else:
        ciphertext = aes.aes_cbc_encrypt(key, os.urandom(16), plaintext)
        mode = "CBC"

    return (ciphertext, mode) if reveal_mode else ciphertext


def detect_mode(ciphertext: bytes) -> str:
    """Duplicate 16-byte blocks can only occur in ECB (deterministic blocks)."""
    return "ECB" if crypto.detect_ecb(ciphertext) else "CBC"


def main() -> None:
    # A long run of identical bytes guarantees duplicate plaintext blocks
    # (hence duplicate ciphertext blocks) whenever the mode is ECB.
    message = b"A" * 56
    trials = 20
    for i in range(trials):
        ciphertext, mode = encryption_oracle(message, reveal_mode=True)
        guess = detect_mode(ciphertext)
        print(f"trial {i + 1:2d}: oracle={mode}  detected={guess}")
        assert guess == mode

    print("OK")


if __name__ == "__main__":
    main()

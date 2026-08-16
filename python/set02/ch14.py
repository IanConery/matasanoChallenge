"""Challenge 14: Byte-at-a-time ECB decryption (Harder)

Take your oracle function from #12.

Now generate a random count of random bytes and prepend this string to every
plaintext. You are now doing:

    AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

Same goal: decrypt the target-bytes.

Stop and think for a second.

What's harder than challenge #12 about doing this? How would you overcome
that obstacle?

The hint is: you're using all the tools you already have; no crazy math is
required. Think "STIMULUS" and "RESPONSE".

https://cryptopals.com/sets/2/challenges/14
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, attacks, crypto

HIDDEN_B64 = (
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
    "YnkK"
)

ORACLE_KEY = os.urandom(16)
PREFIX = os.urandom(random.randint(1, 32))  # fixed per oracle instance
TARGET = crypto.b64_decode(HIDDEN_B64)


def oracle(data: bytes) -> bytes:
    return aes.aes_ecb_encrypt(ORACLE_KEY, crypto.pkcs7_pad(PREFIX + data + TARGET))


def main() -> None:
    # The obstacle: the prefix length is unknown, so the attacker input
    # starts at an unknown offset within its block. STIMULUS/RESPONSE:
    # vary the input and read the response length to see where the block
    # boundaries fall, then simply try every candidate offset. A wrong
    # offset recovers the first target byte at every step (the candidate
    # always lands on the same position), so the true offset is the one
    # whose recovery is not a constant byte.
    total = len(oracle(b""))
    print(f"oracle response length for empty input: {total}")

    recovered_map = attacks.ecb_byte_at_a_time(oracle, len(TARGET), range(16))
    winners = [rec for rec in recovered_map.values() if len(set(rec)) > 1]
    assert len(winners) == 1, f"ambiguous recovery: {len(winners)} candidates"
    recovered = winners[0]
    print(recovered.decode())
    assert recovered == TARGET
    print("OK")


if __name__ == "__main__":
    main()

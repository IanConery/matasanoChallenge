"""Challenge 12: Byte-at-a-time ECB decryption (Simple)

Copy your oracle function to a new function that encrypts buffers under ECB
mode using a consistent but unknown key (for instance, assign a single
random key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE
ENCRYPTING, the following string:

    Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
    aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
    dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
    YnkK

Spoiler alert. Do not decode this string now. Don't do it. Base64 decode the
string before appending it. Do not base64 decode the string by hand; make
your code do it. The point is that you don't know its contents.

What you have now is a function that produces:

    AES-128-ECB(your-string || unknown-string, random-key)

It turns out: you can decrypt "unknown-string" with repeated calls to the
oracle function!

Here's roughly how:

1. Feed identical bytes of your-string to the function 1 at a time --- start
   with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block
   size of the cipher. You know it, but do this step anyway.
2. Detect that the function is using ECB. You already know, but do this step
   anyways.
3. Knowing the block size, craft an input block that is exactly 1 byte short
   (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about
   what the oracle function is going to put in that last byte position.
4. Make a dictionary of every possible last byte by feeding different strings
   to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC",
   remembering the first block of each invocation.
5. Match the output of the one-byte-short input to one of the entries in your
   dictionary. You've now discovered the first byte of unknown-string.
6. Repeat for the next byte.

Congratulations.

This is the first challenge we've given you whose solution will break real
crypto. Lots of people know that when you encrypt something in ECB mode, you
can see penguins through it. Not so many of them can decrypt the contents of
those ciphertexts, and now you can. If our experience is any guideline, this
attack will get you code execution in security tests about once a year.

https://cryptopals.com/sets/2/challenges/12
"""

import os
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

ORACLE_KEY = os.urandom(16)  # consistent but unknown
HIDDEN = crypto.b64_decode(HIDDEN_B64)  # code decodes it; we don't


def oracle(data: bytes) -> bytes:
    return aes.aes_ecb_encrypt(ORACLE_KEY, crypto.pkcs7_pad(data + HIDDEN))


def main() -> None:
    # 1. Discover the block size. The oracle pads, so the ciphertext length
    # is flat between block boundaries and jumps by exactly the block size
    # when a boundary is crossed.
    lengths = [len(oracle(b"A" * n)) for n in range(0, 33)]
    block_size = next(b for b in (lengths[n] - lengths[n - 1] for n in range(1, 33)) if b)
    print(f"block size: {block_size}")
    assert block_size == 16

    # 2. Confirm ECB.
    assert crypto.detect_ecb(oracle(b"A" * 56))
    print("mode: ECB")

    # 3-6. Byte-at-a-time recovery (no prefix in this oracle: offset 0).
    (recovered,) = attacks.ecb_byte_at_a_time(oracle, len(HIDDEN), (0,)).values()
    print(recovered.decode())
    assert recovered == HIDDEN
    print("OK")


if __name__ == "__main__":
    main()

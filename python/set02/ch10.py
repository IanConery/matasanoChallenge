"""Challenge 10: Implement CBC mode

CBC mode is a block cipher mode that allows us to encrypt irregularly-sized
messages, despite the fact that a block cipher natively only transforms
individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block
before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext
block, is added to a "fake 0th ciphertext block" called the initialization
vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier,
making it encrypt instead of decrypt (verify this by decrypting whatever you
encrypt to test), and using your XOR function from the previous exercise to
combine them.

The file here is intelligible (somewhat) when CBC decrypted against "YELLOW
SUBMARINE" with an IV of all ASCII 0 (\\x00\\x00\\x00 &c).

Don't cheat. Do not use OpenSSL's CBC code to do CBC mode, even to verify
your results. What's the point of even doing this stuff if you aren't going
to learn from it?

https://cryptopals.com/sets/2/challenges/10
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, crypto

KEY = b"YELLOW SUBMARINE"
IV = b"\x00" * 16
DATA = Path(__file__).resolve().parents[2] / "data" / "set02" / "challenge_10.txt"


def main() -> None:
    # ECB core now encrypts: verify by decrypting whatever we encrypt.
    sample = b"YELLOW SUBMARINE"
    assert aes.aes_ecb_decrypt(KEY, aes.aes_ecb_encrypt(KEY, sample)) == sample

    # Hand-rolled CBC round-trip.
    message = crypto.pkcs7_pad(b"The quick brown fox jumps over the lazy dog.")
    iv = os.urandom(16)
    ct = aes.aes_cbc_encrypt(KEY, iv, message)
    assert ct != aes.aes_ecb_encrypt(KEY, message)
    assert aes.aes_cbc_decrypt(KEY, iv, ct) == message

    # Decrypt the provided file.
    ciphertext = crypto.b64_decode(DATA.read_text())
    plaintext = aes.aes_cbc_decrypt(KEY, IV, ciphertext)
    unpadded = crypto.pkcs7_unpad(plaintext)
    print(unpadded.decode())
    assert unpadded.startswith(b"I'm back and I'm ringin' the bell")
    assert "Play that funky music" in unpadded.decode()
    print("OK")


if __name__ == "__main__":
    main()

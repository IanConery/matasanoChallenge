"""Challenge 16: CBC bitflipping attacks

Generate a random AES key.

Combine your padding code and CBC code to write two functions.

The first function should take an arbitrary input string, prepend the string:

    "comment1=cooking%20MCs;userdata="

.. and append the string:

    ";comment2=%20like%20a%20pound%20of%20bacon"

The function should quote out the ";" and "=" characters.

The function should then pad out the input to the 16-byte AES block length
and encrypt it under the random AES key.

The second function should decrypt the string and look for the characters
";admin=true;" (or, equivalently, decrypt, split the string on ";", convert
each resulting string into 2-tuples, and look for the "admin" tuple).

Return true or false based on whether the string exists.

If you've written the first function properly, it should not be possible to
provide user input to it that will generate the string the second function is
looking for. We'll have to break the crypto to do that.

Instead, modify the ciphertext (without knowledge of the AES key) to
accomplish this.

You're relying on the fact that in CBC mode, a 1-bit error in a ciphertext
block:

- Completely scrambles the block the error occurs in
- Produces the identical 1-bit error in the next ciphertext block

Stop and think for a second.

Before you implement this attack, answer this question: why does CBC mode
have this property?

Because P_i = ECB_dec(C_i) XOR C_{i-1}: C_{i-1} is XORed into the next
plaintext block after decryption, so changing it changes exactly those bits
of P_i.

https://cryptopals.com/sets/2/challenges/16
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, crypto

KEY = os.urandom(16)
IV = os.urandom(16)
PREFIX = b"comment1=cooking%20MCs;userdata="  # exactly 32 bytes
SUFFIX = b";comment2=%20like%20a%20pound%20of%20bacon"


def profile_for(userdata: str) -> bytes:
    safe = userdata.replace(";", "%3B").replace("=", "%3D")
    plaintext = PREFIX + safe.encode() + SUFFIX
    return aes.aes_cbc_encrypt(KEY, IV, crypto.pkcs7_pad(plaintext))


def profile_is_admin(ciphertext: bytes) -> bool:
    plaintext = aes.aes_cbc_decrypt(KEY, IV, ciphertext)
    return b";admin=true;" in plaintext


def main() -> None:
    # A proper profile_for cannot be talked into emitting ;admin=true;
    for attempt in (";admin=true;", "admin=true", "%3Badmin%3Dtrue%3B"):
        assert not profile_is_admin(profile_for(attempt)), attempt
    print("no user input can produce ;admin=true; directly")

    # Bitflip attack:
    # With a 2-byte input, block 1 is exactly PREFIX[16:] + input and block
    # 2 is the start of SUFFIX. In CBC, P_2 = ECB_dec(C_2) XOR C_1, so
    # overwriting C_1 with ECB_dec(C_2) XOR target makes P_2 decrypt to
    # exactly the target block, while P_1 is scrambled (harmless).
    target_block = b"AAAA;admin=true;"
    assert len(PREFIX) == 32 and len(target_block) == 16

    ct = profile_for("AA")
    assert not profile_is_admin(ct)

    c2 = ct[32:48]
    c1_forced = crypto.xor_bytes(aes.aes_ecb_decrypt(KEY, c2), target_block)
    forged = ct[:16] + c1_forced + ct[32:]

    assert profile_is_admin(forged)
    print("forged profile is admin:", profile_is_admin(forged))
    print(aes.aes_cbc_decrypt(KEY, IV, forged).decode(errors="replace"))
    print("OK")


if __name__ == "__main__":
    main()

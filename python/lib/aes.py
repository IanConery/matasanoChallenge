"""AES-128 ECB, hand-rolled CBC (per challenge 10: no library CBC), and
hand-rolled CTR (challenge 18's format: 64-bit LE nonce, 64-bit LE count)."""

from Crypto.Cipher import AES

from .crypto import xor_bytes


def aes_ecb_encrypt(key: bytes, data: bytes) -> bytes:
    if len(key) != 16:
        raise ValueError("key must be 16 bytes")
    if len(data) % 16:
        raise ValueError("data must be a multiple of the block size")
    return AES.new(key, AES.MODE_ECB).encrypt(data)


def aes_ecb_decrypt(key: bytes, data: bytes) -> bytes:
    if len(key) != 16:
        raise ValueError("key must be 16 bytes")
    if len(data) % 16:
        raise ValueError("data must be a multiple of the block size")
    return AES.new(key, AES.MODE_ECB).decrypt(data)


def _chain(encrypt: bool, key: bytes, iv: bytes, data: bytes) -> bytes:
    if len(iv) != 16:
        raise ValueError("iv must be 16 bytes")
    if len(data) % 16:
        raise ValueError("data must be a multiple of the block size")
    core = aes_ecb_encrypt if encrypt else aes_ecb_decrypt
    out = b""
    prev = iv
    for i in range(0, len(data), 16):
        block = data[i : i + 16]
        if encrypt:
            out += core(key, xor_bytes(block, prev))
            prev = out[-16:]
        else:
            out += xor_bytes(core(key, block), prev)
            prev = block
    return out


def aes_cbc_encrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    """CBC by hand: C_i = ECB_enc(P_i XOR C_{i-1}), C_{-1} = IV."""
    return _chain(True, key, iv, data)


def aes_cbc_decrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    """CBC by hand: P_i = ECB_dec(C_i) XOR C_{i-1}, C_{i-1} = IV."""
    return _chain(False, key, iv, data)


def _ctr_keystream(key: bytes, nonce: int, count: int, length: int) -> bytes:
    out = b""
    i = count
    while len(out) < length:
        block = nonce.to_bytes(8, "little") + i.to_bytes(8, "little")
        out += aes_ecb_encrypt(key, block)
        i += 1
    return out[:length]


def aes_ctr_encrypt(key: bytes, nonce: int, data: bytes, count: int = 0) -> bytes:
    """CTR mode: XOR data against AES-ECB(key, LE64(nonce) || LE64(count))."""
    if len(key) != 16:
        raise ValueError("key must be 16 bytes")
    if not 0 <= nonce < 2**64:
        raise ValueError("nonce must fit in 64 bits")
    return xor_bytes(data, _ctr_keystream(key, nonce, count, len(data)))


def aes_ctr_decrypt(key: bytes, nonce: int, data: bytes, count: int = 0) -> bytes:
    """CTR decryption is identical to encryption."""
    return aes_ctr_encrypt(key, nonce, data, count)

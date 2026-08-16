"""Shared helpers for the Cryptopals challenges."""

import base64
from collections import Counter


def hex_to_bytes(h: str) -> bytes:
    return bytes.fromhex(h.strip())


def bytes_to_hex(b: bytes) -> str:
    return b.hex()


def b64_encode(b: bytes) -> str:
    return base64.b64encode(b).decode()


def b64_decode(s: str) -> bytes:
    return base64.b64decode(s.strip())


def xor_bytes(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("buffers must be equal length")
    return bytes(x ^ y for x, y in zip(a, b))


def single_byte_xor(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)


def repeating_key_xor(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("key must be non-empty")
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def hamming_distance(a: bytes, b: bytes) -> int:
    if len(a) != len(b):
        raise ValueError("buffers must be equal length")
    return bin(int.from_bytes(xor_bytes(a, b), "big")).count("1")


def guess_key_size(data: bytes, min_size: int = 2, max_size: int = 40) -> int:
    """Smallest normalized Hamming distance over the first two key-sized blocks."""
    best_size, best_ratio = min_size, float("inf")
    for size in range(min_size, max_size + 1):
        ratio = hamming_distance(data[:size], data[size : 2 * size]) / size
        if ratio < best_ratio:
            best_size, best_ratio = size, ratio
    return best_size


_FREQ = {
    " ": 18.0, "e": 12.7, "t": 9.1, "a": 8.2, "o": 7.5, "i": 7.0,
    "n": 6.7, "s": 6.3, "h": 6.1, "r": 6.0, "d": 4.3, "l": 4.0,
    "c": 2.8, "u": 2.8, "m": 2.4, "w": 2.4, "f": 2.2, "g": 2.0,
    "y": 2.0, "p": 1.9, "b": 1.5, "v": 1.0, "k": 0.8, "j": 0.15,
    "x": 0.15, "q": 0.1, "z": 0.07,
}
ENGLISH_FREQ = {ord(c): f for c, f in _FREQ.items()}


def score_english(data: bytes) -> float:
    """Higher = more likely English. Letter-frequency based, normalized by length."""
    if not data:
        return 0.0
    freq = Counter(data.lower())
    score = sum(ENGLISH_FREQ.get(b, -1.0) * n for b, n in freq.items())
    return score / len(data)


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    if not 1 <= block_size <= 255:
        raise ValueError("block_size out of range")
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    if not data or len(data) % block_size:
        raise ValueError("invalid padding: bad length")
    pad_len = data[-1]
    if not 1 <= pad_len <= block_size or data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("invalid padding")
    return data[:-pad_len]


def detect_ecb(data: bytes, block_size: int = 16) -> bool:
    """Duplicate block detection for ECB mode."""
    if len(data) % block_size:
        return False
    blocks = [data[i : i + block_size] for i in range(0, len(data), block_size)]
    return len(blocks) != len(set(blocks))

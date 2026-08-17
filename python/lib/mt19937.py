"""Hand-rolled MT19937 Mersenne Twister (challenges 21-24).

Standard init_by_index seeding, twist, and tempering per the Wikipedia
pseudocode. Does not use Python's random module (it is itself MT19937, and
challenge 21 forbids using the language's RNG).
"""

N = 624
M = 397
MATRIX_A = 0x9908B0DF
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7FFFFFFF
WORD = 0xFFFFFFFF


class MT19937:
    def __init__(self, seed: int = 5489):
        self.state = [0] * N
        self.index = N
        self.seed_by_index(seed)

    @classmethod
    def from_state(cls, state: list[int]) -> "MT19937":
        """Build a generator whose internal state array is `state` (ch23 splicing)."""
        if len(state) != N:
            raise ValueError("state must have 624 elements")
        mt = cls.__new__(cls)
        mt.state = [s & WORD for s in state]
        mt.index = N
        return mt

    def seed_by_index(self, seed: int) -> None:
        state = self.state
        state[0] = seed & WORD
        for i in range(1, N):
            prev = state[i - 1] ^ (state[i - 1] >> 30)
            state[i] = (1812433253 * prev + i) & WORD
        self.index = N

    def generate(self) -> int:
        """Next 32-bit (tempered) output."""
        if self.index >= N:
            self._twist()
            self.index = 0
        x = self.state[self.index]
        self.index += 1
        return temper(x)

    def _twist(self) -> None:
        state = self.state
        for i in range(N):
            y = (state[i] & UPPER_MASK) | (state[(i + 1) % N] & LOWER_MASK)
            x = state[(i + M) % N] ^ (y >> 1)
            if y & 1:
                x ^= MATRIX_A
            state[i] = x & WORD


def temper(y: int) -> int:
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    y ^= y >> 18
    return y & WORD


def _undo_xshr(y: int, shift: int) -> int:
    """Invert y = x ^ (x >> shift) for 32-bit values.

    Iterates x = y ^ (x >> shift): each pass extends the correct top-bit
    prefix by `shift` bits, and the fixpoint is the exact preimage.
    """
    x = y
    for _ in range((32 + shift - 1) // shift):
        x = y ^ (x >> shift)
    return x & WORD


def _undo_xshl(y: int, shift: int, mask: int) -> int:
    """Invert y = x ^ ((x << shift) & mask) for 32-bit values."""
    x = y
    while True:
        nxt = (y ^ ((x << shift) & mask)) & WORD
        if nxt == x:
            return x
        x = nxt


def untemper(y: int) -> int:
    """Invert temper(): map an MT19937 output back to its state element."""
    y = _undo_xshr(y, 18)
    y = _undo_xshl(y, 15, 0xEFC60000)
    y = _undo_xshl(y, 7, 0x9D2C5680)
    y = _undo_xshr(y, 11)
    return y

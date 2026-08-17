"""Challenge 21: Implement the MT19937 Mersenne Twister RNG

Implement the MT19937 Mersenne Twister RNG

You can get the psuedocode for this from Wikipedia.

If you're writing in Python, Ruby, or (gah) PHP, your language is probably
already giving you MT19937 as "rand()"; don't use rand(). Write the RNG
yourself.

https://cryptopals.com/sets/3/challenges/21
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import mt19937
from lib.mt19937 import MT19937

# 32-bit outputs compared after each state splice.
SPLICE_WORDS = 1000

# Words to draw from the reference stream before each splice (relative to
# the previous splice). Chosen so the splices land at interesting
# positions: 624 (twist boundary), 623 (last state slot), 624, 1 (just
# after a twist), 500, 623, 300.
CHECKPOINT_ADVANCES = (0, 247, 249, 249, 123, 371, 549)


def check_determinism(words: int = 1000) -> None:
    """Same seed -> identical streams; different seed -> different stream."""
    def stream(seed: int) -> list[int]:
        mt = MT19937(seed)
        return [mt.generate() for _ in range(words)]

    a = stream(1234)
    b = stream(1234)
    c = stream(4321)
    assert a == b, "same seed must give the same stream"
    assert a != c, "different seeds must give different streams"


def cross_check_cpython() -> tuple[int, tuple[int, ...]]:
    """Splice CPython's C MT19937 state into the hand-rolled MT19937 and
    compare the following outputs.

    CPython seeds ints with init_by_array (not init_by_index), so bridge
    the internal state, never the seed: getstate's state tuple on 3.14 is
    625 elements (624 state words + position); hand the 624 words to
    MT19937.from_state and restore the position, then both generators must
    produce identical streams from that point on."""
    rng = random.Random()
    rng.seed(987654321)
    checked = 0
    positions = []
    for advance in CHECKPOINT_ADVANCES:
        for _ in range(advance):
            rng.getrandbits(32)
        state = rng.getstate()[1]
        if len(state) != mt19937.N + 1:
            raise AssertionError(
                f"expected 625-element getstate state (Python 3.14+), got {len(state)}"
            )
        pos = state[mt19937.N]
        mt = MT19937.from_state(list(state[:mt19937.N]))
        mt.index = pos
        positions.append(pos)
        for _ in range(SPLICE_WORDS):
            assert mt.generate() == rng.getrandbits(32), (
                f"output divergence after splice at position {pos}"
            )
            checked += 1
    return checked, tuple(positions)


def main() -> None:
    check_determinism()
    print("determinism: seed 1234 -> identical 1000-output streams (two generators); seed 4321 differs")

    mt = MT19937(5489)
    demo = [mt.generate() for _ in range(5)]
    assert demo[0] == 3499211612
    print("seed 5489 first 5 outputs: " + " ".join(map(str, demo)))

    checked, positions = cross_check_cpython()
    print(
        f"CPython C-MT cross-check: state splice at positions {positions}; "
        f"{checked}/{checked} outputs identical"
    )
    print("OK")


if __name__ == "__main__":
    main()

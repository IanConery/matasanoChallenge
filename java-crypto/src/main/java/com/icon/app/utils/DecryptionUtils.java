package utils;

import java.util.BitSet;
import java.lang.IllegalArgumentException;

public class DecryptionUtils {

  public static int calculateHammingDistance(byte[] stringOneBytes, byte[] stringTwoBytes) {
    if (stringOneBytes.length != stringTwoBytes.length) {
      throw new IllegalArgumentException("Strings must be of equal length");
    }

    int differingBits = 0;
    BitSet stringOneBits = BitSet.valueOf(stringOneBytes);
    BitSet stringTwoBits = BitSet.valueOf(stringTwoBytes);

    for (int i = 0; i < stringOneBits.length(); i++) {
      boolean bit1 = stringOneBits.get(i);
      boolean bit2 = stringTwoBits.get(i);

      if (bit1 != bit2) {
        differingBits++;
      }
    }

    return differingBits;
  }
}

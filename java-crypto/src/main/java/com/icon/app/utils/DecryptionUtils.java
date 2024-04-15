package com.icon.app.utils;

import com.icon.app.utils.HexUtils;
import java.util.BitSet;
import java.lang.IllegalArgumentException;

public class DecryptionUtils {

  // The amount of differing bits between
  // "this is a test"
  // and
  // "wokka wokka!!!"
  // is 37
  public static int calculateHammingDistance(String hexString1, String hexString2) {
    if (hexString1.length() != hexString2.length()) {
      throw new IllegalArgumentException("Strings must be of equal length");
    }
    int differingBits = 0;
    byte[] stringOneBytes = HexUtils.hexStringToBytes(hexString1);
    byte[] stringTwoBytes = HexUtils.hexStringToBytes(hexString2);

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

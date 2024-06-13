package challengeSetOne;

import utils.HexUtils;

public class ChallengeTwoMethods {

  public static String fixedXOR(String hex1, String hex2) {
    if (hex1.length() != hex2.length()) {
      throw new IllegalArgumentException("Hex strings must be equal length");
    }

    byte[] hex1Bytes = HexUtils.hexStringToBytes(hex1);
    byte[] hex2Bytes = HexUtils.hexStringToBytes(hex2);
    byte[] xorBytes = new byte[hex1Bytes.length];

    for (int i = 0; i < hex1Bytes.length; i++) {
      byte hexByte1 = hex1Bytes[i];
      byte hexByte2 = hex2Bytes[i];

      xorBytes[i] = (byte) (hexByte1 ^ hexByte2);
    }

    return HexUtils.bytesToHexString(xorBytes);
  }
}

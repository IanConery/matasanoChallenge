import manipulators.HexManipulators;

// Write a function that takes two equal-length buffers and produces their XOR combination
// given two hex encoded strings perform xor and then return hex

public class ChallengeTwo {
  public static void main(String[] args) {
    String firstHex = "1c0111001f010100061a024b53535009181c";
    String secondHex = "686974207468652062756c6c277320657965";

    System.out.println(fixedXOR(firstHex, secondHex));
    // outputs 746865206b696420646f6e277420706c6179
  }

  public static String fixedXOR(String hex1, String hex2) {
    if (hex1.length() != hex2.length()) {
      throw new IllegalArgumentException("Hex strings must be equal length");
    }

    byte[] hex1Bytes = HexManipulators.hexStringToBytes(hex1);
    byte[] hex2Bytes = HexManipulators.hexStringToBytes(hex2);
    byte[] xorBytes = new byte[hex1Bytes.length];

    for (int i = 0; i < hex1Bytes.length; i++) {
      byte hexByte1 = hex1Bytes[i];
      byte hexByte2 = hex2Bytes[i];

      xorBytes[i] = (byte) (hexByte1 ^ hexByte2);
    }

    return HexManipulators.bytesToHexString(xorBytes);
  }
}

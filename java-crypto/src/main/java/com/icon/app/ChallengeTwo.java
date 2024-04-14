import com.icon.app.utils.HexUtils;

// https://cryptopals.com/sets/1/challenges/2
// Write a function that takes two equal-length buffers and produces their XOR combination
// expected output: 746865206b696420646f6e277420706c6179

public class ChallengeTwo {

  public static final String INPUT_1 = "1c0111001f010100061a024b53535009181c";
  public static final String INPUT_2 = "686974207468652062756c6c277320657965";

  public static void main(String[] args) {
    System.out.println(HexUtils.hexToAscii(INPUT_1));
    // KSSP
    System.out.println(HexUtils.hexToAscii(INPUT_2));
    // hit the bull's eye
    System.out.println(HexUtils.hexToAscii(fixedXOR(INPUT_1, INPUT_2)));
    // the kid don't play

    System.out.println(fixedXOR(INPUT_1, INPUT_2));
    // 746865206b696420646f6e277420706c6179
  }

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

import utils.HexUtils;
import java.util.List;
import java.util.Arrays;

public class Testing extends ChallengeThree {

  private static String qbf = "The Quick Brown Fox Jumps Over The Lazy Dog";

  public static void main(String[] args) {
    String hexString = HexUtils.asciiToHex(qbf);
    String xordHex = xorByChar('-', hexString);

    System.out.println(qbf);
    System.out.println(hexString);
    System.out.println(xordHex);

    byte[] encryptedBytes = HexUtils.hexStringToBytes(xordHex);
    System.out.println(Arrays.toString(encryptedBytes));
    List<String> testThis = Testing.generateBestGuess(encryptedBytes);
    String decrypted = testThis.remove(1);
    String chused = testThis.remove(0);
    System.out.println(decrypted);
    System.out.println(chused);
  }

  public static String xorByChar(char xor, String hexString) {
    byte xorByte = (byte) xor;
    byte[] hexToBytes = HexUtils.hexStringToBytes(hexString);
    byte[] encrypted = new byte[hexToBytes.length];

    for (int i = 0; i < hexToBytes.length; i++) {
      byte xord = (byte) (hexToBytes[i] ^ xorByte);
      encrypted[i] = xord;
    }

    return HexUtils.bytesToHexString(encrypted);
  }
}

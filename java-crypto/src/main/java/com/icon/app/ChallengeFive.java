import com.icon.app.utils.HexUtils;

// https://cryptopals.com/sets/1/challenges/5
// Implement repeating key-XOR
// input:
// Burning 'em, if you ain't quick and nimble
// I go crazy when I hear a cymbal
// Expected output:
// 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
// a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

// Note: the expected output is separated onto two lines on the website - I don't think that was intentional,
// the top line wraps in the middle of the word nimble, specifically at the n

// This is assuming that you'd want to output hexidecimal only, a minor refactor would change that
public class ChallengeFive {
  private static final String ENCRYPTION_KEY = "ICE";
  private static final String PLAIN_TEXT = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal";

  public static void main(String[] args) {

    String encrypted = repeatingKeyXor(PLAIN_TEXT, ENCRYPTION_KEY);

    System.out.println("Encrypted text : " + encrypted);
    // Encrypted text : 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
  }

  public static String repeatingKeyXor(String inputString, String key) {
    final int keyLength = key.length();
    final int stringLength = inputString.length();

    String result = "";
    int startMarker = 0;
    int endMarker = keyLength;
    char[] keyChars = key.toCharArray();

    while (endMarker <= stringLength) {
      char[] stringChars = inputString.substring(startMarker, endMarker).toCharArray();

      for (int i = 0; i < keyLength; i++) {
        result += singleByteEncryptor(keyChars[i], stringChars[i]);
      }

      startMarker += keyLength;
      endMarker += keyLength;
    }

    if (startMarker < stringLength) {
      char[] stringChars = inputString.substring(startMarker).toCharArray();

      for (int i = 0; i < stringChars.length; i++) {
        result += singleByteEncryptor(keyChars[i], stringChars[i]);
      }
    }

    return result;
  }

  private static String singleByteEncryptor(char keyChar, char stringChar) {
    byte keyByte = (byte) keyChar;
    byte stringByte = (byte) stringChar;
    byte xord = (byte) (keyByte ^ stringByte);

    return HexUtils.byteToHex(xord);
  }
}

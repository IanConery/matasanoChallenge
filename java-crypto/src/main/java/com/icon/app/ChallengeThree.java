import java.util.*;
import com.icon.app.utils.HexUtils;

// https://cryptopals.com/sets/1/challenges/3
// Single-byte XOR cipher
// a hex string has been xor'd against one char, find it

public class ChallengeThree {
  public static final String ENCRYPTED_STRING = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";
  // https://en.wikipedia.org/wiki/Etaoin_shrdlu
  private static final String FREQ_LETTERS = "etaoinshrdlu";

  public static void main(String[] args) {

    Map<String, String> cypherKeyAndDecryptedString = singleByteXorCypher(ENCRYPTED_STRING);

    for (String key: cypherKeyAndDecryptedString.keySet()) {
      System.out.println(key + " : " + cypherKeyAndDecryptedString.get(key));
    }
    // Output
    // Character-Used : X
    // Decrypted-String : Cooking MC's like a pound of bacon
  }

  private static Map<String, String> singleByteXorCypher(String encryptedString) {
    int largestCount = 0;
    String largestString = "";
    char charUsedToEncode = '_';
    Map<String, String> solution = new HashMap<>();
    List<Character> alphabetList = generateAlphabetChars();

    for (char ch: alphabetList) {
      String ascii = xorStringOutputAscii(ch, encryptedString);
      int count = numberOfAlphabetChars(ascii);

      if (count > largestCount) {
        largestCount = count;
        largestString = ascii;
        charUsedToEncode = ch;
      }
    }

    solution.put("Character-Used", charUsedToEncode + "");
    solution.put("Decrypted-String", largestString);

    return solution;
  }

  // created but didn't use, keeping for use later
  private static int characterFrequencyScore(String asciiString) {
    int score = 0;
    int strLength = FREQ_LETTERS.length();
    Map<Character, Integer> count = new HashMap<>();

    for (int i = 0; i < strLength; i++) {
      char currentChar = FREQ_LETTERS.charAt(i);
      count.put(currentChar, 0);
    }

    for (int i = 0; i < asciiString.length(); i++) {
      char currentChar = asciiString.charAt(i);
      count.computeIfPresent(currentChar, (k, v) -> v++);
    }

    for (char key: count.keySet()) {
      score += count.get(key);
    }

    return score;
  }

  private static int numberOfAlphabetChars(String asciiString) {
    int count = 0;

    for (int i = 0; i < asciiString.length(); i++) {
      char currentChar = asciiString.charAt(i);
      boolean isAlphabetChar = Character.isLetter(currentChar);

      if (isAlphabetChar) {
        count++;
      }
    }

    return count;
  }

  private static String xorStringOutputAscii(char keyChar, String encrypted) {
    byte keyByte = (byte) keyChar;
    byte[] encryptedBytes = HexUtils.hexStringToBytes(encrypted);
    byte[] decryptedBytes = new byte[encryptedBytes.length];
    String hexString = "";

    for (int i = 0; i < encryptedBytes.length; i++) {
      decryptedBytes[i] = (byte) (keyByte ^ encryptedBytes[i]);
    }

    hexString = HexUtils.bytesToHexString(decryptedBytes);

    return HexUtils.hexToAscii(hexString);
  }

  private static List<Character> generateAlphabetChars() {
    List<Character> alphabetList = new ArrayList<>();

    for (char ch = 'A'; ch < 'z'; ch++) {
      boolean isAlphabetChar = Character.isLetter(ch);
      // there are special chars between Z and a, we don't want those
      if (isAlphabetChar) {
        alphabetList.add(ch);
      }
    }

    return alphabetList;
  }
}

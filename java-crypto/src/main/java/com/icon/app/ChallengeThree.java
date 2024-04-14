import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import com.icon.app.utils.HexUtils;

// https://cryptopals.com/sets/1/challenges/3
// Single-byte XOR cipher
// a hex string has been xor'd against one char, find it

public class ChallengeThree {
  private static final String ENCRYPTED_STRING = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";
  // https://en.wikipedia.org/wiki/Etaoin_shrdlu
  protected static final String FREQ_LETTERS = "EeTtAaOoIiNnSsHhRrDdLlUu ";
  protected static final Map<Character, Integer> frequencyMap = generateFreqCharMap();
  protected static final List<Character> byteChars = generateByteChars();

  public static void main(String[] args) {

    byte[] encryptedBytes = HexUtils.hexStringToBytes(ENCRYPTED_STRING);
    List<String> cypherKeyAndDecryptedString = generateBestGuess(encryptedBytes);
    String decryptedString = cypherKeyAndDecryptedString.remove(1);
    String charUsed = cypherKeyAndDecryptedString.remove(0);

    System.out.println("Character Used: " + charUsed + "\nDecrypted String: " + decryptedString);
    // Output
    // Character-Used : X
    // Decrypted-String : Cooking MC's like a pound of bacon
  }

  public static int characterFrequencyScore(String asciiString) {
    int score = 0;
    Map<Character, Integer> count = generateFreqCharMap();

    for (int i = 0; i < asciiString.length(); i++) {
      char currentChar = asciiString.charAt(i);
      if (frequencyMap.containsKey(currentChar)) {
        score++;
      }
    }

    return score;
  }

  public static List<String> generateBestGuess(byte[] encryptedBytes) {
    int highScore = 0;
    char highScoreChar = '_';
    String highScoreString = "";
    List<String> bestGuess = new ArrayList<>();

    for (char charToXor: byteChars) {
      int score = 0;
      String decrypted = "";
      byte charByte = (byte) charToXor;

      for (int i = 0; i < encryptedBytes.length; i++) {
        byte currentXordByte = (byte) (encryptedBytes[i] ^ charByte);
        char decryptedChar = (char) currentXordByte;
        decrypted += decryptedChar;

        if (frequencyMap.containsKey(decryptedChar)) {
          score++;
        }

        if (score > highScore) {
          highScore = score;
          highScoreChar = charToXor;
          highScoreString = decrypted;
        }
      }
    }

    bestGuess.add(highScoreChar + "");
    bestGuess.add(highScoreString);

    return bestGuess;
  }

  private static Map<Character, Integer> generateFreqCharMap() {
    Map<Character, Integer> output = new HashMap<>();

    for (int i = 0; i < FREQ_LETTERS.length(); i++) {
      char currentChar = FREQ_LETTERS.charAt(i);
      output.put(currentChar, 0);
    }

    return output;
  }

  private static List<Character> generateByteChars() {
    List<Character> alphabetList = new ArrayList<>();

    for (char ch = 0; ch <= 255; ch++) {
      alphabetList.add(ch);
    }

    return alphabetList;
  }
}

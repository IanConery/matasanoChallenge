package challengeSetOne;

import utils.HexUtils;
import utils.CollectionBuilders.CharHashBuilder;
import utils.CollectionBuilders.CharByteListBuilder;
import java.util.List;
import java.util.ArrayList;

public class ChallengeThreeMethods {
  // https://en.wikipedia.org/wiki/Etaoin_shrdlu
  protected static final String FREQ_LETTERS = "EeTtAaOoIiNnSsHhRrDdLlUu ";
  protected static final CharHashBuilder frequencyMap = new CharHashBuilder(FREQ_LETTERS);
  protected static final CharByteListBuilder byteChars = new CharByteListBuilder(0, 255);

  public static String challengeThreeSolver(String encryptedString) {
    byte[] encryptedBytes = HexUtils.hexStringToBytes(encryptedString);
    List<String> cypherKeyAndDecryptedString = generateBestGuess(encryptedBytes);
    String decryptedString = cypherKeyAndDecryptedString.remove(1);
    String charUsed = cypherKeyAndDecryptedString.remove(0);

    return "Character Used: " + charUsed + "\nDecrypted: " + decryptedString;
  }

  public static int characterFrequencyScore(String asciiString) {
    int score = 0;

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
          // System.out.println("Swapping : " + highScoreChar + " : with : " + charToXor);
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

}

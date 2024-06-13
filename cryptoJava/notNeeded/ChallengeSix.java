import utils.DecryptionUtils;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.TreeMap;
import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.lang.IllegalArgumentException;
import java.util.Base64;
import challengeSetOne.ChallengeThreeMethods;

// https://cryptopals.com/sets/1/challenges/6
// Break reapeating key XOR
// challengeSixData.txt has been base64'd after being encrypted with repeating-key XOR.

public class ChallengeSix extends ChallengeThree {
  private static final String PATHNAME = "resources/challengeSixData.txt";

  public static void main(String[] args) {
    byte[] allBytes;
    // List<String> possibleKeys = new ArrayList<>();

    try {
      // Remove the \n from the end of each line (which is weird because they were included in Challenge Five)
      List<String> lines = Files.readAllLines(Paths.get(PATHNAME));
      String base64Text = "";

      for (String line: lines) {
        base64Text += line;
      }

      allBytes = Base64.getDecoder().decode(base64Text);
    } catch (IOException e) {
      allBytes = new byte[0];
      e.printStackTrace();
    }

    List<String> possibleKeys = findAllPossibleKeyStrings(allBytes, 2, 40, 10);

    // move to own method
    int bestScore = -1;
    String bestGuess = "";
    for (String key: possibleKeys) {
      int score = ChallengeSix.characterFrequencyScore(key);
      String[] wordsInString = key.split(" ");
      int normalizedScore = wordsInString.length * score;

      if (normalizedScore > bestScore) {
        bestGuess = key;
        bestScore = normalizedScore;
      }
    }

    // create method to finally decrypt after getting the key

    System.out.println("Most likely key : " + bestGuess);
    // Most likely key : Terminator X: Bring the noise
  }

  public static String challengeSixSolver(String path) {
    byte[] allBytes;
    int bestScore = -1;
    String bestGuess = "";

    try {
      // Remove the \n from the end of each line (which is weird because they were included in Challenge Five)
      List<String> lines = Files.readAllLines(Paths.get(path));
      String base64Text = "";

      for (String line: lines) {
        base64Text += line;
      }

      allBytes = Base64.getDecoder().decode(base64Text);
    } catch (IOException e) {
      allBytes = new byte[0];
      e.printStackTrace();
    }

    List<String> possibleKeys = findAllPossibleKeyStrings(allBytes, 2, 40, 10);

    for (String key: possibleKeys) {
      int score = ChallengeSix.characterFrequencyScore(key);
      String[] wordsInString = key.split(" ");
      int normalizedScore = wordsInString.length * score;

      if (normalizedScore > bestScore) {
        bestGuess = key;
        bestScore = normalizedScore;
      }
    }

    return "Most likely key: " + bestGuess;
  }


  public static List<String> findAllPossibleKeyStrings(byte[] stringBytes, int keySizeMin, int keySizeMax, int returnAmount) {

    List<String> possibleKeys = new ArrayList<>();
    List<Integer> possibleKeySizes = guessKeySizeFromHammingDistance(stringBytes, keySizeMin, keySizeMax, returnAmount);

    for (int keysize: possibleKeySizes) {

      String patchedTogetherKey = "";
      List<byte[]> keySizeBlocks = new ArrayList<>();
      List<byte[]> byteBlocks = new ArrayList<>();

      // Break the cipher text into blocks of keysize
      for (int i = 0; i < stringBytes.length; i += keysize){
        byte[] slice = Arrays.copyOfRange(stringBytes, i, i + keysize);
        keySizeBlocks.add(slice);
      }

      // Take the first byte of every block, then the second ... up to key length
      int blockSize = keySizeBlocks.size();
      for (int i = 0; i < keysize; i++) {
        byte[] newByteBlock = new byte[blockSize];
        for (int k = 0; k < blockSize; k++) {
          byte[] currentArray = keySizeBlocks.get(k);
          byte currentByte = currentArray[i];
          newByteBlock[k] = currentByte;
        }

        byteBlocks.add(newByteBlock);
      }


      for (byte[] encryptedBytes: byteBlocks) {
        List<String> potentialKey = ChallengeThreeMethods.generateBestGuess(encryptedBytes);

        String decryptedStringChar = potentialKey.remove(0);
        patchedTogetherKey += decryptedStringChar;

      }

      possibleKeys.add(patchedTogetherKey);
    }

    return possibleKeys;
  }

  // added multiple guesses as return value, the key size needed was the 6th smallest and not the first
  // somewhat expected as using hamming distance to crack on less thatn ~10 bytes is not effective
  private static List<Integer> guessKeySizeFromHammingDistance(byte[] stringBytes, int testKeySizeMin, int testKeySizeMax, int numberOfGuessesToReturn) {
    if (testKeySizeMax * 4 > stringBytes.length) {
      throw new IllegalArgumentException("testKeySizeMax is too large. It must be <= " + (stringBytes.length / 4));
    }

    List<Integer> topKeySizeGuesses = new ArrayList<>();
    TreeMap<Float, Integer> sortedDistances = new TreeMap<>();

    for (int i = testKeySizeMin; i <= testKeySizeMax; i++){
      // first set of bytes
      byte[] nibble1 = Arrays.copyOfRange(stringBytes, 0, i);
      byte[] nibble2 = Arrays.copyOfRange(stringBytes, i, i * 2);
      // second set of bytes
      byte[] nibble3 = Arrays.copyOfRange(stringBytes, i * 2, i * 3);
      byte[] nibble4 = Arrays.copyOfRange(stringBytes, i * 3, i * 4);
      // calculate hamming destance for both sets
      float distance1 = DecryptionUtils.calculateHammingDistance(nibble1, nibble2);
      float distance2 = DecryptionUtils.calculateHammingDistance(nibble3, nibble4);
      // average both sets
      float distanceAvg = (distance1 + distance2) / 2;
      // normalize the value by dividing by
      float normalizedDistance = distanceAvg / i;

      sortedDistances.put(normalizedDistance, i);
    }

    for (int i = 0; i < numberOfGuessesToReturn; i++) {
      topKeySizeGuesses.add(sortedDistances.pollFirstEntry().getValue());
    }

    return topKeySizeGuesses;
  }

}

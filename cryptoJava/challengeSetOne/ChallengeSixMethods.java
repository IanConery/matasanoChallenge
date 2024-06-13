package challengeSetOne;

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
import utils.HexUtils;
import challengeSetOne.ChallengeThreeMethods;
import challengeSetOne.ChallengeFiveMethods;

public class ChallengeSixMethods {

  public static String challengeSixSolver(String path) {
    byte[] allBytes;
    int bestScore = -1;
    String bestGuess = "";
    // Remove the \n from the end of each line (which is weird because they were included in Challenge Five)
    String base64Text = readAndRemoveNewLinesFromFile(path);
    allBytes = Base64.getDecoder().decode(base64Text);

    List<String> possibleKeys = findAllPossibleKeyStrings(allBytes, 2, 40, 10);

    for (String key: possibleKeys) {
      int score = ChallengeThreeMethods.characterFrequencyScore(key);
      String[] wordsInString = key.split(" ");
      int normalizedScore = wordsInString.length * score;

      if (normalizedScore > bestScore) {
        bestGuess = key;
        bestScore = normalizedScore;
      }
    }

    return bestGuess;
  }

  public static String decryptRepeatingStringXorFile(String filePath, String key) {
    String result = "";

    String fileText = readAndRemoveNewLinesFromFile(filePath);
    byte[] fileBytes = Base64.getDecoder().decode(fileText);
    String decoded = new String(fileBytes);
    result = ChallengeFiveMethods.repeatingKeyXor(decoded, key);

    return HexUtils.hexToAscii(result);
  }

  public static String readAndRemoveNewLinesFromFile(String path) {
    String noNewLines = "";

    try {
      List<String> lines = Files.readAllLines(Paths.get(path));

      for (String line: lines) {
        noNewLines += line;
      }

    } catch (IOException e) {
      e.printStackTrace();
    }

    return noNewLines;
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

  // added multiple guesses as return value, the key size needed for challenge six was the 6th smallest and not the first
  // somewhat expected as using hamming distance to crack less thatn ~10 bytes is not effective
  public static List<Integer> guessKeySizeFromHammingDistance(byte[] stringBytes, int testKeySizeMin, int testKeySizeMax, int numberOfGuessesToReturn) {
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

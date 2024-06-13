package challengeSetOne;

import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.List;
import java.util.ArrayList;
import utils.HexUtils;
import challengeSetOne.ChallengeThreeMethods;

public class ChallengeFourMethods {

  public static String challengeFourSolver(String path) {

    int highScore = 0;
    String highScoreString = "";
    String highScoreChar = "";
    List<String> lines;

    try {
      lines = Files.readAllLines(Paths.get(path));
    } catch (IOException e) {
      lines = new ArrayList<>();
      e.printStackTrace();
    }

    for (String line: lines) {

      byte[] encryptedBytes = HexUtils.hexStringToBytes(line);

      // xor the line
      List<String> solution = ChallengeThreeMethods.generateBestGuess(encryptedBytes);

      // ordered list, remove in reverse order
      String decrypted = solution.remove(1);
      String keyChar = solution.remove(0);

      int currentScore = ChallengeThreeMethods.characterFrequencyScore(decrypted);

      if (currentScore > highScore) {
        highScore = currentScore;
        highScoreString = decrypted;
        highScoreChar = keyChar;
      }
    }

    return "Character Used: " + highScoreChar + "\nDecrypted: " + highScoreString;
  }
}

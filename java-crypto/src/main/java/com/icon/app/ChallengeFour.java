import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.List;
import java.util.ArrayList;
import com.icon.app.utils.HexUtils;

// https://cryptopals.com/sets/1/challenges/4
// Detect single-charactor XOR
// Given a file of strings find one that has been xor'd with a single char

public class ChallengeFour extends ChallengeThree {
  public static final String fileName = "src/main/resources/challengeFourData.txt";

  public static void main(String[] args) {

    int highScore = 0;
    String highScoreString = "";
    String highScoreChar = "";
    List<String> lines;

    try {
      lines = Files.readAllLines(Paths.get(PATHNAME));
    } catch (IOException e) {
      lines = new ArrayList<>();
      e.printStackTrace();
    }

    for (String line: lines) {
      byte[] encryptedBytes = HexUtils.hexStringToBytes(line);
      List<String> solution = ChallengeFour.generateBestGuess(encryptedBytes);

      String decrypted = solution.remove(1);
      String keyChar = solution.remove(0);

      int currentScore = ChallengeFour.characterFrequencyScore(decrypted);

      if (currentScore > highScore) {
        highScore = currentScore;
        highScoreString = decrypted;
        highScoreChar = keyChar;
      }
    }

    System.out.println("Char Used: " + highScoreChar + "\nValue: " + highScoreString);
    // Output:
    // Char Used: 5
    // Value: Now that the party is jumping
  }
}

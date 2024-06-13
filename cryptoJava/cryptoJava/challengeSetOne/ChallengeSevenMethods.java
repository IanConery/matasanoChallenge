package challengeSetOne;

import utils.DecryptionUtils;
import challengeSetOne.ChallengeSixMethods;

public class ChallengeSevenMethods {

  public static String challengeSevenSolver(String path, String key) {
    System.out.println("\ninside seven runner !!!");
    String algorithm = "AES/ECB/NoPadding";
    System.out.println("\nthis is the algorithm : " + algorithm);
    String base64Text = ChallengeSixMethods.readAndRemoveNewLinesFromFile(path);
    System.out.println("\nthis is with removed lines : \n" + base64Text);
    String decrypted = "";
    System.out.println("\nbefore decrypting");
    decrypted = DecryptionUtils.decryptUsingJavaCipherClass(algorithm, base64Text, key);
    System.out.println("This is decrypted length : " + decrypted.length());
    return decrypted;
  }
}

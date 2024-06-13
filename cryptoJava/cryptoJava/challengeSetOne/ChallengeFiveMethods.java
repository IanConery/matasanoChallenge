package challengeSetOne;

import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.List;
import java.util.ArrayList;
import utils.HexUtils;
import challengeSetOne.ChallengeThreeMethods;

public class ChallengeFiveMethods {

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

  public static String singleByteEncryptor(char keyChar, char stringChar) {
    byte keyByte = (byte) keyChar;
    byte stringByte = (byte) stringChar;
    byte xord = (byte) (keyByte ^ stringByte);

    return HexUtils.byteToHex(xord);
  }
}

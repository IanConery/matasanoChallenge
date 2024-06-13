package challengeSetOne;

import utils.HexUtils;
import utils.Base64Utils;

public class ChallengeOneMethods {

  public static String hexTo64UsingBytes(String hexString) {
    byte[] hexToBytes = HexUtils.hexStringToBytes(hexString);
    String bytesTo64 = Base64Utils.bytesToBase64(hexToBytes);

    return bytesTo64;
  }
}

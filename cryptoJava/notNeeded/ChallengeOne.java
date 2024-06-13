import utils.Base64Utils;
import utils.HexUtils;

// https://cryptopals.com/sets/1/challenges/1
// Convert a hex string to base64 operating on raw bytes only
// expected output: SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

public class ChallengeOne {

  public static final String HEX_STRING = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";

  public static void main(String[] args) {
    String result = hexTo64UsingBytes(HEX_STRING);
    System.out.println(HexUtils.hexToAscii(HEX_STRING));
    System.out.println(result);
  }

  private static String hexTo64UsingBytes(String hexString) {
    byte[] hexToBytes = HexUtils.hexStringToBytes(hexString);
    String bytesTo64 = Base64Utils.bytesToBase64(hexToBytes);

    return bytesTo64;
  }
}

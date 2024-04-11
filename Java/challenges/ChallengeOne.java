import manipulators.Base64Manipulators;
import manipulators.HexManipulators;

// convert a hex string to base64 operating on raw bytes only

public class ChallengeOne {
  public static void main(String[] args) {
    byte[] decoded = HexManipulators.hexStringToBytes("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d");
    String hexTo64 = Base64Manipulators.bytesToBase64(decoded);

    System.out.println(hexTo64);
    // output is SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
  }
}

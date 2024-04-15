import com.icon.app.utils.HexUtils;
import com.icon.app.utils.DecryptionUtils;

// https://cryptopals.com/sets/1/challenges/6
// Break reapeating key XOR
// challengeSixData.txt has been base64'd after being encrypted with repeating-key XOR.

public class ChallengeSix {
  public static void main(String[] args) {
    String stringOne = HexUtils.asciiToHex("this is a test");
    String stringTwo = HexUtils.asciiToHex("wokka wokka!!!");

    int test = DecryptionUtils.calculateHammingDistance(stringOne, stringTwo);
    System.out.println(test);
    // 37
  }
}

import manipulators.HexManipulators;
import java.util.HashMap;

// Single-byte XOR cipher
// a hex string has been xor'd against one char find it

public class ChallengeThree {
  public static String encryptedString = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";

  public static void main(String[] args) {
    HashMap<Character, String> mp = singleByteXor(encryptedString);
    int largestAlphaCount = 0;
    String largestAlphaString = "";
    char charUsedWithLargestAlphaString = '_';

    for (char key: mp.keySet()) {
      String currentString = mp.get(key);
      int count = numberOfAlphaChars(currentString);
      if (count > largestAlphaCount) {
        largestAlphaCount = count;
        largestAlphaString = currentString;
        charUsedWithLargestAlphaString = key;
      }
    }
    System.out.println(largestAlphaCount); // 27
    System.out.println(largestAlphaString); // Cooking MC's like a pound of bacon
    System.out.println(charUsedWithLargestAlphaString); // X
  }

  private static int numberOfAlphaChars(String asciiString) {
    int count = 0;

    for (int i = 0; i < asciiString.length(); i++) {
      char currentChar = asciiString.charAt(i);
      boolean isAlpha =  Character.isLetter(currentChar);

      if (isAlpha) {
        count++;
      }

    }

    return count;
  }

  private static HashMap<Character, String> singleByteXor(String encrypted) {
    HashMap<Character, String> charMap = new HashMap<Character, String>();
    {
      for(char ch = 'A'; ch <= 'z'; ch++) {
        String xord = xorStringWithChar(ch, encrypted);
        String ascii = HexManipulators.hexToAscii(xord);

        charMap.put(ch, ascii);
      }
    }

    return charMap;
  }

  private static String xorStringWithChar(char keyChar, String encrypted) {
    byte keyByte = (byte) keyChar;
    byte[] encryptedBytes = HexManipulators.hexStringToBytes(encrypted);
    byte[] decryptedBytes = new byte[encryptedBytes.length];

    for (int i = 0; i < encryptedBytes.length; i++) {
      decryptedBytes[i] = (byte) (keyByte ^ encryptedBytes[i]);
    }

    return HexManipulators.bytesToHexString(decryptedBytes);
  }
}

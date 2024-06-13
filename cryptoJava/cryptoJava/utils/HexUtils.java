package utils;

public class HexUtils {

  public static byte[] hexStringToBytes(String hexString) {
    if (hexString.length() % 2 == 1) {
      throw new IllegalArgumentException("Invalid hexidecimal string: " + hexString);
    }

    byte [] bytes = new byte[hexString.length() / 2];

    for (int i = 0; i < hexString.length(); i += 2) {
      String hex = hexString.substring(i, i + 2);
      bytes[i / 2] = hexCharToByte(hex);
    }

    return bytes;
  }

  public static String bytesToHexString(byte[] bytes) {
    StringBuffer hexStringBuffer = new StringBuffer();

    for (int i = 0; i < bytes.length; i++) {
      hexStringBuffer.append(byteToHex(bytes[i]));
    }

    return hexStringBuffer.toString();
  }

  public static String asciiToHex(String asciiStr) {
    char[] chars = asciiStr.toCharArray();
    StringBuilder hex = new StringBuilder();

    for (char ch: chars) {
      hex.append(Integer.toHexString((int) ch));
    }

    return hex.toString();
  }

  public static String hexToAscii(String hexStr) {
    StringBuilder ascii = new StringBuilder();

    for (int i = 0; i < hexStr.length(); i += 2) {
      String str = hexStr.substring(i, i + 2);
      ascii.append((char) Integer.parseInt(str, 16));
    }

    return ascii.toString();
  }

  // public static String byteToAscii(byte signedByte) {
  //   String hex = byteToHex(signedByte);
  //   return hexToAscii(hex);
  // }

  public static String byteToHex(byte num) {
    char[] hexDigits = new char[2];
    hexDigits[0] = Character.forDigit((num >> 4) & 0xf, 16);
    hexDigits[1] = Character.forDigit((num & 0xf), 16);

    return new String(hexDigits);
  }

  public static byte hexCharToByte(String hex) {
    int firstDigit = toDigit(hex.charAt(0));
    int secondDigit = toDigit(hex.charAt(1));

    // left shift first digit (signifigant) by 4 bits then add less significat digit to it
    return (byte) ((firstDigit << 4) + secondDigit);
  }

  private static int toDigit(char hexChar) {
    int digit = Character.digit(hexChar, 16);

    if (digit == -1) {
      throw new IllegalArgumentException("Invalid hexidecimal character: " + hexChar);
    }

    return digit;
  }
}

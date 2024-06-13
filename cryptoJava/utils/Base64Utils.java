package utils;
import java.util.Base64;

public class Base64Utils {

  public static String bytesToBase64(byte[] bytes) {
    String encoded = Base64.getEncoder().encodeToString(bytes);

    return encoded;
  }

  public static byte[] base64ToBytes(String base64String) {
    byte[] bytes = Base64.getDecoder().decode(base64String);

    return bytes;
  }

  public static String decodeBase64(String base64String) {
    byte[] bytes = Base64.getDecoder().decode(base64String);
    String decodedString = new String(bytes);

    return decodedString;
  }

  public static String encodeToBase64(String asciiString) {
    String encoded = Base64.getEncoder().encodeToString(asciiString.getBytes());
    return encoded;
  }
}

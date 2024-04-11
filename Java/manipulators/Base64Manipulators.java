package manipulators;
import java.util.Base64;

public class Base64Manipulators {
  public static void main(String[] args) {

  }

  public static String bytesToBase64(byte[] bytes) {
    String encoded = Base64.getEncoder().encodeToString(bytes);
    return encoded;
  }

  public static byte[] base64ToBytes(String base64String) {
    byte[] bytes = Base64.getDecoder().decode(base64String);
    return bytes;
  }
}

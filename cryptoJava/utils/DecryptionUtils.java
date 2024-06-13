package utils;

import utils.Base64Utils;
import java.util.BitSet;
import java.security.Key;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.lang.IllegalArgumentException;
import java.security.NoSuchAlgorithmException;
import java.security.InvalidKeyException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.BadPaddingException;

public class DecryptionUtils {

  public static int calculateHammingDistance(byte[] stringOneBytes, byte[] stringTwoBytes) {
    if (stringOneBytes.length != stringTwoBytes.length) {
      throw new IllegalArgumentException("Strings must be of equal length");
    }

    // bitset doesn't have a way to get the actual length of the set
    int actualLengthInBits = stringOneBytes.length * 8;

    int differingBits = 0;
    BitSet stringOneBits = BitSet.valueOf(stringOneBytes);
    BitSet stringTwoBits = BitSet.valueOf(stringTwoBytes);


    for (int i = 0; i < actualLengthInBits; i++) {
      boolean bit1 = stringOneBits.get(i);
      boolean bit2 = stringTwoBits.get(i);

      if (bit1 != bit2) {
        differingBits++;
      }
    }

    return differingBits;
  }

  public static String decryptUsingJavaCipherClass(String algorithm, String base64CipherText, String key) {
    System.out.println("inside decryptUsingJavaCipherClass");

    byte[] plainText;
    String decrypted;
    byte[] cipherBytes = Base64Utils.base64ToBytes(base64CipherText);
    System.out.println("cipherBytes length : " + cipherBytes.length);


    try {
      Key cipherKey = new SecretKeySpec(key.getBytes(), "AES");
      System.out.println("this is cipherKey : " + cipherKey);
      Cipher decryptor = Cipher.getInstance(algorithm);
      System.out.println("this is the decryptor1 : " + decryptor);
      decryptor.init(Cipher.DECRYPT_MODE, cipherKey);
      System.out.println("this is the decryptor2 : " + decryptor);
      plainText = decryptor.doFinal();
    } catch (NoSuchAlgorithmException | NoSuchPaddingException| BadPaddingException | InvalidKeyException | IllegalBlockSizeException e) {
      System.out.println(e);
      e.printStackTrace();
    }

    decrypted = new String(plainText);

    return decrypted;
  }
}

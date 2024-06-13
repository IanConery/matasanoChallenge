package utils;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.Arrays;

public class CollectionBuilders {
  // creates a O(1) lookup of chars
  public static final class CharHashBuilder extends HashMap<Character, Integer> {

    public CharHashBuilder(String charList) {

      for (int i = 0; i < charList.length(); i++) {
        char currentChar = charList.charAt(i);
        this.put(currentChar, 0);
      }
    }
  }

  // builds a list of chars from their respective unsignedbyte number
  // Java uses two's compliment so working directly with bytes is annoying at best
  public static final class CharByteListBuilder extends ArrayList<Character> {

    public CharByteListBuilder(int startByte, int endByte) {
      final char startChar = (char) startByte;
      final char endChar = (char) endByte;

      for (char ch = startChar; ch <= endChar; ch++) {
        this.add(ch);
      }

    }
  }

  // technically not a 'builder'
  // does not support shift and unshift operations
  // this doesn't work it's sharing between instances
  public static final class DynamicByteArray {

    private static final int defaultSize = 256;

    private static byte[] bytes;
    private static boolean isFinal = false;
    private static int indexToBeAssigned = 0;

    public DynamicByteArray() {
      bytes = new byte[defaultSize];
    }

    public DynamicByteArray(int size) {
      bytes = new byte[size];
    }

    public void push(byte byteToAdd) {
      if (indexToBeAssigned == bytes.length) {
        doubleCurrentLength();
      }
      bytes[indexToBeAssigned] = byteToAdd;
      indexToBeAssigned++;
    }

    public byte pop() {
      byte value = bytes[indexToBeAssigned - 1];
      indexToBeAssigned -= 1;
      int oneThirdOfActualLength = (int)(bytes.length * (33.0f/100.0f));

      if (indexToBeAssigned <= oneThirdOfActualLength) {
        decreaseLengthByHalf();
      }

      return value;
    }

    public int length() {
      return indexToBeAssigned;
    }

    public byte[] finalArray() {
      isFinal = true;
      bytes = Arrays.copyOf(bytes, indexToBeAssigned);
      return bytes;
    }

    private void decreaseLengthByHalf() {
      bytes = Arrays.copyOf(bytes, (bytes.length / 2));
    }

    private void doubleCurrentLength() {
      bytes = Arrays.copyOf(bytes, (bytes.length * 2));
    }

  }

}


package com.icon.app.utils;

import java.util.HashMap;
import java.util.ArrayList;

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
}


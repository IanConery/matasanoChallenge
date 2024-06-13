// https://cryptopals.com/sets/1/challenges/4
// Detect single-charactor XOR
// Given a file of strings find one that has been xor'd with a single char

import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.List;
import java.util.ArrayList;
import utils.HexUtils;

// this goes with the stuff on bottom if I need it later
import java.lang.Byte;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;

public class ChallengeFour extends ChallengeThree {
  private static final String PATHNAME = "resources/challengeFourData.txt";

  public static void main(String[] args) {

    int highScore = 0;
    String highScoreString = "";
    String highScoreChar = "";
    List<String> lines;

    try {
      lines = Files.readAllLines(Paths.get(PATHNAME));
    } catch (IOException e) {
      lines = new ArrayList<>();
      e.printStackTrace();
    }

    for (String line: lines) {

      byte[] encryptedBytes = HexUtils.hexStringToBytes(line);

      // xor the line
      List<String> solution = ChallengeFour.generateBestGuess(encryptedBytes); // modify this

      // ordered list, remove in reverse order
      String decrypted = solution.remove(1);
      String keyChar = solution.remove(0);

      int currentScore = ChallengeFour.characterFrequencyScore(decrypted); // modify this

      if (currentScore > highScore) {
        highScore = currentScore;
        highScoreString = decrypted;
        highScoreChar = keyChar;
      } // there will be collisions
    }

    System.out.println("Char Used: " + highScoreChar + "\nValue: " + highScoreString);
    // Output:
    // Char Used: 5
    // Value: Now that the party is jumping
  }

  // // these challenges need serious refactors now
  // public static CrackResult crackSingleCharactorXor(byte[] bytes) {
  //   int currentScore;

  //   List<String> solution = ChallengeFour.generateBestGuess(bytes);
  //   String decrypted = solution.remove(1);
  //   String keyChar = solution.remove(0);

  //   currentScore = ChallengeFour.characterFrequencyScore(decrypted);

  //   return CrackResult.valueOf(currentScore, keyChar, decrypted);
  // }


  // public class CrackResult extends Object {
  //   public int score;
  //   public char charUsed;
  //   public String decryptedString;

  //   public CrackResult(int s, char c, String d) {
  //     score = s;
  //     charUsed = c;
  //     decryptedString = d;
  //   }
  // }

  // CrackResult hey = new CrackResult(4, 'g', "hello");
  // CrackResult another = new CrackResult(23, 'a', "not the same");
  // CrackResult again = new CrackResult(18, 'C', "for good measure");

  // System.out.println(hey);
  // System.out.println(another);
  // System.out.println(again);

  // // java reads the file one byte at a time but casts the byte as an int
  // // between 0 and 255, so we have to convert back to bytes
  // // https://en.wikipedia.org/wiki/Two%27s_complement
  // // This could work but it's goin to need a lot of work
  // public static final byte CR = Byte.decode("0x0d");
  // public static final byte LF = Byte.decode("0x0a");

  // private static List<String> readFileByteByByte(String pathname) {

  //   List<String> lines = new ArrayList<>();

  //   try {

  //     File dataFile = new File(pathname);
  //     // should throw here if file doesn't exist
  //     // boolean fileExists = dataFile.exists();
  //     // System.out.println(fileExists);
  //     InputStream fileStream = new FileInputStream(dataFile);

  //     int index = 0;
  //     String buffer = "";

  //     int unsignedByte;
  //     int crAsInt = Byte.toUnsignedInt(CR);
  //     int lfAsInt = Byte.toUnsignedInt(LF);

  //     // while not eof
  //     while ((unsignedByte = fileStream.read()) != -1) {

  //       char charFromUnsignedByte = (char) unsignedByte;

  //       // if the byte is CR or LF and not the begining of the line
  //       if (buffer.length() > 0 && (unsignedByte == crAsInt || unsignedByte == lfAsInt)) {
  //         lines.add(buffer);
  //         buffer = "";
  //         index = 0;
  //       }

  //       if (unsignedByte == crAsInt || unsignedByte == lfAsInt) {
  //         // skip it and continue
  //         continue;
  //       }

  //       buffer += charFromUnsignedByte;
  //       index++;
  //     }

  //     fileStream.close();
  //     // probably not going to happen
  //     if (buffer.length() > 0) {
  //       lines.add(buffer);
  //     }

  //   } catch(IOException e) {
  //     e.printStackTrace();
  //   }

  //   return lines;
  // }

}

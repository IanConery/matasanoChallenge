import utils.HexUtils;
import challengeSetOne.ChallengeOneMethods;
import challengeSetOne.ChallengeTwoMethods;
import challengeSetOne.ChallengeThreeMethods;
import challengeSetOne.ChallengeFourMethods;
import challengeSetOne.ChallengeFiveMethods;
import challengeSetOne.ChallengeSixMethods;
import challengeSetOne.ChallengeSevenMethods;

public class ChallengeSetOneRunner {
  private static final String CHALLENGE_ONE_HEX = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
  private static final String CHALLENGE_TWO_INPUT_1 = "1c0111001f010100061a024b53535009181c";
  private static final String CHALLENGE_TWO_INPUT_2 = "686974207468652062756c6c277320657965";
  private static final String CHALLENGE_THREE_ENCRYPTED_STRING = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";
  private static final String CHALLENGE_FOUR_PATH = "resources/challengeFourData.txt";
  private static final String CHALLENGE_FIVE_ENCRYPTION_KEY = "ICE";
  private static final String CHALLENGE_FIVE_PLAIN_TEXT = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal";
  private static final String CHALLENGE_SIX_PATH = "resources/challengeSixData.txt";
  private static final String CHALLENGE_SEVEN_PATH = "resources/challengeSevenData.txt";
  private static final String CHALLENGE_SEVEN_KEY = "YELLOW SUBMARINE";

  public static void main(String[] args) {
    // https://cryptopals.com/sets/1/challenges/1
    // Convert a hex string to base64 operating on raw bytes only
    // expected output: SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
    String challengeOneResult = ChallengeOneMethods.hexTo64UsingBytes(CHALLENGE_ONE_HEX);
    String challengeOneDecrypted = HexUtils.hexToAscii(CHALLENGE_ONE_HEX);
    System.out.println("\nChallenge One:");
    System.out.println("Result : " + challengeOneResult);
    System.out.println("Challenge one decrypted: " + challengeOneDecrypted);
    // Challenge one result : SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

    // https://cryptopals.com/sets/1/challenges/2
    // Write a function that takes two equal-length buffers and produces their XOR combination
    // expected output: 746865206b696420646f6e277420706c6179
    String challengeTwoResult = ChallengeTwoMethods.fixedXOR(CHALLENGE_TWO_INPUT_1, CHALLENGE_TWO_INPUT_2);
    String challengeTwoDecrypted = HexUtils.hexToAscii(challengeTwoResult);
    System.out.println("\nChallenge Two:");
    System.out.println("Decrypted input one: " + HexUtils.hexToAscii(CHALLENGE_TWO_INPUT_1));
    System.out.println("Decrypted input two: " + HexUtils.hexToAscii(CHALLENGE_TWO_INPUT_2));
    System.out.println("Result : " + challengeTwoResult);
    System.out.println("Challenge two decrypted: " + challengeTwoDecrypted);

    // https://cryptopals.com/sets/1/challenges/3
    // Single-byte XOR cipher
    // a hex string has been xor'd against one char, find it
    String challengeThreeResult = ChallengeThreeMethods.challengeThreeSolver(CHALLENGE_THREE_ENCRYPTED_STRING);
    System.out.println("\nChallenge Three:");
    System.out.println(challengeThreeResult);

    // https://cryptopals.com/sets/1/challenges/4
    // Detect single-charactor XOR
    // Given a file of strings find one that has been xor'd with a single char
    String challengeFourResult = ChallengeFourMethods.challengeFourSolver(CHALLENGE_FOUR_PATH);
    System.out.println("\nChallenge Four:");
    System.out.println(challengeFourResult);

    // https://cryptopals.com/sets/1/challenges/5
    // Implement repeating key-XOR
    String challengeFiveResult = ChallengeFiveMethods.repeatingKeyXor(CHALLENGE_FIVE_PLAIN_TEXT, CHALLENGE_FIVE_ENCRYPTION_KEY);
    System.out.println("\nChallenge Five:");
    System.out.println(challengeFiveResult);

    // https://cryptopals.com/sets/1/challenges/6
    // Break reapeating key XOR
    // challengeSixData.txt has been base64'd after being encrypted with repeating-key XOR.
    String challengeSixResult = ChallengeSixMethods.challengeSixSolver(CHALLENGE_SIX_PATH);
    System.out.println("\nChallenge Six:");
    System.out.println("Most likely key: " + challengeSixResult);
    // comment out next line to trim output
    // System.out.println("\n" + ChallengeSixMethods.decryptRepeatingStringXorFile(CHALLENGE_SIX_PATH, challengeSixResult));

    // https://cryptopals.com/sets/1/challenges/7
    // Decrypt AES in ECB mode
    // challengeSevenData.txt has been encrypted with AES in ECB mode using the key "YELLOW SUBMARINE"
    System.out.println("\nChallenge Seven:");
    String challengeSevenResult = ChallengeSevenMethods.challengeSevenSolver(CHALLENGE_SEVEN_PATH, CHALLENGE_SEVEN_KEY);
    System.out.println(challengeSevenResult);
  }
}

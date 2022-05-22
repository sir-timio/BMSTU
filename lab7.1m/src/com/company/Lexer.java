package com.company.la;
import java.util.ArrayList;
import java.util.regex.Pattern;

public class Lexer {
    public ArrayList<Token> tokens;
    public int axiomCount;
    public static String spec = "(\\(|\\))";
    public static String axiom = "\\* [A-Z](')?";
    public static String nterm = "[A-Z](')?";
    public static String term = "\\\"(\\\\\"|\\\\|\\|\\\t|\\\\\n|.)*?\\\"";
    public static String patternStr = "(?<term>^"+term+")|(?<axiom>^"+axiom+")|(?<nterm>^"+nterm+")|(?<spec>^"+spec+")";

    public Lexer(String text) {
        Pattern pattern = Pattern.compile(patternStr);
        Token token = new Token(text, pattern);
        tokens = new ArrayList<>();
        while (true){
            if (token.getLexemType() == LexemType.A) axiomCount++;
            if (token.getLexemType() == LexemType.END_OF_FILE || token.getLexemType() == LexemType.ERROR){
//                System.out.println(token);
                tokens.add(token);
                break;
            } else {
//                System.out.println(token);
                tokens.add(token);
                token = token.next();
            }
        }
        if (axiomCount != 1) {
            System.out.println("Need only 1 axiom");
            System.exit(1);
        }
    }
}

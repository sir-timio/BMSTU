import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Lab7_1 {
    public static void main(String[] args) throws IOException {
        String text = new String(Files.readAllBytes(Paths.get("abc.txt")));
        Lexer lexer = new Lexer(text);
        Parser parser = new Parser(lexer.tokens);
        NonTermNode root = parser.tree;
//        System.out.println(root.leftPart);
        print(root, 0);

//        for (Token key: parser.rules.keySet()){
//            System.out.print("RULE: " + key + ": ");
//            for (Token rulePart: parser.rules.get(key)){
//                System.out.print(rulePart + " ");
//            }
//            System.out.println();
//        }
    }


    public static void print(Node node, int i){
        if (node instanceof NonTermNode){
            NonTermNode nonTermNode = (NonTermNode) node;
            for (int j = 0; j < i; j++) System.out.print("-");
            System.out.print(nonTermNode.leftPart);
            System.out.println();
            for (int j = 0; j < nonTermNode.children.size(); j++){
                print(nonTermNode.children.get(j), i+2);
            }
        }
        if (node instanceof TermNode){
            TermNode termNode = (TermNode) node;
            for (int j = 0; j < i; j++) System.out.print(" ");
            System.out.print(termNode.token);
            System.out.println();
        }
    }
}


import java.util.*;

//RULES  := RULE RULES1
//RULES1 := RULE RULES1 | .
//RULE   := n R_RULE | a R_RULE
//R_RULE := l_par INNER r_par R_RULE1
//R_RULE1:= l_par INNER r_par R_RULE1 | .
//INNER  := n INNER | t INNER | .

//    Лексика:
//t = T = term   := "symbols"
//a = A = axim   := *nonterm
//n = N = nonterm:= [A-Z] | [A-Z]'

public class Parser {
    public HashMap<Token, ArrayList<Token>> rules;
    public ArrayList<Token> tokens;
    public NonTermNode tree;

    String[][] table = {
//                           T          N              A            l_par               r_par    $
            /* RULES  */{"ERR",  "RULE RULES1",   "RULE RULES1",     "ERR",              "ERR",  "ERR"},
            /* RULES1 */{"ERR",  "RULE RULES1",   "RULE RULES1",     "ERR",              "ERR",   "END_OF_FILE"},
            /* RULE   */{"ERR",  "N R_RULE",      "A R_RULE",        "ERR",              "ERR",  "ERR"},
            /* R_RULE */{"ERR",    "ERR",           "ERR",  "L_PAR INNER R_PAR R_RULE1", "ERR",  "ERR"},
            /* R_RULE1*/{"ERR",    "ERR",           "ERR",  "L_PAR INNER R_PAR R_RULE1", "ERR",   "END_OF_FILE"},
            /* INNER  */{"T INNER","N INNER",        "ERR",          "ERR",              "ERR",   "ERR"},
    };

    public Parser(ArrayList<Token> tokens) {
        this.tokens = tokens;
        rules = new HashMap<>();
        int par_count = 0;
        Token last_decl = null;
        for (Token token: tokens){
            if ((token.getLexemType() == LexemType.N || token.getLexemType() == LexemType.A) && par_count != 0 && last_decl == null){
                System.out.println("NonTerm or axiom without declaration");
                System.exit(1);
            }
            if (token.getLexemType() == LexemType.L_PAR) par_count++;
            if (token.getLexemType() == LexemType.R_PAR) par_count--;
            if ((token.getLexemType() == LexemType.N || token.getLexemType() == LexemType.A) && par_count == 0){
                rules.put(token, new ArrayList<>());
                last_decl = token;
            } else {
                if (token.getLexemType() != LexemType.END_OF_FILE) rules.get(last_decl).add(token);
            }
        }
        tree = topDown();
    }


    public int getTableLineIndex(String word){
        switch (word){
            case "RULES":
                return 0;
            case "RULES1":
                return 1;
            case "RULE":
                return 2;
            case "R_RULE":
                return 3;
            case "R_RULE1":
                return 4;
            case "END_OF_FILE":
                return 5;
            default:
                return 5;
        }
    }

    public int getTableColIndex(String word){
        switch (word){
            case "T":
                return 0;
            case "N":
                return 1;
            case "A":
                return 2;
            case "L_PAR":
                return 3;
            case "R_PAR":
                return 4;
            default:
                return 5;
        }
    }

    public NonTermNode topDown(){
        NonTermNode fake_root = new NonTermNode("S1->RULES $");
        Stack<StackItem> stack = new Stack<>();
        stack.push(new StackItem("$", fake_root));
        stack.push(new StackItem("RULES", fake_root));
        Token token;
        int index = 0;
        StackItem x;
        do {
            token = tokens.get(index);
            x = stack.pop();
            System.out.println("Popped: " + x.type);
            if (x.type.equals("T") || x.type.equals("N") || x.type.equals("A")
                    || x.type.equals("L_PAR") || x.type.equals("R_PAR")){
                if (x.type.equals(token.getLexemType().toString())){
                    x.parent.children.add(new TermNode(token));
                    index++;
                } else {
                    System.out.println("1)Unexpected " + token.getLexemType() + ", expected " + x.type + ", " + token.currentPos);
                    System.exit(1);
                }
            } else if (!table[getTableLineIndex(x.type)][getTableColIndex(token.getLexemType().toString())].equals("ERR")){
                String rule = table[getTableLineIndex(x.type)][getTableColIndex(token.getLexemType().toString())];
                String left_part = x.type;
                NonTermNode nonTermNode = new NonTermNode(left_part + "->" + rule);
                x.parent.children.add(nonTermNode);
                System.out.print("Pushed: ");
                for (int i = nonTermNode.rule.size()-1; i >= 0; i--){
                    stack.push(new StackItem(nonTermNode.rule.get(i), nonTermNode));
                    System.out.print(nonTermNode.rule.get(i) + " ");
                }
                System.out.println();
            } else if (!(x.type.equals("END_OF_FILE")) && !(x.type.equals("INNER") && token.getLexemType()==LexemType.R_PAR)
                    && !(x.type.equals("R_RULE1") && (token.getLexemType()==LexemType.A || token.getLexemType()==LexemType.N))){
                System.out.println(x.type + ", " + token + ", " + table[getTableLineIndex(x.type)][getTableColIndex(token.getLexemType().toString())]);
                System.out.println("2)Unexpected " + token.getLexemType() + ", expected " + x.type + ", " + token.currentPos);
                System.exit(1);
            }
        } while (!x.type.equals("END_OF_FILE"));

        NonTermNode res = (NonTermNode) fake_root.children.get(0);
//        System.out.println(res.leftPart);
        return res;
    }

}

class Node{}

class NonTermNode extends Node{
    public String leftPart;
    public ArrayList<String> rule;
    public ArrayList<Node> children;

    public NonTermNode(String rule) {
        String[] parts = rule.split("->");
        this.leftPart = parts[0];
        this.rule = new ArrayList<>();
        String[] right_parts = parts[1].split(" ");
        this.rule.addAll(Arrays.asList(right_parts));
        this.children = new ArrayList<>();
    }
}

class TermNode extends Node{
    public Token token;

    public TermNode(Token token) {
        this.token = token;
    }
}

class StackItem{
    public String type;
    public NonTermNode parent;

    public StackItem(String type, NonTermNode parent) {
        this.type = type;
        this.parent = parent;
    }
}

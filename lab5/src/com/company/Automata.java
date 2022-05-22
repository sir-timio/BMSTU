package com.company;
import java.util.*;

public class Automata {

    public final static int[][] table = {

                        /* s    u    p    e    r    c    l    a    -    >    "    \   num  ws  a-z  EOL  UNK*/
            /*  START   */{ 1, 10,  10,  10,  10,   6,  10,  10,  11,  -1,  13,  -1,  15,  16,  10, 16,  -1},
            /*  ID_1    */{10,  2,  10,  10,  10,  10,  10,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  ID_2    */{10, 10,   3,  10,  10,  10,  10,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  ID_3    */{10, 10,  10,   4,  10,  10,  10,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  ID_4    */{10, 10,  10,  10,   5,  10,  10,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  KEY_5   */{10, 10,  10,  10,  10,  10,  10,  10,  -1,  -1,  -1,  -1,  -1,  -1,  10, -1,  -1},
            /*  ID_6    */{10, 10,  10,  10,  10,  10,   7,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  ID_7    */{10, 10,  10,  10,  10,  10,  10,   8,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  ID_8    */{ 9, 10,  10,  10,  10,  10,  10,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  ID_9    */{ 5, 10,  10,  10,  10,  10,  10,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  ID_10   */{10, 10,  10,  10,  10,  10,  10,  10,  -1,  -1,  -1,  -1,  10,  -1,  10, -1,  -1},
            /*  OP_11   */{-1, -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  12,  -1,  -1,  -1,  -1,  -1, -1,  -1},
            /*  OP_12   */{-1, -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, -1,  -1},
            /*  LIT_13  */{13, 13,  13,  13,  13,  13,  13,  13,  13,  13,  14,  17,  13,  13,  13, -1,  -1},
            /*  LIT_14  */{-1, -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, -1,  -1},
            /*  NUM_15  */{-1, -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  15,  -1,  -1, -1,  -1},
            /*  WS_16   */{-1, -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  16,  -1, 16,  -1},
            /*  ESC_17  */{13, 13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13, 16,  -1},


    };

    private SortedMap<Position, String> messages;
    private ArrayList<Token> tokens;
    public HashMap<String, Integer> idents = new HashMap<>();
    private int ident_order = 0;
    private String program;
    private Position pos;
    private int state;

    public Automata(String program) {
        this.program = program;
        this.pos = new Position(program);
        this.state = 0;
        this.messages = new TreeMap<>();
        this.tokens = new ArrayList<>();
    }

    public HashMap<String, Integer> getMap() {
        return idents;
    }

    private int getCode(char c) {
        /* s    u    p    e    r    c    l    a    -    >    "   num  ws  a-z*/
        switch (c) {
            case 's':
                return 0;
            case 'u':
                return 1;
            case 'p':
                return 2;
            case 'e':
                return 3;
            case 'r':
                return 4;
            case 'c':
                return 5;
            case 'l':
                return 6;
            case 'a':
                return 7;
            case '-':
                return 8;
            case '>':
                return 9;
            case '\"':
                return 10;
            case '\n':
                return 15;
            case '\\':
                return 11;
        }
        if (c >= '0' && c <= '9')
            return 12;
        if (c == ' ' || c == '\t' || c == '\r')
            return 13;
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
            return 14;
        return 16;
    }

    private String getStateName(int state) {
        return switch (state) {
            case 1, 2, 3, 4, 6, 7, 8, 9, 10 -> "IDENT";
            case 5 -> "KEYWORD";
            case 11, 12 -> "OPERATION";
            case  14 -> "STRING LITERAL";
            case 15 -> "NUMBER";
            case 16 -> "WHITESPACE";
            default -> "ERROR";
        };
    }

    public void run() {
        while (!pos.isEOF()) {
            StringBuilder word = new StringBuilder();
            state = 0;
            boolean finalState = false;
            boolean errorState = false;
            Position start = new Position(pos);

            while (!pos.isEOF()) {
                char curr_char = program.charAt(pos.getIndex());
                int jump_code = getCode(curr_char);

                int next_state = table[state][jump_code];

                if (-1 == next_state) {
                    if (state == 0) {
                        errorState = true;
                    } else {
                        finalState = true;
                    }
                    break;
                }

                state = next_state;
                pos = pos.next();
                word.append(curr_char);

                if (pos.isEOF() && curr_char != '\\') {
                    finalState = true;
                    break;
                }

            }
            if (finalState) {
                Fragment frag = new Fragment(start, pos);
                String value = word.toString().replaceAll("\n", "");
                String domain = getStateName(state);
                if (Objects.equals(domain, "IDENT")){
                    if (idents.containsKey(value)) {
                        int id = idents.get(value);
                        tokens.add(new Token(domain, String.valueOf(id),  frag));
                    } else {
                        idents.put(value, ident_order);
                        tokens.add(new Token(domain, String.valueOf(ident_order),  frag));
                        ident_order++;
                    }
                } else {
                    tokens.add(new Token(domain, value,  frag));
                }
                continue;
            }

            if (errorState) {
                messages.put(new Position(pos), "Unexpected char");
            }

            pos = pos.next();
        }

        Fragment frag = new Fragment(pos, pos);
        tokens.add(new Token("EOF" , " " , frag));
    }

    public boolean hasNextToken() {
        return !tokens.isEmpty();
    }

    public Token nextToken() {
        return tokens.remove(0);
    }

    public void output_messages() {
        if (messages.isEmpty())
            return;
        System.out.println("\nMessages:");
        for (Map.Entry<Position, String> entry : messages.entrySet()) {
            System.out.print("ERROR ");
            System.out.print("(" + entry.getKey().getLine() + ", " +
                    entry.getKey().getPos() + "): ");
            System.out.println(entry.getValue());
        }
    }
}
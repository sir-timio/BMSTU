import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Token{
    private Pattern pattern;
    public Position currentPos, nextPos;
    private LexemType lexemType;
    public String attribute;

    public Token(LexemType lexemType, String attribute){
        this.lexemType = lexemType;
        this.attribute = attribute;
    }

    public Token(String text, Pattern pattern) {
        this(new Position(1,1,0, text), pattern);
    }

    public Token(Position pos, Pattern pattern){
        this.pattern = pattern;
        this.currentPos = pos;
        currentPos = currentPos.skipWhiteSpaces();
        Matcher matcher = pattern.matcher(currentPos.text);
        nextPos = currentPos.nextPosition();

        if (currentPos.isEmpty()){
            lexemType = LexemType.END_OF_FILE;
            attribute = "end_of_file";
        } else if (!matcher.find()) {
            lexemType = LexemType.ERROR;
            attribute = currentPos.text.substring(0,1);
        } else if (matcher.group("spec") != null) {
            if (matcher.group().equals("(")){
                lexemType = LexemType.L_PAR;
            } else {
                lexemType = LexemType.R_PAR;
            }
            attribute = matcher.group("spec");
            nextPos = nextPos.nextTokenPos(matcher.end());
        } else if (matcher.group("axiom") != null) {
            lexemType = LexemType.A;
            attribute = matcher.group("axiom");
            nextPos = nextPos.nextTokenPos(matcher.end());
        } else if (matcher.group("nterm") != null) {
            lexemType = LexemType.N;
            attribute = matcher.group("nterm");
            nextPos = nextPos.nextTokenPos(matcher.end());
        } else if (matcher.group("term") != null) {
            lexemType = LexemType.T;
            attribute = matcher.group("term");
            nextPos = nextPos.nextTokenPos(matcher.end());
        }
    }

    public Token next()  {
        return new Token(nextPos, pattern);
    }

    public LexemType getLexemType() {
        return lexemType;
    }

    @Override
    public String toString() {
        return lexemType + "(" + currentPos + "):" + attribute + "";
    }
}
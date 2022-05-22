class Position{
    private int line, pos, index;
    public String text;

    public Position(int line, int pos, int index, String text) {
        this.line = line;
        this.pos = pos;
        this.index = index;
        this.text = text;
    }

    public boolean isEmpty(){
        return text.isEmpty();
    }

    public int getSymbol(){
        if (index < text.length()){
            return text.charAt(index);
        } else {
            return -1;
        }
    }

    public Position nextPosition(){
        int currentChar = getSymbol();
        if (currentChar == -1){
            return this;
        } else if (currentChar == '\n'){
            return new Position(line+1, 1, index, text.substring(1));
        } else {
            return new Position(line, pos+1, index, text.substring(1));
        }
    }

    public Position skipWhiteSpaces(){
        Position position = this;
        int x = position.getSymbol();
        while(Character.isWhitespace(x)){
            position = position.nextPosition();
            x = position.getSymbol();
        }
        return position;
    }

    @Override
    public String toString() {
        return line + "," + pos;
    }

    public Position nextTokenPos(int end) {
        int lastTokenInd = end-1;
        Position position = this;
        for (int i = 0; i < lastTokenInd; i++){
            position = position.nextPosition();
        }
        position.text = text.substring(lastTokenInd);
        return position;
    }
}

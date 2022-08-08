package com.company;

public class Position implements Comparable<Position> {
    private String text;
    private int line, pos, index;

    public Position(String text) {
        this.text = text;
        line = pos = 1;
        index = 0;
    }

    public Position(Position p) {
        this.text  = p.getText();
        this.line  = p.getLine();
        this.pos   = p.getPos();
        this.index = p.getIndex();
    }

    public String getText() {
        return text;
    }

    public int getLine() {
        return line;
    }

    public int getPos() {
        return pos;
    }

    public int getIndex() {
        return index;
    }

    public boolean isEOF() {
        return index == text.length();
    }

    public boolean isNewLine() {
        if (index == text.length()) {
            return true;
        }
        if (text.charAt(index) == '\r' && index+1 < text.length()) {
            return (text.charAt(index+1) == '\n');
        }
        return (text.charAt(index) == '\n');
    }

    public Position next() {
        Position p = new Position(this);
        if (!p.isEOF()) {
            if (p.isNewLine()) {
                if (p.text.charAt(p.index) == '\r')
                    p.index++;
                p.line++;
                p.pos = 1;
            } else {
                if (Character.isHighSurrogate(p.text.charAt(p.index)))
                    p.index++;
                p.pos++;
            }
            p.index++;
        }
        return p;
    }

    @Override
    public int compareTo(Position other) {
        return Integer.compare(index, other.index);
    }

    @Override
    public String toString() {
        return "(" + line + ", " + pos + ")";
    }

}
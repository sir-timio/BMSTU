enum LexemType{
    END_OF_FILE,
    T,
    A,
    N,
    L_PAR,
    R_PAR,
    $,
    S1,
    POINT,
    ERROR;

    @Override
    public String toString() {
        String text = null;
        switch (this){
            case N:
                text = "N";
                break;
            case T:
                text = "T";
                break;
            case L_PAR:
                text = "L_PAR";
                break;
            case R_PAR:
                text = "R_PAR";
                break;
            case A:
                text = "A";
                break;
            case END_OF_FILE:
                text = "END_OF_FILE";
                break;
            case ERROR:
                text = "ERROR";
                break;
            case $:
                text = "$";
                break;
            case S1:
                text = "S1";
                break;
            case POINT:
                text = "POINT";
                break;
        }
        return text;
    }
}
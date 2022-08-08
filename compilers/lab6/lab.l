%option noyywrap bison-bridge bison-locations

%{

#include <stdio.h>
#include <stdlib.h>

#define TAG_EOF 0
#define TAG_FLOAT 1
#define TAG_DOUBLE 2
#define TAG_WORD 3
#define TAG_SPACE 4
#define TAG_EOL 5
#define TAG_ERROR 6
#include <float.h>
#include <limits.h>


const char *tag_names [] = {
    "EOF", "FLOAT", "DOUBLE", "WORD", "SPACE", "EOL", "ERROR"
};
struct Position {
    int line, pos, index;
};

void print_pos(struct Position *p) {
    printf("(%d,%d)", p->line, p->pos);
}

struct Fragment {
    struct Position starting, following;
};

typedef struct Fragment YYLTYPE;

void print_frag(struct Fragment *f) {
    print_pos(&(f->starting));
    printf("-");
    print_pos(&(f->following));
}

union Token {
    char *word;
    float float_value;
    double double_value;
};

typedef union Token YYSTYPE;

int continued;
struct Position cur;

#define YY_USER_ACTION                       \
{                                            \
    int i;                                   \
    if (!continued)                          \
        yylloc->starting = cur;              \
    continued = 0;                           \
                                             \
    for (i = 0; i < yyleng; i++) {           \
        if (yytext[i] == '\n') {             \
            cur.line++;                      \
            cur.pos = 1;                     \
        } else {                             \
            cur.pos++;                       \
        }                                    \
        cur.index++;                         \
    }                                        \
    yylloc->following = cur;                 \
}

long size;

void init_scanner(char *program) {
    continued = 0;
    cur.line = 1;
    cur.pos = 1;
    cur.index = 0;
    yy_scan_string(program);
}

void err(const char *msg) {
    printf("ERROR");
    print_pos(&cur);
    printf(": %s\n", msg);
}

%}

SPACE [ \t\r]+
EOL [\n]+
DIGIT [0-9]
FLOAT {DIGIT}+
DOUBLE {DIGIT}+\.
WORD [^ \t\r\n]+

%%
{EOL} {
    yylval->word = (char*)("");
	return TAG_EOL;
}
{SPACE} {
	yylval->word = (char*)(" ");
	return TAG_SPACE;
}
{FLOAT} {
    char * endptr;
    float value = strtof(yytext, &endptr);
    if (value > FLT_MAX) {
        return TAG_ERROR;
    }
    yylval->float_value = value;
	return TAG_FLOAT;
}
{DOUBLE} {
    char * endptr;
    double value = strtod(yytext, &endptr);
    if (value > DBL_MAX) {
        return TAG_ERROR;
    }
	yylval->double_value = value;
	return TAG_DOUBLE;
}
{WORD} {
    size += yyleng;
    yylval->word = yytext;
	return TAG_WORD;
}
. {
    err("");
    yylval->word = (char*)("");
	return TAG_ERROR;
}
%%

int main(int argc, const char **argv) {
    int tag;
    YYSTYPE token;
    YYLTYPE coords;
    long size_str;
    char *str;
    FILE *input;
    input = fopen(argv[1], "rb");
    if (input == NULL) {
        fputs("cannot open file", stderr);
        exit(1);
    }
    fseek(input, 0, SEEK_END);
    size_str = ftell(input);
    rewind(input);
    
    str = (char*)malloc(sizeof(char)*(size_str+1));
    if (str == NULL) {
        fputs("malloc error", stderr);
        exit(1);
    }
    fread(str, sizeof(char), size_str, input);
    str[size_str] = '\0';
    fclose(input);
    init_scanner(str);
    do {
        tag = yylex(&token, &coords);
        printf("%s ", tag_names[tag]);
        print_frag(&coords);
        
        if (tag == TAG_WORD || tag == TAG_SPACE || tag == TAG_EOL) {
            printf(": %s\n", token.word);
        }
        else if (tag == TAG_FLOAT) {
            printf(": %f\n", token.float_value);
        }
        else if (tag == TAG_DOUBLE) {
            printf(": %f\n", token.double_value);
        }
        else {
            printf("\n");
        }
    } while (tag != TAG_EOF);
    printf("\n");
    free(str);
    return 0;
}
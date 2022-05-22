package main

import (
	"fmt"
	"regexp"
	"strings"
)

type TokenType string

type Token struct {
	StartPos  int
	EndPos    int
	Line      int
	Value     string
	TokenType TokenType
}

func (t *Token) String() string {
	result := fmt.Sprintf("<%s> ", t.TokenType)
	// if t.StartPos != t.EndPos {
		// result += fmt.Sprintf(" - (%d, %d)", t.Line, t.EndPos)
	// }
	if t.Value != "" {
		result += fmt.Sprintf(" - %s ", t.Value)
	}
	return result
}


type Lexer struct {
	input  string
	tokens []Token
}

var (
	AXIOM    TokenType = "$AXIOM"
	NTERM    TokenType = "$NTERM"
	TERM     TokenType = "$TERM"
	RULE     TokenType = "$RULE"
	EPS      TokenType = "$EPS"
	Term     TokenType = "term"
	Nterm    TokenType = "nterm"
	SYMBOL_R           = regexp.MustCompile(".+")
	TERM_R             = regexp.MustCompile("\".+?\"")
	NEWLINE  TokenType = "\n"
)

func lex(input string) ([]Token, error) {
	str := strings.ReplaceAll(input, "\n", " \n ")
	str = strings.ReplaceAll(input, "\t", " ")
	fmt.Println(str)
	splits := strings.Split(str, "\n")
	lN := 0
	tokens := []Token{}
	for _, line := range splits {
		lN++
		split := strings.Split(line, " ")
		if split[0] == "*" {
			continue
		}
		for _, s := range split {
			switch s {
			case "\n":
				tokens = append(tokens, Token{
					Value:     "",
					TokenType: NEWLINE,
				})
			case "$AXIOM":
				tokens = append(tokens, Token{
					TokenType: AXIOM,
				})
			case "$NTERM":
				tokens = append(tokens, Token{
					TokenType: NTERM,
				})
			case "$TERM":
				tokens = append(tokens, Token{
					TokenType: TERM,
				})
			case "$RULE":
				tokens = append(tokens, Token{
					TokenType: RULE,
				})
			case "$EPS":
				tokens = append(tokens, Token{
					TokenType: EPS,
				})
			default:
				term := TERM_R.FindStringSubmatch(s)
				if len(term) > 0 {
					tokens = append(tokens, Token{
						Value:     term[0],
						TokenType: Term,
					})
					continue
				}

				nterm := SYMBOL_R.FindStringSubmatch(s)
				if len(nterm) > 0 {
					tokens = append(tokens, Token{
						Value:     nterm[0],
						TokenType: Nterm,
					})
				}
			}
		}
	}
	return tokens, nil
}

// A = $AXIOM nterm_list
// N = $NTERM nterm_list
// T = $TERM term_list
// R = $RULE nterm = list
// nterm_list = nterm_list nterm | nterm
// term_list = term_list term | term
// term = \" symbol \"
// nterm = symbol | symbol\'
// list = list \n list | term list | nterm list | $EPS

func main() {
	tokens, err := lex(`$AXIOM E 
$NTERM E' T T' F
$TERM "+" "*" "(" ")" "n"
* asfafas
$RULE E = T E'
$RULE E' = "+" T E'
$EPS
$RULE T = F T'
$RULE T' = "*" F T'
$EPS
$RULE F = "n"
"(" E ")"`)
	fmt.Println(err)
	for _, token := range tokens {
		fmt.Println(token.String())
	}
}


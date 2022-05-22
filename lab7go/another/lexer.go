// package main

// import (
// 	"fmt"
// 	"regexp"
// 	"strings"
// )

// type Lexer struct {
// 	input  string
// 	tokens []Token
// }

// var (
// 	AXIOM    TokenType = "$AXIOM"
// 	NTERM    TokenType = "$NTERM"
// 	TERM     TokenType = "$TERM"
// 	RULE     TokenType = "$RULE"
// 	EPS      TokenType = "$EPS"
// 	Term     TokenType = "term"
// 	Nterm    TokenType = "nterm"
// 	SYMBOL_R           = regexp.MustCompile(".+")
// 	TERM_R             = regexp.MustCompile("\".+?\"")
// 	NEWLINE  TokenType = "\n"
// )

// func lex(input string) ([]Token, error) {
// 	str := strings.ReplaceAll(input, "\n", " \n ")
// 	str = strings.ReplaceAll(input, "\t", " ")
// 	fmt.Println(str)
// 	splits := strings.Split(str, "\n")
// 	lN := 0
// 	tokens := []Token{}
// 	for _, line := range splits {
// 		lN++
// 		split := strings.Split(line, " ")
// 		if split[0] == "*" {
// 			continue
// 		}
// 		for _, s := range split {
// 			switch s {
// 			case "\n":
// 				tokens = append(tokens, Token{
// 					Value:     "",
// 					TokenType: NEWLINE,
// 				})
// 			case "$AXIOM":
// 				tokens = append(tokens, Token{
// 					TokenType: AXIOM,
// 				})
// 			case "$NTERM":
// 				tokens = append(tokens, Token{
// 					TokenType: NTERM,
// 				})
// 			case "$TERM":
// 				tokens = append(tokens, Token{
// 					TokenType: TERM,
// 				})
// 			case "$RULE":
// 				tokens = append(tokens, Token{
// 					TokenType: RULE,
// 				})
// 			case "$EPS":
// 				tokens = append(tokens, Token{
// 					TokenType: EPS,
// 				})
// 			default:
// 				term := TERM_R.FindStringSubmatch(s)
// 				if len(term) > 0 {
// 					tokens = append(tokens, Token{
// 						Value:     term[0],
// 						TokenType: Term,
// 					})
// 					continue
// 				}

// 				nterm := SYMBOL_R.FindStringSubmatch(s)
// 				if len(nterm) > 0 {
// 					tokens = append(tokens, Token{
// 						Value:     nterm[0],
// 						TokenType: Nterm,
// 					})
// 				}
// 			}
// 		}
// 	}
// 	return tokens, nil
// }

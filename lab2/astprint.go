package main

import (
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"

	//"go/printer"
	"go/token"
	"os"
)


func countAssign(file *ast.File) {
	ast.Inspect(file, func(node ast.Node) bool {
		if file, ok := node.(*ast.File); ok {
			file.Decls = append([]ast.Decl{
				&ast.GenDecl{
					Doc: nil,
					Tok: token.VAR,
					Specs: []ast.Spec{
						&ast.ValueSpec{
							Names: []*ast.Ident{
								&ast.Ident{Name: "counter"},
							},
							Values: []ast.Expr{
								&ast.BasicLit{Kind: token.INT, Value: "0"},
							},
						},
					},
				},
			}, file.Decls...)
		} else if blockStmt, block_ok := node.(*ast.BlockStmt); block_ok {
			block_len := len(blockStmt.List)
			for i := block_len-1; i >= 0; i-- {
				stmt := blockStmt.List[i]
				if assign, assign_ok := stmt.(*ast.AssignStmt); assign_ok {
					if left, ok := assign.Lhs[0].(*ast.Ident); ok && left.Name != "counter" {
						block := append(blockStmt.List, nil)
						copy(block[i+1:], block[i:])
						block[i+1] = &ast.IncDecStmt{
							X:      &ast.Ident{ Name: "counter"},
							TokPos: assign.End(),
							Tok: token.INC,
						}

						blockStmt.List = block
					}
				}
			}
		} else if funcDecl, ok := node.(*ast.FuncDecl); ok {
			if funcDecl.Name.Name == "main" {
				funcDecl.Body.List = append(funcDecl.Body.List, &ast.ExprStmt{
						X: &ast.CallExpr{
							Fun: &ast.SelectorExpr{
								X:   ast.NewIdent("fmt"),
								Sel: ast.NewIdent("Printf"),
							},
							Args: []ast.Expr{
								&ast.BasicLit{
									Kind:  token.IDENT,
									Value: "counter",
								},
							},
						},
					})
			}
		} 
		return true
	})
}


func main() {
	if len(os.Args) != 2 {
		return
	}

	fset := token.NewFileSet()
	if file, err := parser.ParseFile(fset, os.Args[1], nil, parser.ParseComments); err == nil {
		countAssign(file)

		if format.Node(os.Stdout, fset, file) != nil {
			fmt.Printf("Formatter error: %v\n", err)	
		}

		// ast.Fprint(os.Stdout, fset, file, nil)
	} else {
		fmt.Printf("Errors in %s\n", os.Args[1])
	}
}

#!/bin/sh
flex -o lab.yy.cpp lab.l
gcc -ll -o lex lab.yy.cpp
./lex in.txt
use std::collections::HashMap;
use std::fmt;
use std::fmt::format;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process::id;

const EOF: char = '\0';

fn is_letter(ch: char) -> bool {
    'a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z'
}

fn is_digit(ch: char) -> bool {
    '0' <= ch && ch <= '9'
}

// fn is_ident_char(ch: char) -> bool {
//     ch == '$'
// }

fn is_break(ch: char) -> bool {
    ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n' || ch == EOF
}

#[derive(Copy, Clone)]
pub struct Position {
    row: i32,
    col: i32,
    i: usize
}

impl Position {
    pub fn to_string(&self) -> String {
        return format!("({}, {})", self.row, self.col)
    }
}




#[derive(Clone)]
pub struct Token {
    start: Position,
    end: Position,
    token_type: TokenType,
}

impl Token {
    pub fn to_string(&self) -> String {
        return format!("{} {}-{}", self.token_type.to_string(), self.start.to_string(),
                       self.end.to_string())
    }
}

#[derive(Clone)]
pub enum TokenType {
    EOF,
    ERROR(String),
    STR(String),
    IDENT(i32),
    NUMBER(i32),
}

impl fmt::Display for TokenType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            TokenType::EOF => write!(f, "EOF"),
            TokenType::ERROR(error) => write!(f, "error: {}", error.to_string()),
            TokenType::STR(str) => write!(f, "STR: {}", str),
            TokenType::IDENT(ident) => write!(f, "IDENT: {}", ident.to_string()),
            TokenType::NUMBER(number) => write!(f, "NUMBER: {}", number.to_string()),

            _ => write!(f, "unknown")
        }
    }
}

pub struct Lexer {
    input: Vec<char>,
    pub pos: Position,
    pub char: char,
    pub token: TokenType,
    pub idents: HashMap<String, i32>,
    pub ident_i: i32

}

impl Lexer {

    pub fn read_char(&mut self){
        self.char = self.input[self.pos.i];
    }

    pub fn inc_pos(&mut self) {
        let ch = self.char;
        if ch == EOF {
            return
        }
        self.pos.i += 1;
        if self.char == '\n' {
            self.pos.row += 1;
            self.pos.col = 1;
        } else {
            self.pos.col += 1;
        }
    }

    pub fn next_token(&mut self) -> Token{
        self.skip_spaces();
        if self.char == EOF {
            return self.eof_token();
        }
        if self.char == '"' {
            return self.read_str();
        }
        if self.char == '$' {
            return self.read_hex();
        }
        if is_letter(self.char) {
            return self.read_ident();
        }
        if is_digit(self.char) && !(self.char == '0') {
            return self.read_number();
        }

        return self.error_token(self.char.to_string());
    }

    pub fn read_ident(&mut self) -> Token {
        let start = self.pos.clone();
        let mut ident_vec: Vec<char> = Vec::new();

        loop {

            ident_vec.push(self.char);

            self.inc_pos();
            self.read_char();


            let ch = self.char;
            if !(is_letter(ch) || ch == '$') {
                break;
            }
        }
        let token_type: TokenType;
        let ident = String::from_iter(ident_vec);
        let key = self.idents.get(&ident);
        match key {
            Some(key) => {
                token_type = TokenType::IDENT(*key)
            },
            None => {
                self.idents.insert(ident, self.ident_i);
                token_type = TokenType::IDENT(self.ident_i);
                self.ident_i += 1;
            }
        }

        let mut end = self.pos.clone();
        end.col -= 1;
        return Token{
            start,
            end,
            token_type,
        }
    }

    pub fn read_number(&mut self) -> Token {
        let start = self.pos.clone();
        let mut number: i32 = 0;

        loop {
            let s = self.char.to_string();
            let ch = self.char;

            if is_break(ch) {
                break;
            }

            if !is_digit(ch){
                return self.error_token(number.to_string());
            }

            number = number * 10 + s.parse::<i32>().unwrap();
            self.inc_pos();
            self.read_char();


        }
        let mut end = self.pos.clone();
        end.col -= 1;
        return Token{
            start: start,
            end: end,
            token_type: TokenType::NUMBER(number),
        }
    }

    pub fn read_hex(&mut self) -> Token {
        let start = self.pos.clone();
        let mut number: i32 = 0;

        self.inc_pos();
        self.read_char();
        loop {
            let s = self.char.to_string();
            let ch = self.char;

            if is_break(ch) {
                break
            }
            if !(is_digit(ch) || 'a' <= ch && ch <= 'f' || 'A' <= ch && ch <= 'F') {
                return self.error_token(number.to_string());
            }

            number = number * 16 + i32::from_str_radix(&*s, 16).unwrap();

            self.inc_pos();
            self.read_char();

        }

        let mut end = self.pos.clone();
        end.col -= 1;

        return Token{
            start: start,
            end: end,
            token_type: TokenType::NUMBER(number)
        }
    }

    pub fn read_str(&mut self) -> Token {
        let start = self.pos.clone();
        let mut str: Vec<char> = Vec::new();

        self.inc_pos();
        self.read_char();

        loop {
            if self.char == '"' {
                self.inc_pos();
                self.read_char();
                if self.char != '"' {
                    break;
                }
            }

            if self.char == '\\' {
                self.inc_pos();
                self.read_char();
                if self.char == '\n' {
                    self.inc_pos();
                    self.read_char();
                } else {
                    str.push(self.char);
                    return self.error_token(String::from_iter(str));
                }
            }

            str.push(self.char);

            self.inc_pos();
            self.read_char();
        }


        let mut end = self.pos.clone();
        end.col -= 1;

        return Token {
            start: start,
            end: end,
            token_type: TokenType::STR(String::from_iter(str)),
        };
    }

    pub fn eof_token(&mut self) -> Token {
        self.read_char();
        return Token {
            start: self.pos.clone(),
            end: self.pos.clone(),
            token_type: TokenType::EOF,
        }
    }

    pub fn error_token(&mut self, left: String) -> Token {
        let start = self.pos.clone();
        let mut val: Vec<char> = Vec::new();
        while ! is_break(self.char) {
            val.push(self.char);
            self.inc_pos();
            self.read_char();

        }
        return Token {
            start: start,
            end: self.pos.clone(),
            token_type: TokenType::ERROR(format!("{}{}", left, String::from_iter(val))),
        }
    }


    pub fn skip_spaces(&mut self) {
        let mut again = true;
        while again {
            again = false;

            self.read_char();
            let ch = self.char;

            if ch == EOF {
                break;
            }

            if ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n'{
                self.inc_pos();
                again = true;
            }
        }
    }
}

fn main() {
    let filename = "input";

    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut lines: Vec<String> = Vec::new();
    for line in reader.lines() {
        let line = line.unwrap();
        lines.push(line);
    }
    lines.push(EOF.to_string());
    let program = lines.join("\n");
    println!("{}\n\n", program);

    let mut lexer = Lexer {
        input:  program.chars().collect(),
        pos: Position{
            row: 1,
            col: 1,
            i: 0
        },
        char: '^',
        token: TokenType::EOF,
        idents: HashMap::new(),
        ident_i: 0,
    };
    loop {
        let token = lexer.next_token();
        println!("{}", token.to_string());
        match token.token_type {
            TokenType::EOF => break,
            _ => {}
        }
    }
    for key in lexer.idents.keys() {
        println!("{}: {}", key, lexer.idents.get(key).unwrap())
    }
}

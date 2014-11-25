from util import error, debug

_tokens = [
"TOK_EOF",
"TOK_BOOL", "TOK_CHAR", "TOK_INTEGER", "TOK_REAL", "TOK_STRING", "TOK_IDENT",
"TOK_PACKAGE", "TOK_CLASS", "TOK_IFACE", "TOK_FUNC", "TOK_ALIAS",
"TOK_CONST", "TOK_VAR",
"TOK_IF", "TOK_ELSE", "TOK_WHILE", "TOK_FOR",
"TOK_CONTINUE", "TOK_BREAK", "TOK_RETURN",
"TOK_PLUS", "TOK_MINUS", "TOK_ASTERISK", "TOK_FSLASH", "TOK_PERCENT", "TOK_CARAT",
"TOK_LT", "TOK_LTEQ", "TOK_GT", "TOK_GTEQ", "TOK_EQ", "TOK_EQEQ", "TOK_NEQ",
"TOK_LPAREN", "TOK_RPAREN", "TOK_LSQUARE", "TOK_RSQUARE", "TOK_LCURLY", "TOK_RCURLY",
"TOK_COMMA", "TOK_PERIOD", "TOK_EXCLAM", "TOK_SEMI", "TOK_COLON", "TOK_COLONEQ", "TOK_COLCOL",
"TOK_PIPEPIPE", "TOK_AMPAMP"
]

for i, tok in enumerate(_tokens):
    vars()[tok] = i

KEYWORDS = {
    "package": TOK_PACKAGE,
    "var": TOK_VAR,
    "const": TOK_CONST,
    "class": TOK_CLASS,
    "interface": TOK_IFACE,
    "func": TOK_FUNC,
    "alias": TOK_ALIAS,
    "if": TOK_IF,
    "else": TOK_ELSE,
    "while": TOK_WHILE,
    "for": TOK_FOR,
    "continue": TOK_CONTINUE,
    "break": TOK_BREAK,
    "return": TOK_RETURN,
}

SYMBOLS = {
    '+': TOK_PLUS,
    '-': TOK_MINUS,
    '*': TOK_ASTERISK,
    '/': TOK_FSLASH,
    '%': TOK_PERCENT,
    '^': TOK_CARAT,
    '<': TOK_LT,
    '<=': TOK_LTEQ,
    '>': TOK_GT,
    '>=': TOK_GTEQ,
    '=': TOK_EQ,
    '==': TOK_EQEQ,
    '!=': TOK_NEQ,
    '(': TOK_LPAREN,
    ')': TOK_RPAREN,
    '[': TOK_LSQUARE,
    ']': TOK_RSQUARE,
    '{': TOK_LCURLY,
    '}': TOK_RCURLY,
    ',': TOK_COMMA,
    '.': TOK_PERIOD,
    '!': TOK_EXCLAM,
    ';': TOK_SEMI,
    ':': TOK_COLON,
    ':=': TOK_COLONEQ,
    "::": TOK_COLCOL,
    "||": TOK_PIPEPIPE,
    "&&": TOK_AMPAMP,
}

class Lexer(object):
    def __init__(self, ctx, stream):
        self.ctx = ctx
        self.stream = stream
        self.idx = 0
        self.buff = ""
        self.line = 1
        self.prev = TOK_EOF

    def gettok(self):
        self.buff = ""
        tok = TOK_EOF
        while not self.idx >= len(self.stream):
            ch = self.stream[self.idx]
            if ch.isspace():
                self.idx += 1
                if ch == '\n':
                    self.line += 1
                    if self.prev in [TOK_IDENT, TOK_BOOL, TOK_CHAR,
                            TOK_INTEGER, TOK_REAL, TOK_STRING, TOK_RPAREN,
                            TOK_RCURLY, TOK_RSQUARE, TOK_RETURN, TOK_BREAK,
                            TOK_CONTINUE]:
                        tok = TOK_SEMI
                        break
                continue
            elif ch.isalpha():
                while self.stream[self.idx].isalnum():
                    self.buff += self.stream[self.idx]
                    self.idx += 1
                tok = KEYWORDS[self.buff] if self.buff in KEYWORDS else TOK_IDENT
                break
            elif ch.isdigit():
                while self.stream[self.idx].isdigit():
                    self.buff += self.stream[self.idx]
                    self.idx += 1
                if self.stream[self.idx] == '.':
                    self.buff += self.stream[self.idx]
                    self.idx += 1
                    while self.stream[self.idx].isdigit():
                        self.buff += self.stream[self.idx]
                        self.idx += 1
                    tok = TOK_REAL
                else:
                    tok = TOK_INTEGER
                break
            elif ch == '"':
                self.idx += 1
                while self.stream[self.idx] != '"':
                    self.buff += self.stream[self.idx]
                    self.idx += 1
                tok = TOK_STRING
                break
            elif ch in SYMBOLS:
                self.buff += self.stream[self.idx]
                self.idx += 1
                if self.buff + self.stream[self.idx] in ['<=','>=','==']:
                    self.buff += self.stream[self.idx]
                    self.idx += 1
                tok = SYMBOLS[self.buff]
                break
            else:
                error("ERROR")
                break
        self.prev = tok
        #debug("tok: %s" % _tokens[tok])
        return tok

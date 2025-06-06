import tkinter as tk
import re

# Anahtar kelimeler listesi
keywords = {
    'int', 'float', 'char', 'double', 'void', 'return',
    'if', 'else', 'while', 'for', 'break', 'continue'
}

# Regex tanımları
token_specification = [
    ('COMMENT',   r'//.*'),                 # Tek satır yorum
    ('BLOCK_COMMENT', r'/\*[\s\S]*?\*/'),   # Blok yorum
    ('CHAR',      r"'[^']'"),               # Tek karakterli char literal
    ('STRING',    r'"[^"]*"'),              # String literal
    ('NUMBER',    r'\d+(\.\d*)?'),          # Sayılar
    ('IDENTIFIER',r'[A-Za-z_][A-Za-z0-9_]*'), # Değişken/ad
    ('OPERATOR',  r'==|!=|<=|>=|[\+\-\*/=<>]'), # İşleçler
    ('SEPARATOR', r'[;\(\)\{\},\[\]]'),     # Ayırıcılar
    ('SKIP',      r'[ \t]+'),               # Boşluk/tab
    ('NEWLINE',   r'\n'),                   # Satır sonu
    ('MISMATCH',  r'.'),                    # Eşleşmeyen
]


token_colors = {
    'KEYWORD': '#569cd6',      # Mavi 
    'IDENTIFIER': '#d4d4d4',   # gri
    'NUMBER': '#b5cea8',       # Yeşil
    'OPERATOR': '#d16969',     # Kırmızı
    'STRING': '#ce9178',       # pembe
    'SEPARATOR': '#c586c0',    # Mor
}



# Regex birleştirme
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).finditer

def tokenize_with_positions(code):
    tokens = []
    line = 1
    col = 0
    for mo in get_token(code):
        kind = mo.lastgroup
        value = mo.group()
        start = f"{line}.{col}"
        col += len(value)
        if '\n' in value:
            line += value.count('\n')
            col = 0
        end = f"{line}.{col}"
        if kind == 'IDENTIFIER' and value in keywords:
            kind = 'KEYWORD'
        if kind not in ['SKIP', 'NEWLINE']:
            tokens.append((kind, value, start, end))
    return tokens

def tokenize(code):
    tokens = []
    for mo in get_token(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'IDENTIFIER' and value in keywords:
            kind = 'KEYWORD'
        if kind not in ['SKIP', 'NEWLINE', 'COMMENT', 'BLOCK_COMMENT']:
            tokens.append((kind, value))
    return tokens


def highlight_text():
    content = text.get("1.0", tk.END)
    tokens = tokenize_with_positions(content)

    for tag in text.tag_names():
        text.tag_remove(tag, "1.0", tk.END)

    for kind, value, start, end in tokens:
        if kind not in text.tag_names():
            text.tag_config(kind, foreground=token_colors.get(kind, "black"))
        text.tag_add(kind, start, end)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def match(self, expected_type):
        kind, value = self.current_token()
        if kind == expected_type:
            self.pos += 1
            return value
        else:
            raise SyntaxError(f"Beklenen: {expected_type}, Bulunan: {kind} ('{value}')")

    def parse(self):
        self.stmt()

    # stmt → IDENTIFIER = expr ;
    def stmt(self):
        kind, value = self.current_token()

        if kind == 'KEYWORD' and value in ('int', 'float', 'char', 'double'):
            self.match('KEYWORD')
            self.match('IDENTIFIER')
            self.match('OPERATOR')  # =
            self.expr()
            self.match('SEPARATOR')  # ;

        elif kind == 'IDENTIFIER':
            self.match('IDENTIFIER')
            self.match('OPERATOR')  # =
            self.expr()
            self.match('SEPARATOR')  # ;

        elif kind == 'KEYWORD' and value == 'return':
            self.match('KEYWORD')
            self.expr()
            self.match('SEPARATOR')

        elif kind == 'KEYWORD' and value == 'if':
            self.match('KEYWORD')
            self.match('SEPARATOR')  # (
            self.expr()
            self.match('SEPARATOR')  # )
            self.stmt()  # ya tek stmt ya da block destekli

        elif kind == 'KEYWORD' and value == 'while':
            self.match('KEYWORD')
            self.match('SEPARATOR')  # (
            self.expr()
            self.match('SEPARATOR')  # )
            self.stmt()

        elif kind == 'SEPARATOR' and value == '{':
            self.block()

        elif kind == 'KEYWORD' and value == 'for':
            self.for_stmt()
    

        else:
            raise SyntaxError(f"Beklenmeyen ifade: {kind} '{value}'")


    def block(self):
        self.match('SEPARATOR')  # {
        self.stmt_list()
        self.match('SEPARATOR')  # }

    def stmt_list(self):
        while True:
            kind, value = self.current_token()
            if kind == 'SEPARATOR' and value == '}':
                break
            self.stmt()
    def for_stmt(self):
        self.match('KEYWORD')     # for
        self.match('SEPARATOR')   # (
        
        # init: int i = 0; veya i = 0;
        kind, val = self.current_token()
        if kind == 'KEYWORD' and val in ('int', 'float', 'char', 'double'):
            self.match('KEYWORD')
            self.match('IDENTIFIER')
            self.match('OPERATOR')
            self.expr()
        elif kind == 'IDENTIFIER':
            self.match('IDENTIFIER')
            self.match('OPERATOR')
            self.expr()
        else:
            raise SyntaxError("For döngüsü init kısmı hatalı")
        self.match('SEPARATOR')  # ;

        # condition: expr
        self.expr()
        self.match('SEPARATOR')  # ;

        # update: i = i + 1
        self.match('IDENTIFIER')
        self.match('OPERATOR')
        self.expr()
        self.match('SEPARATOR')  # )

        # gövde
        self.stmt()

    # expr → term ((+|-) term)*
    def expr(self):
        self.term()
        while self.current_token()[1] in ('+', '-'):
            self.match('OPERATOR')
            self.term()

    # term → factor ((*|/) factor)*
    def term(self):
        self.factor()
        while self.current_token()[1] in ('*', '/'):
            self.match('OPERATOR')
            self.factor()

    # factor → NUMBER | IDENTIFIER | ( expr )
    def factor(self):
        kind, value = self.current_token()
        if kind == 'NUMBER':
            self.match('NUMBER')
        elif kind == 'IDENTIFIER':
            self.match('IDENTIFIER')
        elif value == '(':
            self.match('SEPARATOR')
            self.expr()
            self.match('SEPARATOR')  # )
        else:
            raise SyntaxError(f"Beklenmeyen token: {kind} ('{value}')")

def on_text_change(event):
    highlight_text()
    content = text.get("1.0", tk.END)
    parse_tokens = tokenize(content) 
    try:
        parser = Parser(parse_tokens)
        parser.parse()
        print("Parse başarılı ✅")
    except SyntaxError as e:
        print("Parse hatası ❌:", e)


# Pencere oluştur
root = tk.Tk()
root.title("Syntax Highlighter")


text = tk.Text(
    root,
    wrap="word",
    font=("Consolas", 12),
    bg="#1e1e1e",       
    fg="#d4d4d4",       
    insertbackground="white", 
    selectbackground="#264f78", 
    selectforeground="white"   
)

text.pack(expand=1, fill="both")

text.bind("<KeyRelease>", on_text_change)

root.mainloop()

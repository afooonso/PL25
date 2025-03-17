import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN'
)


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'


def t_error(t):
    print(f"Ilegal character {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()


tokens_list = []
current_index = 0

def tokenize(expression):
    """Converts the input expression into a list of tokens"""
    global tokens_list, current_index
    lexer.input(expression)
    tokens_list = [(tok.type, tok.value) for tok in lexer]
    tokens_list.append(('EOF', None))  # Fim da entrada
    current_index = 0

def current_token():
    """Returns the current token"""
    return tokens_list[current_index]

def next_token():
    """Advances to the next token"""
    global current_index
    current_index += 1

# Analisador sintático recursivo descendente
def parse_expression():
    """Processes a mathematical expression containing addition and subtraction. First resolves nested expressions (if any)."""
    term = parse_term()
    while current_token()[0] in ('PLUS', 'MINUS'):
        if current_token()[0] == 'PLUS':
            next_token()
            term += parse_term()
        elif current_token()[0] == 'MINUS':
            next_token()
            term -= parse_term()
    return term

def parse_term():
    """Processes a mathematical expression containing multiplication and division. First resolves nested expressions (if any).
    """
    factor = parse_factor()
    while current_token()[0] in ('TIMES', 'DIVIDE'):
        if current_token()[0] == 'TIMES':
            next_token()
            factor *= parse_factor()
        elif current_token()[0] == 'DIVIDE':
            next_token()
            divisor = parse_factor()
            if divisor == 0:
                raise ValueError("Erro: divisão por zero!")
            factor /= divisor
    return factor

def parse_factor():
    """ Processes a factor in a mathematical expression. A factor can be a number or an expression enclosed in parentheses."""
    tok_type, tok_value = current_token()
    
    if tok_type == 'NUMBER':  
        next_token()
        return tok_value
    elif tok_type == 'LPAREN': 
        next_token()
        result = parse_expression()
        if current_token()[0] != 'RPAREN':
            raise ValueError("Erro: Parêntese fechado esperado!")
        next_token() 
        return result
    else:
        raise ValueError(f"Erro: Token inesperado {tok_type}")

def parse(expression):
    """Parses a mathematical expression and returns the result."""
    tokenize(expression)
    result = parse_expression()
    if current_token()[0] != 'EOF':
        raise ValueError("Erro: Entrada inválida!")
    return result

while True:
    expr = input("Expressão matemática (ou 'sair' para terminar): ")
    
    if expr.lower() == "sair":
        print("Até logo! 🚀")
        break
    
    try:
        print("Resultado:", parse(expr))
    except Exception as e:
        print("Erro:", e)
"""
T = {'+', '-', '*', '/', '(', ')', 'NUMBER'}

N = {S, Expr, Term, Factor}

S = S

P = {
    S -> Expr               LA = {'NUMBER', '(', '+' , '-', 'EOF'}

    Expr -> Term OpExpr      LA = {'NUMBER', '(', '+' , '-', 'EOF'}
    
    OpExpr -> PLUS Term      LA = {'+', 'EOF'}
            | MINUS Term     LA = {'-', 'EOF'}
            | &              LA = {')', 'EOF'}

    Term -> Factor OpTerm    LA = {'NUMBER', '(', '+' , '-', 'EOF'}
    
    OpTerm -> TIMES Factor   LA = {'*'}
            | DIVIDE Factor  LA = {'/'}
            | &              LA = {'+', '-', ')', 'EOF'}
    
    Factor -> '(' Expr ')'    LA = {'('}
            | NUMBER         LA = {'NUMBER'}
}





"""
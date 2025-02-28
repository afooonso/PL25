import ply.lex as lex

tokens = (
    'SELECT', 'WHERE',
    'VAR',      # ?variáveis (ex: ?s, ?w, ?nome)
    'LITERAL',  # "Chuck Berry"@en
    'IRI',      # dbo:MusicalArtist, dbo:artist etc.
    'A',        # a
    'OPEN_CURLY', 'CLOSE_CURLY',  # { }
    'DOT', 'COLON'  # . e :
)


t_SELECT = r'SELECT'
t_WHERE = r'WHERE'
t_A = r'a'  
t_OPEN_CURLY = r'\{'
t_CLOSE_CURLY = r'\}'
t_DOT = r'\.'
t_COLON = r':'

def t_VAR(t):
    r'\?[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_LITERAL(t):
    r'\"[^\"]*\"@[a-zA-Z]+'
    return t

def t_IRI(t):
    r'[a-zA-Z_][a-zA-Z0-9_-]*:[a-zA-Z_][a-zA-Z0-9_-]*'
    return t


t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Ilegal character: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()

data = '''SELECT ?nome ?desc WHERE {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en.
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc.
}
'''

lexer.input(data)

for tok in lexer:
    print(tok)

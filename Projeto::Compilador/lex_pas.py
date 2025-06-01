
import ply.lex as lex
from ply.lex import TOKEN

tokens = (
    'cCHAR', 'cINTEGER', 'cREAL', 'cBOO', 'cSTRING', 
    'oLP', 'oRP', 'oLB', 'oRB', 'oPLUS', 'oMINUS',
    'oMUL', 'oDIV', 'oASSIGN', 'oEQUAL', 'oLT', 'oGT', 
    'oLE', 'oGE', 'oUNEQU', 'oCOMMA', 'oSEMI',
    'oCOLON', 'oDOTDOT', 'oDOT',
    'yNAME', 'kDOWNTO',
    'kAND', 'kARRAY', 'kBEGIN', 'kDO', 'kELSE', 'kEND',
    'kFOR', 'kIF', 'kMOD', 'kNOT', 'kOF', 'kOR',
    'kPROGRAM', 'kTHEN', 'kTO', 'kVAR', 'kWHILE', 'kDIV',
    'SYS_FUNCT', 'SYS_PROC', 'SYS_TYPE'
)

t_oLP = r'\('
t_oRP = r'\)'
t_oLB = r'\['
t_oRB = r'\]'
t_oPLUS = r'\+'
t_oMINUS = r'-'
t_oMUL = r'\*'
t_oDIV = r'/'
t_oASSIGN = r':='
t_oEQUAL = r'='
t_oLT = r'<'
t_oGT = r'>'
t_oLE = r'<='
t_oGE = r'>='
t_oUNEQU = r'<>'
t_oCOMMA = r','
t_oSEMI = r';'
t_oCOLON = r':'
t_oDOTDOT = r'\.\.'
t_oDOT = r'\.'

t_ignore = ' \t\x0c'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\{[^}]*\}'
    pass

def t_cCHAR(t):
    r"'([^']|\\')'"
    t.value = t.value[1:-1]
    return t

def t_cSTRING(t):
    r"'([^']|\\')*'"
    t.value = t.value[1:-1]
    return t

def t_cBOO(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

@TOKEN(r'[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?')
def t_cREAL(t):
    t.value = float(t.value)
    return t

@TOKEN(r'[1-9][0-9]*|0[0-7]*|0[xX][0-9a-fA-F]+')
def t_cINTEGER(t):
    if t.value.lower().startswith('0x'):
        t.value = int(t.value[2:], 16)
    elif t.value.startswith('0') and len(t.value) > 1:
        t.value = int(t.value, 8)
    else:
        t.value = int(t.value)
    return t



@TOKEN(r'(?i:abs|chr|odd|ord|pred|sqr|sqrt|succ|length)\b')
def t_SYS_FUNCT(t):
    t.value = t.value.lower()
    return t

@TOKEN(r'(?i:write|writeln|read|readln)\b')
def t_SYS_PROC(t):
    t.value = t.value.lower()
    return t

@TOKEN(r'(?i:boolean|char|integer|real)\b')
def t_SYS_TYPE(t):
    t.value = t.value.lower()
    return t

@TOKEN(r'(?i:and)\b')  
def t_kAND(t): return t
@TOKEN(r'(?i:array)\b')  
def t_kARRAY(t): return t
@TOKEN(r'(?i:begin)\b')   
def t_kBEGIN(t): return t
@TOKEN(r'(?i:do)\b')      
def t_kDO(t): return t
@TOKEN(r'(?i:else)\b')  
def t_kELSE(t): return t
@TOKEN(r'(?i:end)\b')   
def t_kEND(t): return t
@TOKEN(r'(?i:for)\b')   
def t_kFOR(t): return t
@TOKEN(r'(?i:if)\b')    
def t_kIF(t): return t
@TOKEN(r'(?i:mod)\b')   
def t_kMOD(t): return t
@TOKEN(r'(?i:not)\b')   
def t_kNOT(t): return t
@TOKEN(r'(?i:of)\b')   
def t_kOF(t): return t
@TOKEN(r'(?i:or)\b')     
def t_kOR(t): return t
@TOKEN(r'(?i:program)\b') 
def t_kPROGRAM(t): return t
@TOKEN(r'(?i:then)\b')  
def t_kTHEN(t): return t
@TOKEN(r'(?i:to)\b')    
def t_kTO(t): return t
@TOKEN(r'(?i:var)\b')    
def t_kVAR(t): return t
@TOKEN(r'(?i:while)\b')  
def t_kWHILE(t): return t
@TOKEN(r'(?i:div)\b')   
def t_kDIV(t): return t
@TOKEN(r'(?i:downto)\b') 
def t_kDOWNTO(t): return t

@TOKEN(r'[a-zA-Z_][a-zA-Z0-9_]*')
def t_yNAME(t):
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            data = file.read()
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
    except IndexError:
        print("Error: No input file provided. Usage: python lex_pas.py <filename>")
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")

import ply.yacc as yacc
from lex_pas import tokens, lexer
import ast_nodes as ast
from pascal_codegen import CodeGenerator

precedence = (
    ('left', 'kTHEN'),
    ('left', 'kELSE'),
)
def p_program(p):
    'program : kPROGRAM yNAME oSEMI program_block oDOT'
    p[0] = ast.Program(name=p[2], block=p[4])

def p_program_block(p):
    'program_block : declarations compound_statement'
    p[0] = ast.Block(declarations=p[1], compound_statement=p[2])

def p_declarations(p):
    '''declarations : var_declaration declarations
                   | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_var_declaration(p):
    'var_declaration : kVAR var_declaration_list oSEMI'
    p[0] = ast.VarDeclarations(declarations=p[2])

def p_var_declaration_list(p):
    '''var_declaration_list : var_declaration_item
                            | var_declaration_list oSEMI var_declaration_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_var_declaration_item(p):
    'var_declaration_item : name_list oCOLON type_spec'
    p[0] = ast.VarDeclaration(names=p[1], type=p[3])

def p_name_list(p):
    '''name_list : yNAME
                | name_list oCOMMA yNAME'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type_spec(p):
    '''type_spec : SYS_TYPE
                 | yNAME
                 | array_type'''
    p[0] = p[1]

def p_array_type(p):
    'array_type : kARRAY oLB index_range oRB kOF type_spec'
    p[0] = ast.ArrayType(index_range=p[3], element_type=p[6])

def p_index_range(p):
    'index_range : expression oDOTDOT expression'
    p[0] = ast.IndexRange(lower=p[1], upper=p[3])

def p_compound_statement(p):
    'compound_statement : kBEGIN statement_list kEND'
    p[0] = ast.Compound(statements=p[2])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list oSEMI statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_statement(p):
    '''statement : if_statement
                 | assignment_statement
                 | procedure_call
                 | compound_statement
                 | while_statement
                 | for_statement
                 | empty'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : kIF expression kTHEN statement %prec kTHEN
                   | kIF expression kTHEN statement else_part'''
    if len(p) == 5:
        p[0] = ast.IfStatement(condition=p[2], then_part=p[4], else_part=None)
    else:
        p[0] = ast.IfStatement(condition=p[2], then_part=p[4], else_part=p[5])

def p_else_part(p):
    '''else_part : kELSE statement'''
    p[0] = p[2]

def p_assignment_statement(p):
    'assignment_statement : lvalue oASSIGN expression'
    p[0] = ast.Assignment(left=p[1], right=p[3])

def p_procedure_call(p):
    '''procedure_call : yNAME
                      | SYS_PROC oLP argument_list oRP
                      | SYS_PROC'''
    if len(p) == 2:
        if p[1].lower() == 'readln':
            p[0] = ast.ReadlnAssignment(target=None)
        else:
            p[0] = ast.ProcedureCall(name=p[1], args=[])
    elif len(p) == 5:
        if p[1].lower() == 'readln':
            if len(p[3]) == 1:
                p[0] = ast.ReadlnAssignment(target=p[3][0])
            else:
                assignments = [ast.ReadlnAssignment(target=arg) for arg in p[3]]
                p[0] = ast.Compound(statements=assignments)
        else:
            p[0] = ast.ProcedureCall(name=p[1], args=p[3])
    else:
        if p[1].lower() == 'readln':
            p[0] = ast.ReadlnAssignment(target=None)
        else:
            p[0] = ast.ProcedureCall(name=p[1], args=[])

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list oCOMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_while_statement(p):
    'while_statement : kWHILE expression kDO statement'
    p[0] = ast.WhileStatement(condition=p[2], body=p[4])

def p_for_statement(p):
    'for_statement : kFOR yNAME oASSIGN expression direction expression kDO statement'
    p[0] = ast.ForStatement(var_name=p[2], start_value=p[4], end_value=p[6], body=p[8], direction=p[5])

def p_direction(p):
    '''direction : kTO
                 | kDOWNTO'''
    p[0] = p[1].lower()

def p_expression(p):
    '''expression : simple_expression
                  | simple_expression relop simple_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast.BinaryOp(left=p[1], op=p[2], right=p[3])

def p_relop(p):
    '''relop : oEQUAL
             | oUNEQU
             | oLT
             | oLE
             | oGT
             | oGE'''
    p[0] = p[1]

def p_simple_expression(p):
    '''simple_expression : term
                         | sign term
                         | simple_expression addop term'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ast.UnaryOp(op=p[1], expr=p[2])
    else:
        p[0] = ast.BinaryOp(left=p[1], op=p[2], right=p[3])

def p_sign(p):
    '''sign : oPLUS
            | oMINUS'''
    p[0] = p[1]

def p_addop(p):
    '''addop : oPLUS
             | oMINUS
             | kOR'''
    p[0] = p[1]

def p_term(p):
    '''term : factor
            | term mulop factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast.BinaryOp(left=p[1], op=p[2], right=p[3])

def p_mulop(p):
    '''mulop : oMUL
             | oDIV
             | kDIV
             | kMOD
             | kAND'''
    p[0] = p[1]

def p_lvalue(p):
    '''lvalue : yNAME
              | yNAME oLB expression oRB'''
    if len(p) == 2:
        p[0] = ast.Variable(name=p[1])
    else:
        p[0] = ast.ArrayAccess(array=ast.Variable(name=p[1]), index=p[3])

def p_factor(p):
    '''factor : lvalue
              | number
              | cBOO
              | char_literal
              | string
              | oLP expression oRP
              | kNOT factor
              | SYS_FUNCT oLP argument_list oRP
              | SYS_FUNCT'''
    if len(p) == 5 and p.slice[1].type == 'SYS_FUNCT':
        p[0] = ast.FunctionCall(name=p[1], args=p[3])
    elif len(p) == 2:
        if isinstance(p[1], ast.Node):
            p[0] = p[1]
        elif p.slice[1].type == 'cBOO':
            p[0] = ast.Boolean(value=p[1])
        elif p.slice[1].type == 'SYS_FUNCT':
            p[0] = ast.FunctionCall(name=p[1], args=[])
        else:
            p[0] = ast.Variable(name=p[1])
    elif len(p) == 3:
        p[0] = ast.UnaryOp(op=p[1], expr=p[2])
    elif len(p) == 4:
        p[0] = p[2]

def p_number(p):
    '''number : cINTEGER
              | cREAL'''
    if p.slice[1].type == 'cINTEGER':
        p[0] = ast.Number(value=int(p[1]))
    else:
        p[0] = ast.Number(value=float(p[1]))


def p_string(p):
    'string : cSTRING'
    p[0] = ast.String(value=p[1])

def p_char_literal(p):
    'char_literal : cCHAR'
    p[0] = ast.CharLiteral(p[1])

def p_empty(p):
    'empty :'
    p[0] = ast.NoOp()

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(write_tables=False)

if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
        result = parser.parse(data, lexer=lexer)
        print("\n" + "="*50)
        print(ast.pretty_print_ast(result))
        print("\nAST Graph:")
        dot = result.graphviz()
        dot.render('ast_graph', format='png', cleanup=True)
        print("AST graph saved as 'ast_graph.png'")
        print("\n" + "="*50)
        generator = CodeGenerator()
        generator.generate(result)
        machine_code = generator.get_code()
        print("Generated Machine Code:")
        print("="*50)
        with open('output.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(machine_code)
        print("Machine code written to 'output.txt'")
    except IndexError:
        print("Error: No input file provided. Usage: python yacc_pas.py <filename>")
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")

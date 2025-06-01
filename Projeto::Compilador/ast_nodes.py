import uuid
class Node:
    pass

class Program(Node):
    def __init__(self, name, block):
        self.name = name
        self.block = block
    
    def __repr__(self):
        return f"Program({self.name}, {self.block})"
    
    def graphviz(self, dot=None, parent_id=None):
        import graphviz
        if dot is None:
            dot = graphviz.Digraph()
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"Program: {self.name}")
        self.block.graphviz(dot, node_id)
        return dot

class Block(Node):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement
    
    def __repr__(self):
        return f"Block(declarations={self.declarations}, statements={self.compound_statement})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "Block")
        dot.edge(parent_id, node_id)
        for decl in self.declarations:
            decl.graphviz(dot, node_id)
        self.compound_statement.graphviz(dot, node_id)
        return dot

class VarDeclarations(Node):
    def __init__(self, declarations):
        self.declarations = declarations
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "VarDeclarations")
        dot.edge(parent_id, node_id)
        for decl in self.declarations:
            decl.graphviz(dot, node_id)
        return dot
    
    def __repr__(self):
        return f"VarDeclarations({self.declarations})"

class VarDeclaration(Node):
    def __init__(self, names, type):
        self.names = names
        self.type = type
    
    def __repr__(self):
        return f"VarDeclaration(names={self.names}, type={self.type})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"VarDeclaration: {', '.join(self.names)}")
        dot.edge(parent_id, node_id)

        if isinstance(self.type, Node):
            self.type.graphviz(dot, node_id)
        else:
            type_id = str(uuid.uuid4())
            dot.node(type_id, f"Type: {self.type}")
            dot.edge(node_id, type_id)

        return dot


class Type(Node):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Type({self.name})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"Type: {self.name}")
        dot.edge(parent_id, node_id)
        return dot

class Compound(Node):
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Compound({self.statements})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "Compound")
        dot.edge(parent_id, node_id)
        for stmt in self.statements:
            stmt.graphviz(dot, node_id)
        return dot

class Assignment(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Assignment({self.left} := {self.right})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "Assignment")
        dot.edge(parent_id, node_id)
        self.left.graphviz(dot, node_id)
        self.right.graphviz(dot, node_id)
        return dot

class Variable(Node):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Variable({self.name})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"Variable: {self.name}")
        dot.edge(parent_id, node_id)
        return dot

class ProcedureCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"ProcedureCall({self.name}, {self.args})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"ProcedureCall: {self.name}")
        dot.edge(parent_id, node_id)
        for arg in self.args:
            arg.graphviz(dot, node_id)
        return dot

class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name.lower()  # Normaliza o nome
        self.args = args
    
    def __repr__(self):
        return f"FunctionCall({self.name}, args={self.args})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"FunctionCall: {self.name.upper()}")
        dot.edge(parent_id, node_id)
        for arg in self.args:
            arg.graphviz(dot, node_id)
        return dot
    
    def pretty_print(self, indent=0):
        spaces = '  ' * indent
        print(f"{spaces}{self.name.upper()}Call:")
        if self.args:
            print(f"{spaces}  Arguments:")
            for arg in self.args:
                arg.pretty_print(indent + 2)

class IfStatement(Node):
    def __init__(self, condition, then_part, else_part=None):
        self.condition = condition
        self.then_part = then_part
        self.else_part = else_part
    
    def __repr__(self):
        return f"If({self.condition}, then={self.then_part}, else={self.else_part})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "IfStatement")
        dot.edge(parent_id, node_id)
        
        # Condition
        cond_id = str(uuid.uuid4())
        dot.node(cond_id, "Condition")
        dot.edge(node_id, cond_id)
        self.condition.graphviz(dot, cond_id)
        
        # Then part
        then_id = str(uuid.uuid4())
        dot.node(then_id, "Then")
        dot.edge(node_id, then_id)
        self.then_part.graphviz(dot, then_id)
        
        # Else part if exists
        if self.else_part:
            else_id = str(uuid.uuid4())
            dot.node(else_id, "Else")
            dot.edge(node_id, else_id)
            self.else_part.graphviz(dot, else_id)
        
        return dot

class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"While({self.condition}, do={self.body})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "WhileStatement")
        dot.edge(parent_id, node_id)
        
        # Condition
        cond_id = str(uuid.uuid4())
        dot.node(cond_id, "Condition")
        dot.edge(node_id, cond_id)
        self.condition.graphviz(dot, cond_id)
        
        # Body
        body_id = str(uuid.uuid4())
        dot.node(body_id, "Body")
        dot.edge(node_id, body_id)
        self.body.graphviz(dot, body_id)
        
        return dot

class ForStatement(Node):
    def __init__(self, var_name, start_value, end_value, body, direction):
        self.var_name = var_name
        self.start_value = start_value
        self.end_value = end_value
        self.body = body
        self.direction = direction
    
    def __repr__(self):
        return f"For({self.var_name} from {self.start_value} to {self.end_value}, do={self.body})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"ForStatement: {self.var_name} ({self.direction})")
        dot.edge(parent_id, node_id)
        
        # Start value
        start_id = str(uuid.uuid4())
        dot.node(start_id, "Start")
        dot.edge(node_id, start_id)
        self.start_value.graphviz(dot, start_id)
        
        # End value
        end_id = str(uuid.uuid4())
        dot.node(end_id, "End")
        dot.edge(node_id, end_id)
        self.end_value.graphviz(dot, end_id)
        
        # Body
        body_id = str(uuid.uuid4())
        dot.node(body_id, "Body")
        dot.edge(node_id, body_id)
        self.body.graphviz(dot, body_id)
        
        return dot

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"BinaryOp: {self.op}")
        dot.edge(parent_id, node_id)
        self.left.graphviz(dot, node_id)
        self.right.graphviz(dot, node_id)
        return dot

class UnaryOp(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    
    def __repr__(self):
        return f"UnaryOp({self.op}{self.expr})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"UnaryOp: {self.op}")
        dot.edge(parent_id, node_id)
        self.expr.graphviz(dot, node_id)
        return dot

class Number(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"Number: {self.value}")
        dot.edge(parent_id, node_id)
        return dot

class String(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"String('{self.value}')"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"String: '{self.value}'")
        dot.edge(parent_id, node_id)
        return dot
    
class CharLiteral(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"CharLiteral('{self.value}')"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"Char: '{self.value}'")
        dot.edge(parent_id, node_id)
        return dot

class ArrayAccess(Node):
    def __init__(self, array, index):
        self.array = array
        self.index = index
    
    def __repr__(self):
        return f"ArrayAccess({self.array}[{self.index}])"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "ArrayAccess")
        dot.edge(parent_id, node_id)
        self.array.graphviz(dot, node_id)
        self.index.graphviz(dot, node_id)
        return dot

class NoOp(Node):
    def __repr__(self):
        return "NoOp()"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "NoOp")
        if parent_id is not None:
            dot.edge(parent_id, node_id)
        return dot
    
class Boolean(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Boolean({self.value})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, f"Boolean: {self.value}")
        if parent_id is not None:
            dot.edge(parent_id, node_id)
        return dot
    
class ArrayType(Node):
    def __init__(self, index_range, element_type):
        self.index_range = index_range
        self.element_type = element_type
    
    def __repr__(self):
        return f"ArrayType[{self.index_range} of {self.element_type}]"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "ArrayType")
        if parent_id:
            dot.edge(parent_id, node_id)
        
        self.index_range.graphviz(dot, node_id)

        if isinstance(self.element_type, Node):
            self.element_type.graphviz(dot, node_id)
        else:
            elem_id = str(uuid.uuid4())
            dot.node(elem_id, f"ElementType: {self.element_type}")
            dot.edge(node_id, elem_id)

        return dot

class IndexRange(Node):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
    
    def __repr__(self):
        return f"IndexRange({self.lower}..{self.upper})"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "IndexRange")
        if parent_id:
            dot.edge(parent_id, node_id)
        self.lower.graphviz(dot, node_id)
        self.upper.graphviz(dot, node_id)
        return dot

class ReadlnAssignment(Node):
    def __init__(self, target):
        self.target = target  # Pode ser None (readln sem argumentos)
    
    def __repr__(self):
        if self.target:
            return f"ReadlnAssignment(target={self.target})"
        return "ReadlnAssignment()"
    
    def graphviz(self, dot, parent_id):
        node_id = str(uuid.uuid4())
        dot.node(node_id, "Readln")
        if parent_id:
            dot.edge(parent_id, node_id)
        if self.target:
            self.target.graphviz(dot, node_id)
        return dot
    
    def pretty_print(self, indent=0):
        spaces = '  ' * indent
        print(f"{spaces}Readln ->")
        if self.target:
            print(f"{spaces}  Target:")
            self.target.pretty_print(indent + 2)

# ... [rest of your pretty_print_ast function remains the same]
    
def pretty_print_ast(node, indent=0):
    """Recursive pretty printer for AST nodes"""
    spaces = '  ' * indent
    if isinstance(node, Program):
        print(f"{spaces}Program: {node.name}")
        pretty_print_ast(node.block, indent+1)
    elif isinstance(node, Block):
        print(f"{spaces}Block:")
        print(f"{spaces}  Declarations:")
        for decl in node.declarations:
            pretty_print_ast(decl, indent+2)
        print(f"{spaces}  Statements:")
        pretty_print_ast(node.compound_statement, indent+2)
    elif isinstance(node, VarDeclarations):
        print(f"{spaces}VarDeclarations:")
        for decl in node.declarations:
            pretty_print_ast(decl, indent+1)
    elif isinstance(node, VarDeclaration):
        names = ', '.join(node.names)
        print(f"{spaces}VarDeclaration: {names} : {node.type}")
    elif isinstance(node, Type):
        print(f"{spaces}Type: {node.name}")
    elif isinstance(node, Compound):
        print(f"{spaces}Compound:")
        for stmt in node.statements:
            pretty_print_ast(stmt, indent+1)
    elif isinstance(node, Assignment):
        print(f"{spaces}Assignment:")
        print(f"{spaces}  Left:")
        pretty_print_ast(node.left, indent+2)
        print(f"{spaces}  Right:")
        pretty_print_ast(node.right, indent+2)
    elif isinstance(node, Variable):
        print(f"{spaces}Variable: {node.name}")
    elif isinstance(node, ProcedureCall):
        print(f"{spaces}ProcedureCall: {node.name}")
        print(f"{spaces}  Arguments:")
        for arg in node.args:
            pretty_print_ast(arg, indent+2)
    elif isinstance(node, FunctionCall):
        print(f"{spaces}FunctionCall: {node.name}")
        print(f"{spaces}  Arguments:")
        for arg in node.args:
            pretty_print_ast(arg, indent+2)
    elif isinstance(node, IfStatement):
        print(f"{spaces}IfStatement:")
        print(f"{spaces}  Condition:")
        pretty_print_ast(node.condition, indent+2)
        print(f"{spaces}  Then:")
        pretty_print_ast(node.then_part, indent+2)
        if node.else_part:
            print(f"{spaces}  Else:")
            pretty_print_ast(node.else_part, indent+2)
    elif isinstance(node, WhileStatement):
        print(f"{spaces}WhileStatement:")
        print(f"{spaces}  Condition:")
        pretty_print_ast(node.condition, indent+2)
        print(f"{spaces}  Body:")
        pretty_print_ast(node.body, indent+2)
    elif isinstance(node, ForStatement):
        print(f"{spaces}ForStatement:")
        print(f"{spaces}  Variable: {node.var_name}")
        print(f"{spaces}  Start:")
        pretty_print_ast(node.start_value, indent+2)
        print(f"{spaces}  End:")
        pretty_print_ast(node.end_value, indent+2)
        print(f"{spaces}  Direction: {node.direction}")
        print(f"{spaces}  Body:")
        pretty_print_ast(node.body, indent+2)
    elif isinstance(node, BinaryOp):
        print(f"{spaces}BinaryOp: {node.op}")
        print(f"{spaces}  Left:")
        pretty_print_ast(node.left, indent+2)
        print(f"{spaces}  Right:")
        pretty_print_ast(node.right, indent+2)
    elif isinstance(node, UnaryOp):
        print(f"{spaces}UnaryOp: {node.op}")
        print(f"{spaces}  Expression:")
        pretty_print_ast(node.expr, indent+2)
    elif isinstance(node, Number):
        print(f"{spaces}Number: {node.value}")
    elif isinstance(node, String):
        print(f"{spaces}String: '{node.value}'")
    elif isinstance(node, ArrayAccess):
            print(f"{spaces}ArrayAccess:")
            print(f"{spaces}  Array:")
            if isinstance(node.array, str):  # Handle case where array is still a string
                print(f"{spaces}    Variable: {node.array}")
            else:
                pretty_print_ast(node.array, indent+2)
            print(f"{spaces}  Index:")
            pretty_print_ast(node.index, indent+2)
    elif isinstance(node, ArrayType):
        print(f"{spaces}ArrayType:")
        print(f"{spaces}  Index Range:")
        pretty_print_ast(node.index_range, indent+2)
        print(f"{spaces}  Element Type:")
        pretty_print_ast(node.element_type, indent+2)
    elif isinstance(node, IndexRange):
        print(f"{spaces}IndexRange:")
        print(f"{spaces}  Lower:")
        pretty_print_ast(node.lower, indent+2)
        print(f"{spaces}  Upper:")
        pretty_print_ast(node.upper, indent+2)
    elif isinstance(node, Boolean):
        print(f"{spaces}Boolean: {node.value}")
    elif isinstance(node, NoOp):
        print(f"{spaces}NoOp")
    
    elif isinstance(node, ReadlnAssignment):
        print(f"{spaces}Readln ->")
        if node.target:
            print(f"{spaces}  Target:")
            pretty_print_ast(node.target, indent + 2)
        else:
            print(f"{spaces}  (no target)")
    else:
        print(f"{spaces}Unknown node type: {type(node)}")
        
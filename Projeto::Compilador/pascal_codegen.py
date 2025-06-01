import ast_nodes as ast

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0
        self.var_offset = 0
        self.symbol_table = {}
        self.type_info = {}
        self.array_info = {}
        self.string_info = {}
        self.heap_allocated = False
        self.string_constants = {}
        self.next_string_id = 0

    def generate(self, node):
        if isinstance(node, ast.Program):
            self.generate_program(node)
        elif isinstance(node, ast.Block):
            self.generate_block(node)
        elif isinstance(node, ast.VarDeclarations):
            self.generate_var_declarations(node)
        elif isinstance(node, ast.VarDeclaration):
            self.generate_var_declaration(node)
        elif isinstance(node, ast.Compound):
            self.generate_compound(node)
        elif isinstance(node, ast.Assignment):
            self.generate_assignment(node)
        elif isinstance(node, ast.Variable):
            self.generate_variable(node)
        elif isinstance(node, ast.ArrayAccess):
            self.generate_array_access(node)
        elif isinstance(node, ast.ProcedureCall):
            self.generate_procedure_call(node)
        elif isinstance(node, ast.FunctionCall):
            self.generate_function_call(node)
        elif isinstance(node, ast.IfStatement):
            self.generate_if_statement(node)
        elif isinstance(node, ast.WhileStatement):
            self.generate_while_statement(node)
        elif isinstance(node, ast.ForStatement):
            self.generate_for_statement(node)
        elif isinstance(node, ast.BinaryOp):
            self.generate_binary_op(node)
        elif isinstance(node, ast.UnaryOp):
            self.generate_unary_op(node)
        elif isinstance(node, ast.Number):
            self.generate_number(node)
        elif isinstance(node, ast.String):
            self.generate_string(node)
        elif isinstance(node, ast.Boolean):
            self.generate_boolean(node)
        elif isinstance(node, ast.CharLiteral):
            self.generate_char_literal(node)
        elif isinstance(node, ast.NoOp):
            pass
        elif isinstance(node, ast.ReadlnAssignment):
            self.generate_readln_assignment(node)
        elif isinstance(node, list):
            for item in node:
                self.generate(item)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")
        return self.code

    def generate_program(self, node):
        self.generate(node.block)

    def generate_block(self, node):
        if node.declarations:
            self.generate(node.declarations)
        self.code.append("start")
        if node.compound_statement:
            self.generate(node.compound_statement)
        self.code.append("stop")

    def generate_var_declarations(self, node):
        for decl in node.declarations:
            self.generate(decl)

    def generate_var_declaration(self, node):
        var_type = node.type.name.lower() if isinstance(node.type, ast.Type) else str(node.type).lower()
        
        for name in node.names:
            if isinstance(node.type, ast.ArrayType):
                lower = node.type.index_range.lower.value
                upper = node.type.index_range.upper.value
                size = upper - lower + 1
                
                # Array allocation
                self.code.append(f"pushi {size}")
                self.code.append("allocn")
                self.code.append(f"storeg {self.var_offset}")
                
                self.array_info[name] = {
                    'pointer_offset': self.var_offset,
                    'lower_bound': lower,
                    'size': size,
                    'element_type': node.type.element_type.name.lower() if isinstance(node.type.element_type, ast.Type) else 'integer'
                }
                self.heap_allocated = True
                self.symbol_table[name] = self.var_offset
                self.type_info[name] = 'array'
                self.var_offset += 1
            else:
                self.symbol_table[name] = self.var_offset
                self.type_info[name] = var_type
                
                if var_type == 'integer':
                    self.code.append("pushi 0")
                elif var_type == 'real':
                    self.code.append("pushf 0.0")
                elif var_type == 'boolean':
                    self.code.append("pushi 0")
                elif var_type == 'string':
                    self.code.append("pushs \"\"")
                    self.string_info[name] = self.var_offset
                elif var_type == 'char':
                    self.code.append("pushs \"\0\"")
                else:
                    self.code.append("pushi 0")
                
                self.code.append(f"storeg {self.var_offset}")
                self.var_offset += 1

    def generate_compound(self, node):
        for stmt in node.statements:
            self.generate(stmt)

    def generate_char_literal(self, node):
        self.code.append(f"pushs \"{node.value}\"")

    def generate_binary_op(self, node):
        left_is_string_access = isinstance(node.left, ast.ArrayAccess) and node.left.array.name in self.string_info
        right_is_char = isinstance(node.right, (ast.CharLiteral, ast.Variable)) and self._get_expression_type(node.right) == 'char'
        
        right_is_string_access = isinstance(node.right, ast.ArrayAccess) and node.right.array.name in self.string_info
        left_is_char = isinstance(node.left, (ast.CharLiteral, ast.Variable)) and self._get_expression_type(node.left) == 'char'

        if left_is_string_access and right_is_char:
            self.generate(node.left)
            if isinstance(node.right, ast.CharLiteral):
                self.code.append(f"pushi {ord(node.right.value)}")
            else:
                self.code.append(f"pushg {self.symbol_table[node.right.name]}")
                self.code.append("pushi 0")
                self.code.append("charat")
        elif right_is_string_access and left_is_char:
            if isinstance(node.left, ast.CharLiteral):
                self.code.append(f"pushi {ord(node.left.value)}")
            else:
                self.code.append(f"pushg {self.symbol_table[node.left.name]}")
                self.code.append("pushi 0")
                self.code.append("charat")
            self.generate(node.right)
        else:
            self.generate(node.left)
            self.generate(node.right)

        if node.op in ['=', '<>', '<', '<=', '>', '>=']:
            op_map = {
                '=': 'equal',
                '<>': 'equal\nnot',
                '<': 'inf',
                '<=': 'infeq',
                '>': 'sup',
                '>=': 'supeq'
            }
            self.code.append(op_map[node.op])
        else:
            left_type = self._get_expression_type(node.left)
            right_type = self._get_expression_type(node.right)
            use_float = (left_type == 'real' or right_type == 'real')
            
            op_map = {
                '+': 'fadd' if use_float else 'add',
                '-': 'fsub' if use_float else 'sub',
                '*': 'fmul' if use_float else 'mul',
                '/': 'fdiv' if use_float else 'div',
                'div': 'div',
                'mod': 'mod',
                'and': 'and',
                'or': 'or'
            }
            if node.op in op_map:
                self.code.append(op_map[node.op])

    def generate_assignment(self, node):
        left_type = self._get_expression_type(node.left)
        right_type = self._get_expression_type(node.right)

        if left_type != right_type:
            # Permitir atribuição de boolean := true/false
            if left_type == 'boolean' and isinstance(node.right, ast.Boolean):
                pass
            # Permitir char := 'c'
            elif left_type == 'char' and isinstance(node.right, ast.CharLiteral):
                pass
            # Permitir real := integer → mas assume que o número já vem como float no AST (sem itof aqui!)
            elif left_type == 'real' and right_type == 'integer':
                pass  # assume que generate_number já fez pushf
            else:
                raise TypeError(f"Incompatible types in assignment: {left_type} := {right_type}")


        # Handle char variable assignment
        if isinstance(node.left, ast.Variable) and left_type == 'char':
            if isinstance(node.right, ast.CharLiteral):
                self.generate_char_literal(node.right)
            else:
                self.generate(node.right)
            self.code.append(f"storeg {self.symbol_table[node.left.name]}")
            return

        # Generate the right-hand side value first (except for array assignments)
        if not isinstance(node.left, ast.ArrayAccess):
            if isinstance(node.right, ast.CharLiteral):
                self.generate_char_literal(node.right)
            else:
                self.generate(node.right)

        # Handle variable assignment
        if isinstance(node.left, ast.Variable):
            offset = self.symbol_table[node.left.name]
            var_type = self.type_info.get(node.left.name, 'integer')
            self.code.append(f"storeg {offset}")

        # Handle array assignment
        elif isinstance(node.left, ast.ArrayAccess):
            array_name = node.left.array.name

            # First push array base address
            if array_name in self.array_info:
                self.code.append(f"pushg {self.array_info[array_name]['pointer_offset']}")
            elif array_name in self.string_info:
                self.code.append(f"pushg {self.symbol_table[array_name]}")
            else:
                raise ValueError(f"Unknown array/string: {array_name}")

            # Then push index (with lower bound adjustment if needed)
            self.generate(node.left.index)
            if array_name in self.array_info and self.array_info[array_name]['lower_bound'] != 0:
                self.code.append(f"pushi {self.array_info[array_name]['lower_bound']}")
                self.code.append("sub")

            # For array assignment, generate the value after pushing array and index
            if isinstance(node.right, ast.CharLiteral):
                self.generate_char_literal(node.right)
                if array_name in self.string_info:
                    self.code.append(f"pushi {ord(node.right.value)}")
            else:
                self.generate(node.right)

            # Perform the store operation
            if array_name in self.array_info:
                self.code.append("storen")
            elif array_name in self.string_info:
                if not isinstance(node.right, ast.CharLiteral):
                    self.code.append("chr")  # Convert to ASCII if needed
                self.code.append("setcharat")


    def generate_variable(self, node):
        if node.name not in self.symbol_table:
            if node.name.isdigit():
                self.code.append(f"pushi {node.name}")
                return
            raise ValueError(f"Undeclared variable: {node.name}")
            
        offset = self.symbol_table[node.name]
        var_type = self.type_info.get(node.name, 'integer')
        
        if var_type == 'char':
            self.code.append(f"pushg {offset}")
        else:
            self.code.append(f"pushg {offset}")

    def generate_array_access(self, node):
        array_name = node.array.name

        if array_name in self.string_info:
            self.code.append(f"pushg {self.symbol_table[array_name]}")
            self.generate(node.index)
            self.code.append("pushi 1")
            self.code.append("sub")
            self.code.append("charat")
        elif array_name in self.array_info:
            array_data = self.array_info[array_name]
            self.code.append(f"pushg {array_data['pointer_offset']}")
            self.generate(node.index)
            if array_data['lower_bound'] != 0:
                self.code.append(f"pushi {array_data['lower_bound']}")
                self.code.append("sub")
            self.code.append("loadn")
        else:
            raise ValueError(f"Unknown array/string: {array_name}")


    def generate_procedure_call(self, node):
        proc_name = node.name.lower()
        
        if proc_name in ['writeln', 'write']:
            for arg in node.args:
                if isinstance(arg, ast.CharLiteral):
                    self.generate_char_literal(arg)
                else:
                    self.generate(arg)
                
                if isinstance(arg, ast.String):
                    self.code.append("writes")
                elif isinstance(arg, ast.Boolean):
                    self.code.append("writei")
                elif isinstance(arg, ast.Number):
                    self.code.append("writei")
                elif isinstance(arg, ast.CharLiteral):
                    self.code.append("writechr")
                else:
                    var_type = self._get_expression_type(arg)
                    if var_type == 'string':
                        self.code.append("writes")
                    elif var_type == 'char':
                        self.code.append("writechr")
                    else:
                        self.code.append("writei")
            
            if proc_name == 'writeln':
                self.code.append("writeln")
        elif proc_name == 'readln':
            if node.args and len(node.args) > 0:
                target = node.args[0]
                if isinstance(target, ast.ArrayAccess):
                    array_name = target.array.name
                    if array_name in self.array_info:
                        self.code.append(f"pushg {self.array_info[array_name]['pointer_offset']}")
                        self.generate(target.index)
                        if self.array_info[array_name]['lower_bound'] != 0:
                            self.code.append(f"pushi {self.array_info[array_name]['lower_bound']}")
                            self.code.append("sub")
                        self.code.append("read")
                        element_type = self.array_info[array_name]['element_type']
                        if element_type == 'integer':
                            self.code.append("atoi")
                        elif element_type == 'real':
                            self.code.append("atof")
                        self.code.append("storen")
                    elif array_name in self.string_info:
                        self.code.append(f"pushg {self.symbol_table[array_name]}")
                        self.generate(target.index)
                        self.code.append("read")
                        self.code.append("setcharat")
                elif isinstance(target, ast.Variable):
                    var_type = self.type_info.get(target.name, 'integer')
                    self.code.append("read")
                    if var_type == 'string':
                        self.code.append(f"storeg {self.symbol_table[target.name]}")
                    elif var_type == 'real':
                        self.code.append("atof")
                        self.code.append(f"storeg {self.symbol_table[target.name]}")
                    else:
                        self.code.append("atoi")
                        self.code.append(f"storeg {self.symbol_table[target.name]}")

    def generate_function_call(self, node):
        func_name = node.name.lower()
        
        if len(node.args) > 0:
            self.generate(node.args[0])
        
        if func_name == 'length':
            arg = node.args[0]
            if isinstance(arg, ast.Variable):
                if arg.name in self.string_info:
                    self.code.append("strlen")
                elif arg.name in self.array_info:
                    self.code.append(f"pushi {self.array_info[arg.name]['size']}")
                else:
                    raise ValueError(f"Cannot get length of non-string/array variable: {arg.name}")
            elif isinstance(arg, ast.String):
                self.code.append(f"pushi {len(arg.value)}")
            else:
                raise ValueError("Length function can only be applied to strings or arrays")
        elif func_name == 'chr':
            self.code.append("writechr")
        elif func_name == 'ord':
            pass
        elif func_name == 'pred':
            self.code.append("pushi 1")
            self.code.append("sub")
        elif func_name == 'succ':
            self.code.append("pushi 1")
            self.code.append("add")
        elif func_name == 'abs':
            label = f"ABSSKIPNEG{self.label_count}"
            self.label_count += 1
            self.code.append("dup 1")
            self.code.append("pushi 0")
            self.code.append("inf")
            self.code.append(f"jz {label}")
            self.code.append("neg")
            self.code.append(f"{label}:")
        elif func_name == 'odd':
            self.code.append("pushi 2")
            self.code.append("mod")
            self.code.append("pushi 0")
            self.code.append("equal")
            self.code.append("not")
        elif func_name == 'sqr':
            self.code.append("dup 1")
            self.code.append("mul")
        elif func_name == 'sqrt':
            self.code.append("itof")
            self.code.append("fsqrt")

    def generate_readln_assignment(self, node):
        if isinstance(node.target, ast.ArrayAccess):
            array_name = node.target.array.name
            if array_name in self.array_info:
                # Push array address and index first
                self.code.append(f"pushg {self.array_info[array_name]['pointer_offset']}")
                self.generate(node.target.index)
                if self.array_info[array_name]['lower_bound'] != 0:
                    self.code.append(f"pushi {self.array_info[array_name]['lower_bound']}")
                    self.code.append("sub")
                
                # Read input
                self.code.append("read")
                
                # Convert based on array element type
                element_type = self.array_info[array_name]['element_type']
                if element_type == 'integer':
                    self.code.append("atoi")
                elif element_type == 'real':
                    self.code.append("atof")
                
                # Store the value
                self.code.append("storen")
            elif array_name in self.string_info:
                # Handle string character assignment
                self.code.append(f"pushg {self.symbol_table[array_name]}")
                self.generate(node.target.index)
                self.code.append("read")
                self.code.append("setcharat")
            else:
                raise ValueError(f"Unknown array/string: {array_name}")
        else:
            # Normal variable assignment
            self.code.append("read")
            if node.target:
                if isinstance(node.target, ast.Variable):
                    var_type = self.type_info.get(node.target.name, 'integer')
                    if var_type == 'string':
                        self.code.append(f"storeg {self.symbol_table[node.target.name]}")
                    elif var_type == 'real':
                        self.code.append("atof")
                        self.code.append(f"storeg {self.symbol_table[node.target.name]}")
                    else:
                        self.code.append("atoi")
                        self.code.append(f"storeg {self.symbol_table[node.target.name]}")

    def generate_if_statement(self, node):
        self.generate(node.condition)
        else_label = f"ELSE{self.label_count}"
        end_label = f"ENDIF{self.label_count}"
        self.code.append(f"jz {else_label}")
        self.generate(node.then_part)
        self.code.append(f"jump {end_label}")
        self.code.append(f"{else_label}:")
        if node.else_part:
            self.generate(node.else_part)
        self.code.append(f"{end_label}:")
        self.label_count += 1

    def generate_while_statement(self, node):
        start_label = f"WHILE{self.label_count}"
        end_label = f"ENDWHILE{self.label_count}"
        self.code.append(f"{start_label}:")
        self.generate(node.condition)
        self.code.append(f"jz {end_label}")
        self.generate(node.body)
        self.code.append(f"jump {start_label}")
        self.code.append(f"{end_label}:")
        self.label_count += 1

    def generate_for_statement(self, node):
        start_label = f"FOR{self.label_count}"
        end_label = f"ENDFOR{self.label_count}"

        # Inicializa a variável de controlo: i := start_value
        self.generate(ast.Assignment(
            left=ast.Variable(name=node.var_name),
            right=node.start_value
        ))

        self.code.append(f"{start_label}:")

        # IMPORTANTE: ordem correta de comparação
        # para "to": continua enquanto i <= end → termina quando i > end → sup
        # para "downto": continua enquanto i >= end → termina quando i < end → inf
        self.generate(ast.Variable(name=node.var_name))  # push i
        self.generate(node.end_value)                   # push end

        if node.direction == 'to':
            self.code.append("infeq")                     # i > end → TERMINA
            self.code.append(f"jz {end_label}")         # se i > end → salta
        else:
            self.code.append("supeq")                     # i < end → TERMINA
            self.code.append(f"jz {end_label}")         # se i < end → salta

        # Corpo do loop
        self.generate(node.body)

        # i := i + 1 (ou i - 1)
        self.generate(ast.Variable(name=node.var_name))
        self.code.append("pushi 1")
        if node.direction == 'to':
            self.code.append("add")
        else:
            self.code.append("sub")
        self.code.append(f"storeg {self.symbol_table[node.var_name]}")

        self.code.append(f"jump {start_label}")
        self.code.append(f"{end_label}:")
        self.label_count += 1


    def generate_unary_op(self, node):
        self.generate(node.expr)
        if node.op == '-':
            is_float = self._get_expression_type(node.expr) == 'real'
            if is_float:
                self.code.append("pushf -1.0")
                self.code.append("fmul")
            else:
                self.code.append("neg")
        elif node.op == 'not':
            self.code.append("not")

    def generate_number(self, node):
        if isinstance(node.value, float):
            self.code.append(f"pushf {node.value}")
        else:
            self.code.append(f"pushi {node.value}")


    def generate_string(self, node):
        if node.value not in self.string_constants:
            self.string_constants[node.value] = f"STR{self.next_string_id}"
            self.next_string_id += 1
        self.code.append(f'pushs "{node.value}"')

    def generate_boolean(self, node):
        self.code.append(f"pushi {1 if node.value else 0}")

    def _get_expression_type(self, node):
        if isinstance(node, ast.Number):
            return 'real' if isinstance(node.value, float) else 'integer'
        elif isinstance(node, ast.CharLiteral):
            return 'char'
        elif isinstance(node, ast.Variable):
            return self.type_info.get(node.name, 'integer')
        elif isinstance(node, ast.BinaryOp):
            left_type = self._get_expression_type(node.left)
            right_type = self._get_expression_type(node.right)
            return 'real' if 'real' in [left_type, right_type] else 'integer'
        elif isinstance(node, ast.ArrayAccess):
            array_name = node.array.name
            if array_name in self.array_info:
                return self.array_info[array_name]['element_type']
            elif array_name in self.string_info:
                return 'char'
            return 'integer'
        elif isinstance(node, ast.String):
            return 'string'
        return 'integer'

    def get_code(self):
        return "\n".join(self.code)
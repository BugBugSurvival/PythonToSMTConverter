# Author: Yixuan

import ast
import re

class PythonToSMTConverter:
    """
    PythonToSMTConverter converts a subset of Python code to SMT-LIB2 code.
    This class is designed to convert Python code containing mathematical expressions and simple control
    flow structures into equivalent SMT-LIB2 format.

    Usage:
    ------
    1. Initialize the converter with the desired return type for the SMT code:
       ```
       converter = PythonToSMTConverter(return_type)
       ```
    2. Convert Python code to SMT-LIB2 format:
       ```
       smt_code = converter.python_to_smt(python_code)
       ```
   
    Note:
    -----
    - The supported return types are 'Int' for integers and 'Bool' for booleans.
    - The input Python code should be a subset of Python, including basic arithmetic operations,
      comparison operators, if statements, and function definitions.
    - Comments in the Python code are preserved in the conversion process.
    - The resulting SMT-LIB2 code can be used with SMT solvers for formal verification purposes.

    """

    def __init__(self, return_type):
        """
        Initialize the PythonToSMTConverter.

        Parameters:
        -----------
        return_type (str): The return type for the SMT code. Supported types are 'Int' and 'Bool'.
        """

        self.return_type = return_type
    def remove_comments(self, py_code):
        """
        Remove comments from a given Python code.
        This method parses the input Python code and removes all comments,
        including both inline comments marked with '#' and multiline comments enclosed in triple quotes.
        It returns the modified Python code without comments.
        """

        # Remove # comments
        lines = py_code.split('\n')
        lines_without_sharp_comments = [re.split(r'#', line, 1)[0] for line in lines]

        # Join lines without # comments and split by triple quotes to remove """ comments
        code_without_comments = '\n'.join(lines_without_sharp_comments)
        code_lines = code_without_comments.split('"""')
        code_without_all_comments = [code_lines[i] if i % 2 == 0 else '' for i in range(len(code_lines))]
        return ''.join(code_without_all_comments)
    
    def convert(self, node):
        """
        Convert an abstract syntax tree (AST) node to its corresponding SMT-LIB2 representation.

        Parameters:
        -----------
        node : ast.Node
            The AST node to be converted.

        Returns:
        --------
        str
            The SMT-LIB2 representation of the given AST node.

        Supported AST Node Types::
        ------
        - ast.Module: Represents a Python module.
        - ast.FunctionDef: Represents a function definition.
        - ast.Assign: Represents variable assignment.
        - ast.BinOp: Represents binary operations (e.g., +, -, *, /).
        - ast.Compare: Represents comparison operations.
        - ast.If: Represents an if statement.
        - ast.Expr: Represents an expression statement.
        - ast.Name: Represents a variable or identifier.
        - ast.NameConstant: Represents True, False, or None.
        - ast.Num: Represents a numeric constant.
        - ast.Str: Represents a string constant.
        - ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod: Represents specific arithmetic operations.
        - ast.BoolOp: Represents boolean operations (and, or).
        - ast.UnaryOp: Represents unary operations (e.g., not).
        - ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE: Represents comparison operators.
        - ast.Return: Represents a return statement.
        """

        if node is None:
            return ''

        if isinstance(node, ast.Module):
            return '\n'.join(self.convert(n) for n in node.body)
        
        elif isinstance(node, ast.FunctionDef):
            args = ' '.join(f'({arg.arg} {self.return_type})' for arg in node.args.args)
            body = '\n'.join(self.convert(n) for n in node.body)
            return f'(define-fun {node.name} ({args}) {self.return_type} {body})'
        
        elif isinstance(node, ast.Assign):
            targets = ' '.join(self.convert(target) for target in node.targets)
            value = self.convert(node.value)
            return f'(let {targets} {value})'
        
        elif isinstance(node, ast.BinOp):
            left = self.convert(node.left)
            op = self.convert(node.op)
            right = self.convert(node.right)
            return f'({op} {left} {right})'
        
        elif isinstance(node, ast.Compare):
            left = self.convert(node.left)
            ops = ' '.join(self.convert(op) for op in node.ops)
            comparators = ' '.join(self.convert(comp) for comp in node.comparators)
            if any(isinstance(op, ast.NotEq) for op in node.ops):
                return f'(not (= {left} {comparators}))'
            else:
                return f'({ops} {left} {comparators})'
            
        elif isinstance(node, ast.If):
            test = self.convert(node.test)
            body = '\n'.join(self.convert(n) for n in node.body)
            orelse = '\n'.join(self.convert(n) for n in node.orelse)
            return f'(ite {test} {body} {orelse})'
        
        elif isinstance(node, ast.Expr):
            return self.convert(node.value)
        
        elif isinstance(node, ast.Name):
            if node.id.lower() == 'true':
                return 'true'
            elif node.id.lower() == 'false':
                return 'false'
            else:
                return node.id
            
        elif isinstance(node, ast.NameConstant):
            return str(node.value)
        
        elif isinstance(node, ast.Num):
            return str(node.n)
        
        
        elif isinstance(node, ast.Str):
            return f'"{node.s}"'
        
        elif isinstance(node, ast.Add):
            return '+'
        
        elif isinstance(node, ast.Sub):
            return '-'
        
        elif isinstance(node, ast.Mult):
            return '*'
        
        elif isinstance(node, ast.Div):
            return 'div'
        
        elif isinstance(node, ast.Mod):
            return 'mod'
        
        elif isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                op = 'and'
            elif isinstance(node.op, ast.Or):
                op = 'or'
            else:
                op = f'UNKNOWN_TYPE_BoolOp_{type(node.op).__name__}'
            values = ' '.join(self.convert(value) for value in node.values)
            return f'({op} {values})'
        
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                operand = self.convert(node.operand)
                return f'(not {operand})'
            elif isinstance(node.op, ast.USub):
                operand = self.convert(node.operand)
                return f'(- {operand})'
            
        elif isinstance(node, ast.Eq):
            return '='

        elif isinstance(node, ast.Lt):
            return '<'
        
        elif isinstance(node, ast.LtE):
            return '<='
        
        elif isinstance(node, ast.Gt):
            return '>'
        
        elif isinstance(node, ast.GtE):
            return '>='
        
        elif isinstance(node, ast.Return):
            return self.convert(node.value) if node.value else 'nil'
        else:
            return f'UNKNOWN_TYPE_{type(node).__name__}'

    def python_to_smt(self, py_code):
        """
        Convert Python code to SMT-LIB2 format.

        Parameters:
        -----------
        py_code (str): Python code to be converted.

        Returns:
        --------
        str: The equivalent SMT-LIB2 code.
        """
        py_code = self.remove_comments(py_code)
        tree = ast.parse(py_code)
        return self.convert(tree)


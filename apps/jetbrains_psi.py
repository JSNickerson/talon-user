# If you plan on adding more, the PsiViewer plugin is essential.
# Poke around the tree, and note that I'm using the elementType / node field.
# (Giving a regex here, so that Py:IF_STATEMENT is matched by IF_STATEMENT, STATEMENT and IF_)
# If the elementType field varies depending on containing types, you can use | to specify more than one.
# (i.e., you want 'parameter' to work in both methods and functions, but they have different element types)
# The "_" gives a default ordinal/offset for the word.
#
# Putting ## in the path puts the ordinality modifier there instead of the end.
# Notes:
# - CSharp's AST is 80% dummy nodes.
#   We need a selector like: DUMMY_BLOCK>[regex] which filters by regex on element.text
#   in order to do anything useful. (Not entirely sure that would work either...)

PSI_PATHS = {
    # "block": {
    #     "_": "this",
    #     "cs": "DUMMY_BLOCK,DUMMY_BLOCK"
    # },
    "parameter": {
        "_": 0, # You probably want the first parameter of the current function
        "+": [", space", None],
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,PARAMETERS,PARAMETER_DECLARATION",
        "java": "METHOD|FUNCTION,^PARAMETER_LIST,PARAMETER",
        "py": "FUNCTION_DECLARATION,PARAMETER",
        "php": "Class method|function|Function,Parameter list,Parameter",
        "default": "DECLARATION,PARAMETER",
    },
    "parameter name": {
        "_": 0,  # You probably want the first parameter of the current function
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,PARAMETERS,PARAMETER_DECLARATION##,PARAM_DEFINITION",
        "java": "METHOD|FUNCTION,^PARAMETER_LIST,PARAMETER##,IDENTIFIER",
    },
    "parameter type": {
        "_": 0,  # You probably want the first parameter of the current function
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,PARAMETERS,PARAMETER_DECLARATION##,TYPE",
        "java": "METHOD|FUNCTION,^PARAMETER_LIST,PARAMETER##,TYPE,IDENTIFIER",
    },
    "import": {
        "_": 0, # You probably want the first import of the current file
        "+": ["enter", None],
        "go": "FILE,IMPORT_LIST,IMPORT_SPEC",
        "java": "FILE,IMPORT_LIST,IMPORT_STATEMENT",
        "py": "FILE,IMPORT_STATEMENT",
        "php": "FILE,Use list",
        "default": "FILE,IMPORT_STATEMENT",
    },
    "comment": {
        "_": "next",  # You probably want the next comment
        # "+": ["\n", None],
        "php": "FILE,Comment",
        "default": "FILE,COMMENT",
    },
    "method": {
        "_": "this",  # You probably want the method containing the cursor
        "+": ["enter shift-tab", "method"],
        "go": "FILE,METHOD_DECLARATION|FUNCTION_DECLARATION",
        "java": "java.FILE,METHOD",
        "py": "FILE,Py:FUNCTION_DECLARATION",
        "cs": "File,DUMMY_TYPE_DECLARATION,DUMMY_BLOCK",
        "php": "FILE,Class method|function|Function",
        "default": "FILE,METHOD_DECLARATION",
    },
    "method name": {
        "_": 0,  # You probably want the method name of the current method
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,identifier",
        "py": "Py:FUNCTION_DECLARATION,Py:IDENTIFIER",
        "java": "METHOD,IDENTIFIER",
        "php": "Class method,identifier",
        "default": "METHOD_DECLARATION,identifier",
    },
    "receiver": {
        "_": 0,  # You probably want the method name of the current method
        "go": "METHOD_DECLARATION,RECEIVER,identifier",
    },
    "receiver type": {
        "_": 0,  # You probably want the method name of the current method
        "go": "METHOD_DECLARATION,RECEIVER,TYPE",
    },
    "result": {
        "_": 0,  # You probably want the method name of the current method
        "go": "METHOD_DECLARATION,SIGNATURE,RESULT,TYPE",
    },
    "result name": {
        "_": 0,  # You probably want the method name of the current method
        "go": "METHOD_DECLARATION,SIGNATURE,RESULT,identifier",  # XXX Doesn't quite handle two.
    },
    "function": {
        "_": "this",  # You probably want the function containing the cursor
        "+": ["enter shift-tab", "function"],
        "go": "FILE,METHOD_DECLARATION|FUNCTION_DECLARATION",
        "py": "FILE,Py:FUNCTION_DECLARATION",
        "php": "FILE,Function",
        "default": "FILE,FUNCTION_DECLARATION",
    },
    "function name": {
        "_": 0,  # You probably want the function name of the current method
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,identifier",
        "py": "Py:FUNCTION_DECLARATION,Py:IDENTIFIER",
        "php": "Function,identifier",
        "default": "FUNCTION_DECLARATION,identifier",
    },
    "class": {
        "_": "this",  # You probably want the class containing the cursor
        "+": ["enter shift-tab", "class"],
        "py": "FILE,Py:CLASS_DECLARATION",
        "java": "FILE,CLASS",
        "php": "FILE,Class",
        "default": "FILE,CLASS_DECLARATION",
    },
    "class name": {
        "_": 0,  # You probably want the name of the current class
        "py": "Py:CLASS_DECLARATION,Py:IDENTIFIER",
        "java": "CLASS,IDENTIFIER",
        "php": "Class,identifier",
        "default": "CLASS_DECLARATION,identifier",
    },
    "type": {
        "_": "this",  # You probably want the type containing the cursor
        "+": ["\n", "type"],
        "go": "FILE,TYPE_DECLARATION",
    },
    "type name": {
        "_": 0,  # You probably want the name of the current type
        "go": "FILE,TYPE_DECLARATION,identifier",
    },
    "struct": {
        "_": "this",  # You probably want the struct containing the cursor.
        "+": ["enter shift-tab", "struct"],
        "go": "FILE,STRUCT_TYPE",
    },
    "if statement": {
        "_": "next",  # You probably want the next if statement of the method
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,IF_STATEMENT",
        "java": "METHOD|FUNCTION,IF_STATEMENT",
        "py": "Py:FUNCTION_DECLARATION,Py:IF_STATEMENT",
        "php": "FILE,If",
        "default": "METHOD_DECLARATION|FUNCTION_DECLARATION,IF_STATEMENT",
    },
    "while statement": {
        "_": "next",  # You probably want the next if statement of the method
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,FOR_STATEMENT",
        "java": "METHOD|FUNCTION,WHILE_STATEMENT",
        "py": "Py:FUNCTION_DECLARATION,Py:WHILE_STATEMENT",
        "php": "FILE,While",
        "default": "METHOD_DECLARATION|FUNCTION_DECLARATION,WHILE_STATEMENT",
    },
    "for statement": {
        "_": "next",  # You probably want the next if statement of the method
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,FOR_STATEMENT",
        "java": "METHOD|FUNCTION,FOREACH_STATEMENT|FOR_STATEMENT",
        "py": "Py:FUNCTION_DECLARATION,Py:FOR_STATEMENT",
        "php": "FILE,For",
        "default": "METHOD_DECLARATION|FUNCTION_DECLARATION,FOR_STATEMENT",
    },
    "statement": {
        "_": "next",  # You probably want the next statement of the method
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,STATEMENT",
        "java": "METHOD|FUNCTION,STATEMENT",
        "py": "Py:FUNCTION_DECLARATION|FILE,STATEMENT",
        "cs": "File,DUMMY_BLOCK,DUMMY_NODE",
        "php": "FILE,Statement",
        "default": "METHOD_DECLARATION|FUNCTION_DECLARATION|FILE,STATEMENT",
    },
    "argument": {
        "_": "next",  # You probably want the next argument of the current statement
        "go": "STATEMENT,ARGUMENT_LIST,_EXPR|LITERAL|_EXPRESSION",
        "java": "STATEMENT,EXPRESSION_LIST,_EXPRESSION",
        "py": "STATEMENT,ARGUMENT_LIST,EXPRESSION",
        "php": "Statement,Parameter list,Parameter",
        "default": "STATEMENT,ARGUMENT_LIST,EXPRESSION",
    },
    "return": {
        "_": "next",  # You probably want the next return statement of the method
        "go": "METHOD_DECLARATION|FUNCTION_DECLARATION,RETURN_STATEMENT",
        "java": "METHOD|FUNCTION,RETURN_STATEMENT",
        "py": "Py:FUNCTION_DECLARATION,Py:RETURN_STATEMENT",
        "php": "FILE,Return",
        "default": "METHOD_DECLARATION|FUNCTION_DECLARATION,RETURN_STATEMENT",
    },
    # "value": {
    #     "_": 0, # First value of the literal?
    #     "go": "LITERAL_VALUE,ELEMENT",
    #     "py": "Py:DICT_LITERAL_EXPRESSION,Py:KEY_VALUE_EXPRESSION",
    #     "default": "LITERAL_VALUE,ELEMENT",
    # },
    "left hand": {
        "_": 0,  # LHS of the current statement.  Ordinals make sense for multi-assign.
        "go": "STATEMENT,LEFT_HAND_EXPR_LIST|VAR_DEFINITION",
        "py": "Py:ASSIGNMENT_STATEMENT,Py:TARGET_EXPRESSION",
    },
    # XXX RHS expression
    # "index": {
    #     "go": "sibling INDEX_OR_SLICE_EXPR",
    #     "py": "sibling Py:SUBSCRIPTION_EXPRESSION",
    # }
}
G2 = r"""
%import common.WS
%import common.CNAME 
%ignore WS
%ignore COMMENT
%ignore COMPLEX_COMMENT

program: macro* (decl)+ -> program
macro : "import" STRING 
decl: variable_decl -> variable_declaration
    | function_decl -> function_declaration
    | class_decl -> class_declaration
    | interface_decl -> interface_declaration

variable_decl: variable ";" -> variable_declared
variable: type identifier -> variable_defined
        | type identifier "=" const -> variable_defined_with_assign
type: "int" -> type_int
    | "double" -> type_double
    | "bool" -> type_bool
    | "string" -> type_string
    | identifier -> type_identifier
    | type /\[\s*\]/ -> type_array

function_decl: type identifier "(" formals ")" stmt_block -> typed_function_declared
    | "void" identifier "(" formals ")" stmt_block -> void_function_declared

formals: variable ("," variable)* -> formals_variable
    | -> formals_empty
class_decl: "class" identifier extends_ident implements_ident "{" (field)* "}" -> new_class
extends_ident: "extends" identifier -> extends_identifier
    | -> extends_identifier_empty
implements_ident: "implements" identifier ("," identifier)* -> implements_identifier
    | -> implements_identifier_empty
field:access_mode variable_decl -> field_variable
    | access_mode function_decl -> field_function
access_mode: "public" -> access_mode_public
            | "private" -> access_mode_private
            | "protected"
            |  -> access_mode_emtpy
interface_decl: "interface" identifier "{" (prototype)* "}" -> interface_declaration
prototype: type identifier "(" formals ")" ";" -> prototype_type
    | "void" identifier "(" formals ")" ";" -> prototype_void
stmt_block: "{" (variable_decl)* (stmt)* "}" -> statement_block
stmt: if_stmt -> statement_if
    | while_stmt -> statement_while
    | for_stmt -> statement_for
    | break_stmt -> statement_break
    | continue_stmt -> statement_continue
    | return_stmt -> statement_return
    | print_stmt -> statement_print
    | optional_expression ";" -> statement_optional_expression
    | stmt_block -> statement_block
if_stmt: "if" "(" expr ")" stmt ("else" stmt)? -> if_statement
while_stmt: "while" "(" expr ")" stmt -> while_statement
for_stmt: "for" "(" optional_expression ";" expr ";" optional_expression ")" stmt -> for_statement
return_stmt: "return" optional_expression ";" -> return_statement
optional_expression: (expr)?-> optional_expression_statement
break_stmt: "break" ";" -> break_statement
continue_stmt: "continue" ";" -> continue_statement
print_stmt : "Print" "(" expr ("," expr)* ")" ";" -> print_statement

expr: assigns -> expr_or

assigns: concrete_lvalue "=" assigns -> assign
    | or -> assign_or

or: or "||" and -> or
    | and -> or_and
and: and "&&" eqs -> and
    | eqs -> and_eqs
eqs: eqs "==" rels -> equals
    | eqs "!=" rels -> n_equals
    | rels -> eqs_rels
rels: rels "<" addi -> lt
    | rels "<=" addi -> lte
    | rels ">" addi -> gt
    | rels ">=" addi -> gte
    | addi -> rels_addi
addi: addi "+" multi -> add
    | addi "-" multi -> sub
    | multi -> addi_multi
multi: multi "*" unary -> mult
    | multi "/" unary -> div
    | multi "%" unary -> mod
    | unary -> multi_unary
unary: "-" unary -> neg
    | "!" unary -> not
    | par -> unary_par
par: "(" par ")" -> par
    | "(" expr ")" -> par_expr
    | atom -> par_atom

args:  expr ("," expr)* -> args
| -> empty_args
    
concrete_lvalue: lvalue "." identifier -> clv_access
    | lvalue_atom "." identifier -> clv_access
    | lvalue "[" expr "]" -> clv_index
    | lvalue_atom "[" expr "]" -> clv_index
    | identifier -> clv_id

atom: const -> atom_const
    | dts "("expr")" -> atom_dts
    | "ReadInteger" "(" ")" -> read_integer
    | "ReadLine" "(" ")" -> read_line
    | lvalue -> atom_lv
    | lvalue_atom -> atom_lv

lvalue: lvalue "." identifier -> lv_access
    | lvalue_atom "." identifier -> lv_access
    | lvalue "[" expr "]" -> lv_index
    | lvalue_atom "[" expr "]" -> lv_index
    | identifier -> lv_id
    | "(" lvalue ")" -> lv_par

lvalue_atom: "new" CLS_IDENT ["("")"]  -> expr_instantiate
    | "NewArray" "(" expr "," type ")" -> expr_instantiate_array
    | "this" -> expr_this
    | identifier "(" args ")" -> lv_call

dts: "dtoi" | "btoi" | "itod" | "itob" -> dts

identifier: IDENT -> identifier
const: INTEGER -> int_const
    | DOUBLE -> double_const
    | BOOL -> bool_const
    | NULL -> null_const
    | STRING -> string_const
NULL: "null"

BOOL: "true" | "false" 
DOUBLE: /[0-9]+\.[0-9]*([eE]([-+]?)[0-9]+)?/
IDENT: /\b(?!(this|class|return|if|else|__func__|__line__|itod|dtoi|itob|btoi|while|for|continue|break|private|public|void|string|bool|true|false|int|double)\b)[A-Za-z][A-Za-z0-9_]{0,128}/
CLS_IDENT :  /\b(?!(int|double|string|bool|true|false)\b)[A-Za-z][A-Za-z0-9_]{0,128}/
STRING : /".*?(?<!\\)"/
HEXADECIMAL: /0[xX][A-Fa-f0-9]+/
DECIMAL: /[0-9]+/
INTEGER: HEXADECIMAL | DECIMAL
COMMENT : /\/\/.*/
COMPLEX_COMMENT : /\/\*([^\*]|(\*+[^\/\*]))*\*+\//
"""

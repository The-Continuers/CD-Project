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
    | -> implements_identifier_emtpy
field:access_mode variable_decl -> field_variable
    | access_mode function_decl -> field_function
access_mode: "public" -> access_mode_public
            | "private" -> access_mode_private
            |  -> access_mode_emtpy
interface_decl: "interface" identifier "{" (prototype)* "}" -> interface_declaration
prototype: type identifier "(" formals ")" ";" -> prototype_type
    | "void" identifier "(" formals ")" ";" -> prototype_void
stmt_block: "{" (variable_decl)* (stmt)* "}" -> statement_block
stmt: optional_expression ";" -> statement_optional_expression
    | if_stmt -> statement_if
    | while_stmt -> statement_while
    | for_stmt -> statement_for
    | break_stmt -> statement_break
    | continue_stmt -> statement_continue
    | return_stmt -> statement_return
    | print_stmt -> statement_print
    | stmt_block -> statement_block
if_stmt: "if" "(" expr ")" stmt ("else" stmt)? -> if_statement
while_stmt: "while" "(" expr ")" stmt -> while_statement
for_stmt: "for" "(" optional_expression ";" expr ";" optional_expression ")" stmt -> for_statement
return_stmt: "return" optional_expression ";" -> return_statement
optional_expression: (expr)?-> optional_expression_statement
break_stmt: "break" ";" -> break_statement
continue_stmt: "continue" ";" -> continue_statement
print_stmt : "Print" "(" expr ("," expr)* ")" ";" -> print_statement

expr: or -> expr_or

or: or "||" and -> or
    | and -> or_and
and: and "&&" equals -> and
    | equals -> and_equals
equals: equals "==" n_equals  -> equals
    | n_equals -> equals_n_equals
n_equals: n_equals "!=" lt -> n_equals
    | lt -> n_equals_lt
lt: lt "<" lte -> lt
    | lte -> lt_lte
lte: lte "<=" gt -> lte
    | gt -> lte_gt
gt: gt ">" gte -> gt
    | gte -> expr6_expr7
gte: gte ">=" add -> gte
    | add -> gte_add
add: add "+" add_equal -> add
    | add_equal -> add_add_equal
add_equal : add_equal "+=" sub -> add_equal
   | sub -> add_equal_sub
sub: sub "-" sub_equal -> expr_sub
    | sub_equal -> sub_sub_equal
sub_equal : sub_equal "-=" multi -> expr_sub_equal
   | multi -> sub_equal_multi
multi: multi "*" multi_equal -> expr_mul
    | multi_equal -> multi_multi_equal
multi_equal : multi_equal "*=" divide -> expr_mul_equal
   | divide -> multi_equal_divide
divide: divide "/" divide_equal -> expr_div
    | divide_equal -> divide_divide_equal
divide_equal : divide_equal "/=" mod -> expr_div_equal
   | mod -> divide_equal_mod
mod: mod "%" mod_equal -> expr_mod
    | mod_equal -> mod_mod_equal
mod_equal : mod_equal "%=" neg -> expr_mod_equal
   | neg -> mod_equal_neg

neg: "-" neg  -> expr_negative
    | not -> neg_not
not: "!" not -> expr_not
    | assign -> not_assign

assign: real_l_value "=" expr -> assign
    | expr_const -> assign_expr_const
real_l_value: l_value_id -> identifier_l_value
    | expr_const "." identifier -> member_access_fields
    | "(" expr ")" l_value_bracket -> bracket_expr_access_idx
l_value_id: l_value_id "[" expr "]" -> array_access_l_value
            | identifier -> l_value_identifier
            | "[" expr "]" -> l_value_access_idx
l_value_bracket: l_value_id "[" expr "]" -> array_access_idx
    | "[" expr "]"
l_value: real_l_value -> l_value_real_l_value
    | "(" expr ")" -> l_value_pass_element

expr_const:  const -> expr_const
    | l_value -> expr_left_value
    | call -> expr_call
    | "new" CLS_IDENT ["("")"]  -> expr_instantiate
    | "NewArray" "(" expr "," type ")" -> expr_instantiate_array
    | dts "("expr")" -> expr_dts
    | "this" -> expr_this
    | "ReadInteger" "(" ")" -> expr_read_integer
    | "ReadLine" "(" ")" -> expr_read_line
    | "__func__" -> expr_f
    | "__line__" -> expr_l

call: identifier "(" args ")" -> function_call
    | expr_const "." identifier "(" args ")" -> method_call
args:  expr ("," expr)* -> args
    | -> empty_args

dts: "dtoi" | "btoi" | "itod" | "itob" -> dts

identifier: IDENT -> identifier
BOOL: "true" | "false"
const: INTEGER -> int_const
    | DOUBLE -> double_const
    | BOOL -> bool_const
    | NULL -> null_const
    | STRING -> string_const
NULL: "null"

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

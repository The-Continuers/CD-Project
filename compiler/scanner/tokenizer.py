import ply.lex as lex

tokens = (
    'T_NORM',
    'T_ID',
    'T_INTLITERAL',
    'T_DOUBLELITERAL',
    'T_STRINGLITERAL',
    'T_BOOLEANLITERAL'
)

# main tokens
t_T_NORM = r"^(<<)|(>>)|(<=)|(>=)|(==)|(!=)|(&&)|(\|\|)|[{}\[\],;()=\-!+*\/<>%]$"
t_T_ID = r"^[_a-zA-Z][_a-zA-Z0-9]*$"
t_T_INTLITERAL = r"^(0x)?[0-9]+$"
# todo overlook
t_T_DOUBLELITERAL = r"^[0-9]+(\.[0-9]+)?$"
t_T_STRINGLITERAL = r"""^\"([^"]|(\\\"))*\"$"""
t_T_BOOLEANLITERAL = r"^(true)|(false)$"
# todo t_comment. PreProcessor?

# other tokens
t_ignore = " \t\n"


# todo adjust the rest of the string to UNDEFINED_TOKEN
def t_error(t):
    pass


lexer = lex.lex()

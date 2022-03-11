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
def t_T_NORM(t):
    r"^(<<)|(>>)|(<=)|(>=)|(==)|(!=)|(&&)|(\|\|)|[{}\[\],;()=\-!+*\/<>%]$"
    return t


def t_T_ID(t):
    r"^[_a-zA-Z][_a-zA-Z0-9]*$"
    return t


def t_T_INTLITERAL(t):
    r"^(0x)?[0-9]+$"
    t.value = int(t.value)
    return t


# todo overlook
def t_T_DOUBLELITERAL(t):
    r"^[0-9]+(\.[0-9]+)?$"
    t.value = float(t.value)
    return t


def t_T_STRINGLITERAL(t):
    r"""^\"([^"]|(\\\"))*\"$"""
    return t


# todo
def t_T_BOOLEANLITERAL(t):
    r"^(true)|(false)$"
    return t


# todo t_comment. PreProcessor?

# other tokens
t_ignore = " \t\n"


# todo adjust the rest of the string to UNDEFINED_TOKEN
def t_error(t):
    pass


lexer = lex.lex()

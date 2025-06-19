from ply import lex

# verilog
tokens = (
    'ID',
    'BDH',
    'NUMBER',
    'NOT',
    'MUL',
    'PLUS',
    'MINUS',
    'SHIFTL',
    'SHIFTR',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQ',
    'NE',
    'AND',
    'XOR',
    'OR',
    'LAND',
    'LOR',
    'LNOT',
    'TERNARY_L',
    'TERNARY_R',
    'LPAREN',
    'RPAREN',
    'BITSEL_L',
    'BITSEL_R',
    'CONCAT_L',
    'CONCAT_M',
    'CONCAT_R',
    'ASSIGN'
)

t_NOT = r'~'
t_MUL = r'\*'
t_PLUS = r'\+'
t_MINUS = r'-'
t_SHIFTL = r'<<'
t_SHIFTR = r'>>'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_AND = r'&'
t_XOR = r'\^'
t_OR = r'\|'
t_LAND = r'&&'
t_LOR = r'\|\|'
t_LNOT = r'!'
t_TERNARY_L = r'\?'
t_TERNARY_R = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BITSEL_L = r'\['
t_BITSEL_R = r'\]'
t_CONCAT_L = r'\{'
t_CONCAT_M = r','
t_CONCAT_R = r'\}'
t_ASSIGN = r'='

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_BDH(t):
    r"[1-9]\d*'[bdh][0-9a-fA-F]+"
    b_ind = t.value.find('\'b')
    d_ind = t.value.find('\'d')
    h_ind = t.value.find('\'h')
    if b_ind != -1:
        bits = int(t.value[:b_ind])
        t.value = (bits, '0b'+t.value[b_ind+2:])
    elif d_ind != -1:
        bits = int(t.value[:d_ind])
        t.value = (bits, t.value[d_ind+2:])
    elif h_ind != -1:
        bits = int(t.value[:h_ind])
        t.value = (bits, '0x'+t.value[h_ind+2:])
    return t

def t_NUMBER(t):
    r'\d+'
    int_value = int(t.value)
    t.value = (1 if int_value == 0 else int_value.bit_length(), t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()



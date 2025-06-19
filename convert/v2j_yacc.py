import ply.yacc as yacc

from convert.verilog_lex import tokens # do not ignore this line or delete it

# 最开始
def p_start(p):
    'start : var ASSIGN expr'
    p[0] = p[1] + p[3] + ');'

def p_var1(p):
    'var : ID'
    p[0] = f'{p[1]}.set('

def p_var2(p):
    'var : ID BITSEL_L num BITSEL_R'
    p[0] = f'{p[1]}.setBit(' + p[3][1] + ', '

def p_var3(p):
    'var : ID BITSEL_L num TERNARY_R num BITSEL_R'
    p[0] = f'{p[1]}.setBits(' + p[3][1] + ','+ p[5][1] + ', '
    

# 三目运算符
def p_ternary(p):
    'expr : expr TERNARY_L expr TERNARY_R expr'
    p[0] = p[1] + '.ternary(' + p[3] + ','+ p[5] + ')'

# 逻辑运算符
def p_logic_op(p):
    '''expr : expr LAND expr
            | expr LOR expr'''
    if p[2] == '&&':
        p[0] = p[1] + '.logicalAnd(' + p[3] + ')'
    elif p[2] == '||':
        p[0] = p[1] + '.logicalOr(' + p[3] + ')'

# 位运算符
def p_bit_op(p):
    '''expr : expr AND expr
            | expr XOR expr
            | expr OR expr'''
    if p[2] == '&':
        p[0] = p[1] + '.bitAnd(' + p[3] + ')'
    elif p[2] == '^':
        p[0] = p[1] + '.bitXor(' + p[3] + ')'
    elif p[2] == '|':
        p[0] = p[1] + '.bitOr(' + p[3] + ')'

# 关系运算符
def p_relational_op(p):
    '''expr : expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr EQ expr
            | expr NE expr'''
    if p[2] == '<':
        p[0] = p[1] + '.lessThan(' + p[3] + ')'
    elif p[2] == '<=':
        p[0] = p[1] + '.lessEqual(' + p[3] + ')'
    elif p[2] == '>':
        p[0] = p[1] + '.greaterThan(' + p[3] + ')'
    elif p[2] == '>=':
        p[0] = p[1] + '.greaterEqual(' + p[3] + ')'
    elif p[2] == '==':
        p[0] = p[1] + '.isEqual(' + p[3] + ')'
    elif p[2] == '!=':
        p[0] = p[1] + '.notEqual(' + p[3] + ')'

# 移位运算符
def p_shift_op(p):
    '''expr : expr SHIFTL expr
            | expr SHIFTR expr'''
    if p[2] == '<<':
        p[0] = p[1] + '.shiftLeft(' + p[3] + ')'
    elif p[2] == '>>':
        p[0] = p[1] + '.shiftRight(' + p[3] + ')'

# 算术运算符
def p_arithmetic_op(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr MUL expr'''
    if p[2] == '+':
        p[0] = p[1] + '.add(' + p[3] + ')'
    elif p[2] == '-':
        p[0] = p[1] + '.sub(' + p[3] + ')'
    elif p[2] == '*':
        p[0] = p[1] + '.mul(' + p[3] + ')'


# 单目运算符
def p_unary_op(p):
    '''expr : LNOT expr
            | NOT expr
            | AND expr %prec UAND
            | XOR expr %prec UXOR
            | OR expr %prec UOR'''
    if p[1] == '+':
        p[0] = p[2]
    elif p[1] == '-':
        p[0] = p[2] + '.neg()'
    elif p[1] == '!':
        p[0] = p[2] + '.logicalNot()'
    elif p[1] == '~':
        p[0] = p[2] + '.bitNot()'
    elif p[1] == '&':
        p[0] = p[2] + '.reduceAnd()'
    elif p[1] == '^':
        p[0] = p[2] + '.reduceXor()'
    elif p[1] == '|':
        p[0] = p[2] + '.reduceOr()'

# 位选择运算符
def p_bits_select(p):
    'expr : expr BITSEL_L num TERNARY_R num BITSEL_R'
    p[0] = p[1] + '.getBits(' + p[3][1] + ','+ p[5][1] + ')'

def p_bit_select(p):
    'expr : expr BITSEL_L num BITSEL_R'
    p[0] = p[1] + '.getBit(' + p[3][1] + ')'

# 连接运算符
def p_concat(p):
    'expr : CONCAT_L concatlist CONCAT_R'
    p[0] = 'wire.concat(' + p[2] + ')'

def p_concatlist(p):
    '''concatlist : expr CONCAT_M concatlist
                  | expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ','+ p[3]

# 值
def p_expr_ID(p):
    'expr : ID'
    p[0] = p[1]

def p_expr_num(p):
    'expr : num'
    p[0] = f'new wire({p[1][0] - 1}, 0, {p[1][1]})'

def p_num(p):
    '''num : NUMBER
           | BDH'''
    p[0] = p[1]

def p_num_arith(p):
    '''num : PLUS num %prec UPLUS
           | MINUS num %prec UMINUS'''
    if p[1] == '+':
        p[0] = p[2]
    elif p[1] == '-':
        p[0] = (p[2][0], '-' + p[2][1])

# 括号
def p_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

# 错误处理
def p_error(p):
    print("Syntax error in input!")

precedence = (
    ('left', 'CONCAT_M'),
    ('left', 'CONCAT_L', 'CONCAT_R'),
    ('right', 'TERNARY_L', 'TERNARY_R'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'SHIFTL', 'SHIFTR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL'),
    ('right', 'UMINUS', 'UPLUS', 'LNOT', 'NOT', 'UAND', 'UXOR', 'UOR'),
    ('left', 'BITSEL_L', 'BITSEL_R')
)

parser = yacc.yacc(debug=False, write_tables=False)

if __name__ == '__main__':
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
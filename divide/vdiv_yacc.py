import ply.yacc as yacc

from divide.verilog_lex import tokens # do not ignore this line or delete it

var_name = ''
name_count = 0


# 最开始
def p_start(p):
    'start : var ASSIGN expr'
    p[0] = p[3]['code'].copy()
    p[0].append(f'assign {p[1]} = {p[3]["name"]};\n')

def p_var1(p):
    'var : ID'
    global var_name, name_count
    var_name = p[1]
    name_count = 0
    p[0] = f'{p[1]}'

def p_var2(p):
    'var : ID BITSEL_L num BITSEL_R'
    global var_name, name_count
    var_name = p[1] + '_' + p[3][1]
    name_count = 0
    p[0] = f'{p[1]}[' + p[3][1] + ']'

def p_var3(p):
    'var : ID BITSEL_L num TERNARY_R num BITSEL_R'
    global var_name, name_count
    var_name = p[1] + '_' + p[3][1] + '_' + p[5][1]
    name_count = 0
    p[0] = f'{p[1]}[' + p[3][1] + ': ' + p[5][1] + ']'
    

# 三目运算符
def p_ternary(p):
    'expr : expr TERNARY_L expr TERNARY_R expr'
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    code.extend(p[3]['code'])
    code.extend(p[5]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    code.append(f'wire {name} = {p[1]["name"]}? {p[3]["name"]} : {p[5]["name"]};')
    p[0] = {
        'name': name,
        'code': code
    }


# 逻辑运算符
def p_logic_op(p):
    '''expr : expr LAND expr
            | expr LOR expr'''
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    code.extend(p[3]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    if p[2] == '&&':
        code.append(f'wire {name} = {p[1]["name"]} && {p[3]["name"]};')
    elif p[2] == '||':
        code.append(f'wire {name} = {p[1]["name"]} || {p[3]["name"]};')
    p[0] = {
        'name': name,
        'code': code
    }

# 位运算符
def p_bit_op(p):
    '''expr : expr AND expr
            | expr XOR expr
            | expr OR expr'''
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    code.extend(p[3]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    if p[2] == '&':
        code.append(f'wire {name} = {p[1]["name"]} & {p[3]["name"]};')
    elif p[2] == '^':
        code.append(f'wire {name} = {p[1]["name"]} ^ {p[3]["name"]};')
    elif p[2] == '|':
        code.append(f'wire {name} = {p[1]["name"]} | {p[3]["name"]};')
    p[0] = {
        'name': name,
        'code': code
    }

# 关系运算符
def p_relational_op(p):
    '''expr : expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr EQ expr
            | expr NE expr'''
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    code.extend(p[3]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    if p[2] == '<':
        code.append(f'wire {name} = {p[1]["name"]} < {p[3]["name"]};')
    elif p[2] == '<=':
        code.append(f'wire {name} = {p[1]["name"]} <= {p[3]["name"]};')
    elif p[2] == '>':
        code.append(f'wire {name} = {p[1]["name"]} > {p[3]["name"]};')
    elif p[2] == '>=':
        code.append(f'wire {name} = {p[1]["name"]} >= {p[3]["name"]};')
    elif p[2] == '==':
        code.append(f'wire {name} = {p[1]["name"]} == {p[3]["name"]};')
    elif p[2] == '!=':
        code.append(f'wire {name} = {p[1]["name"]} != {p[3]["name"]};')
    p[0] = {
        'name': name,
        'code': code
    }

# 移位运算符
def p_shift_op(p):
    '''expr : expr SHIFTL expr
            | expr SHIFTR expr'''
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    code.extend(p[3]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    if p[2] == '<<':
        code.append(f'wire {name} = {p[1]["name"]} << {p[3]["name"]};')
    elif p[2] == '>>':
        code.append(f'wire {name} = {p[1]["name"]} >> {p[3]["name"]};')
    p[0] = {
        'name': name,
        'code': code
    }

# 算术运算符
def p_arithmetic_op(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr MUL expr'''
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    code.extend(p[3]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    if p[2] == '+':
        code.append(f'wire {name} = {p[1]["name"]} + {p[3]["name"]};')
    elif p[2] == '-':
        code.append(f'wire {name} = {p[1]["name"]} - {p[3]["name"]};')
    elif p[2] == '*':
        code.append(f'wire {name} = {p[1]["name"]} * {p[3]["name"]};')
    p[0] = {
        'name': name,
        'code': code
    }


# 单目运算符
def p_unary_op(p):
    '''expr : LNOT expr
            | NOT expr
            | AND expr %prec UAND
            | XOR expr %prec UXOR
            | OR expr %prec UOR'''
    global var_name, name_count
    code = []
    code.extend(p[2]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    if p[1] == '!':
        code.append(f'wire {name} = !{p[2]["name"]};')
    elif p[1] == '~':
        code.append(f'wire {name} = ~{p[2]["name"]};')
    elif p[1] == '&':
        code.append(f'wire {name} = &{p[2]["name"]};')
    elif p[1] == '^':
        code.append(f'wire {name} = ^{p[2]["name"]};')
    elif p[1] == '|':
        code.append(f'wire {name} = |{p[2]["name"]};')
    p[0] = {
        'name': name,
        'code': code
    }

# 位选择运算符
def p_bits_select(p):
    'expr : expr BITSEL_L num TERNARY_R num BITSEL_R'
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    code.append(f'wire {name} = {p[1]["name"]}[{p[3][1]}: {p[5][1]}];')
    p[0] = {
        'name': name,
        'code': code
    }

def p_bit_select(p):
    'expr : expr BITSEL_L num BITSEL_R'
    global var_name, name_count
    code = []
    code.extend(p[1]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    code.append(f'wire {name} = {p[1]["name"]}[{p[3][1]}];')
    p[0] = {
        'name': name,
        'code': code
    }

# 连接运算符
def p_concat(p):
    'expr : CONCAT_L concatlist CONCAT_R'
    global var_name, name_count
    code = []
    code.extend(p[2]['code'])
    name = f'{var_name}_{name_count}'
    name_count += 1
    code.append(f'wire {name} = {{p[2]["name"]}};')
    p[0] = {
        'name': name,
        'code': code
    }

def p_concatlist(p):
    '''concatlist : expr CONCAT_M concatlist
                  | expr'''
    code = []
    code.extend(p[1]['code'])
    name = p[1]["name"]
    if len(p) != 2:
        code.extend(p[3]['code'])
        name += ', ' + p[3]["name"]
    p[0] = {
        'name': name,
        'code': code
    }

# 值
def p_expr_ID(p):
    'expr : ID'
    p[0] = {
        'name': p[1],
        'code': []
    }

def p_expr_num(p):
    'expr : num'
    global var_name, name_count
    name = f'{var_name}_{name_count}'
    name_count += 1
    p[0] = {
        'name': name,
        'code': [f'wire {name} = {p[1][1]};']
    }

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

parser = yacc.yacc(debug=False, write_tables=False, start='start')

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
import re
import ply.lex as lex

states = (
  ('code','exclusive'),
)

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'in' : 'IN',
    'function' : 'FUNC',
    'program' : 'PROG',
    'int' : 'DATATYPE',
    'float' : 'DATATYPE',
    'double' : 'DATATYPE',
    'char' : 'DATATYPE',
    'string' : 'DATATYPE'
}

tokens = (
    'VAR',
    'LOPEN',
    'RCLOSE',
    'LPARN',
    'RPARN',
    'CALL',
    'CHAR',
    'STRING',
    'INT',
    'DOUBLE',
    'COMMENT',
    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'IN',
    'FUNC',
    'PROG',
    'DATATYPE',
    'ASSIGN',
    'CODE'
)

literals = (
    '+',
    '-',
    '*',
    '/', 
    '=',
    '{', 
    '}',
)

def t_INITIAL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.lexer.clevel = 0
    t.lexer.cpos = []
    t.type = reserved.get(t.value,'VAR')
    return t

def t_INITIAL_COMMENT(t):
    r'(\/\*(.|\n)*?\*\/)|(\/\/.*)'
    pass

def t_INITIAL_ASSIGN(t):
    r'(?:(?<=\w)|(?<=\w ))=(?=\s?.)'
    return t

def t_INITIAL_LPARN(t):
    r'\('
    t.type = 'LPARN'
    t.lexer.clevel += 1
    t.lexer.cpos.append(t.lexer.lexpos-1)

def t_INITIAL_RPERN(t):
    r'\)'
    t.type = 'RPARN'
    t.lexer.clevel -= 1

    if t.lexer.clevel >= 0:
        t.value = t.lexer.lexdata[t.lexer.cpos.pop(-1):t.lexer.lexpos]
        t.type = 'CALL'
        return t

def t_INITIAL_CALL(t):
    r'(?<!\w )\w+\(\w+(,\s?[\w_]+)*\)'
    t.type = 'CALL'
    return t

def t_INITIAL_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VAR')
    return t

def t_INITIAL_STRING(t):
   r'\"([^\\\n]|(\\.))*?\"'
   return t

def t_INITIAL_CHAR(t):
   r'\'([^\\\n]|(\\.))*?\''
   return t

def t_INITIAL_DOUBLE(t):
   r'\s\d+\.\d+'
   return t

def t_INITIAL_INT(t):
   r'\s\d+'
   return t

def t_INITIAL_nonspace(t):
   r'[^\s\{\}\'\"]+'

def t_code(t):
    r'\{'
    t.type = 'LOPEN'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.clevel = 0
    t.lexer.cpos = []
    t.lexer.begin('code')
    return t

def t_code_COMMENT(t):
    r'(\/\*(.|\n)*?\*\/)|(\/\/.*)'
    pass

def t_code_LOPEN(t):
    r'\{'
    t.type = 'LOPEN'
    t.lexer.level += 1
    return t

def t_code_RCLOSE(t):
    r'\}'
    t.type = 'RCLOSE'
    t.lexer.level -= 1

    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
         t.type = "CODE"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')
         return t

def t_code_ASSIGN(t):
    r'(?:(?<=\w)|(?<=\w ))=(?=\s?.)'
    return t

def t_code_LPARN(t):
    r'\('
    t.type = 'LPARN'
    t.lexer.clevel += 1
    t.lexer.cpos.append(t.lexer.lexpos-1)

def t_code_RPERN(t):
    r'\)'
    t.type = 'RPARN'
    t.lexer.clevel -= 1

    if t.lexer.clevel >= 0:
        t.value = t.lexer.lexdata[t.lexer.cpos.pop(-1):t.lexer.lexpos]
        t.type = 'CALL'
        return t

def t_code_CALL(t):
    r'(?<!\w )\w+\(\w+(,\s?[\w_]+)*\)'
    t.type = 'CALL'
    return t

def t_code_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VAR')
    return t

def t_code_STRING(t):
   r'\"([^\\\n]|(\\.))*?\"'
   return t

def t_code_CHAR(t):
   r'\'([^\\\n]|(\\.))*?\''
   return t

def t_code_DOUBLE(t):
   r'\s\d+\.\d+'
   return t

def t_code_INT(t):
   r'\s\d+'
   return t

def t_code_nonspace(t):
   r'[^\s\{\}\'\"]+'

t_code_ignore = " \t\n"
t_ignore = " \t\n;"

def t_code_error(t):
    t.lexer.skip(1)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()

# Test it out
data = '''
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;
string c;
c = "asda";

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
'''

# Give the lexer some input
lexer.input(data)
for tok in lexer:
    print(tok)
    # print(tok.type, tok.value, tok.lineno, tok.lexpos)
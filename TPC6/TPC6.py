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
    'char' : 'CHAR'
}

tokens = (
    'VAR',
    'LOPEN',
    'RCLOSE',
    'CALL',
    'NUM',
    'CHAR',
    'STRING',
    'COMMENT',
    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'IN',
    'FUNC',
    'PROG',
    'DATATYPE',
    'CODE'
)

literals = (
    '+',
    '-',
    '*',
    '/', 
    '{', 
    '}',
    '(',
    ')'
)

def t_INITIAL_COMMENT(t):
    r'(\/\*(.|\n)*?\*\/)|(\/\/.*)'
    pass

def t_INITIAL_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VAR')
    return t

def t_code(t):
    r'\{'
    t.type = 'LOPEN'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
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

def t_code_NUM(t):
   r'\s\d+'
   return t

def t_code_nonspace(t):
   r'[^\s\{\}\'\"]+'

t_code_ignore = " \t\n"
t_ignore = " \t\n"

def t_code_error(t):
    t.lexer.skip(1)
        
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

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
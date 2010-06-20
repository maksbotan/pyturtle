import sys
sys.path.insert(1,'/home/maks/pyturtle')

from ply import yacc
from pyturtle.parser.logo_l import tokens

def p_func_call(t):
    'func_call : func_name args'

    print "Calling function '%s' with args '%s'" % (t[1], t[2])

def p_func_name(t):
    'func_name : WORD'
    
    t[0] = t[1]

def p_args_signle(t):
    'args : arg'
    print 'args_single: ', t[1]
    t[0] = t[1]

def p_args_multi(t):
    'args : args arg'
    print 'args_multi: ', t[1], ' ', t[2]
    if isinstance(t[1], list):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1],t[2]]

def p_arg_word(t):
    'arg : WORD'
    t[0] = t[1]

def p_arg_num(t):
    'arg : NUMBER'
    t[0] = t[1]

yacc.yacc()

if __name__ == '__main__':
    yacc.parse('print 1 2 w0rd')

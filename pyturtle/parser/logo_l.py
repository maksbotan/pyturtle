import sys
sys.path.insert(1,'/home/maks/pyturtle')

from ply import lex
from pyturtle.misc import ParseErrorException

tokens = (
    'NUMBER',
    'QUOT',
    'WORD'
    )

t_NUMBER = r'\d+'
t_QUOT = r'"'
t_WORD = r'[a-zA-z][a-zA-Z0-9]*'
t_ignore = ' \t'

def t_error(t):
    raise ParseErrorException(t.value, 'Unexpected symbol')

lex.lex()

if __name__ == '__main__':
    lex.input ('print 1 "d \'')
    for tok in iter(lex.token, None):
        print repr(tok.type), repr(tok.value)

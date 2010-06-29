from ply import lex, yacc
from pyturtle.misc import Event

class parser:

    def __init__(self, vars, q, callback):
        self.vars = vars
        self.q = q
        self.callback = callback

        self.build()

    tokens = (
            'NUMBER',
            'QUOT',
            'WORD'
        )

    t_QUOT = r'"'
    t_WORD = r'[a-zA-z][a-zA-Z0-9]*'
    t_ignore = ' \t'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_error(self, t):
        self.response.append(['Unexpected symbol', t])

    def p_func_call(self, p):
        'func_call : func_name'
        print 'parser.p_func_call: Calling "%s"' % p[1]
        self.q.put_nowait(
            Event(
                self.callback, ([p[1]], )
                )
            )

    def p_func_call_args(self, p):
        'func_call : func_name args'
        print "parser.p_func_call: Calling '%s' with args '%s'" % (p[1], p[2])
        self.q.put_nowait(
            Event(
                self.callback, ([p[1], p[2]], )
                )
            )
        

    def p_func_name(self, p):
        'func_name : WORD'
    
        p[0] = p[1]

    def p_args_signle(self, p):
        'args : arg'
        p[0] = p[1]

    def p_args_multi(self, p):
        'args : args arg'
        if isinstance(p[1], list):
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = [p[1],p[2]]

    def p_arg_word(self,p):
        'arg : WORD'
        p[0] = p[1]

    def p_arg_num(self, p):
        'arg : NUMBER'
        p[0] = p[1]

    def p_arg_quoted(self, p):
        'arg : QUOT WORD'
        p[0] = p[2]

    def p_error(self, p):
        print 'Error occured!'
        self.q.put_nowait(
            Event(
                self.callback, (['error', 'Not implemented yet', self.cmd], )
                )
            )

    def build(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def parse(self, cmd):
        self.cmd = cmd
        self.parser.parse(cmd, lexer=self.lexer)

import threading

class ParserThread(threading.Thread):
    """
    Thread class for parsing commands parallel with GTK main loop execution
    """

    def __init__(self, vars, command, response):
        """
        Constructor
        
        Arguments:
        yacc -- ply.yacc module ready for parsing
        vars -- dict of variables previously defined by user
        """
        
        threading.Thread.__init__(self)

        self.vars = vars
        self.cmd = command
        self.resp = response

    def run(self):
        print 'parsing...'
        self.yacc.parse(self.cmd)
        print 'parsed'

    from ply import lex, yacc
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

    def p_func_call(t):
        'func_call : func_name args'
        self.resp.append([t[1], t[2]])
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

    def p_arg_qouted(t):
        'arg : QUOT WORD'
        t[0] = t[1]

    @classmethod
    def init_parser(cls):
        cls.yacc = yacc.yacc()

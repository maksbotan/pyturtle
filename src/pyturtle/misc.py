
class ParseError(BaseException):
    """Class ParseErrorException
    """
    # Attributes:
    command = None  # () 
    type = None  # () 
    
    # Operations
    def __init__(self, type):
        """function __init__
        
        command: 
        type: 
        
        returns 
        """
        self.type = type

    def __str__(self):
        return 'Error parsing command "%s": "%s"' % self.type

class ExecutionError(BaseException):
    
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return 'Error executing command "%s": "%s"' % self.reason

class Event:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __call__(self, *args, **kwargs):
        if isinstance(self.args, list) or isinstance(self.args, tuple):
            import threading
            print 'Event.__call__ in thread "%s"' % threading.current_thread().name
            self.func(*self.args)
        elif isinstance(self.args, dict):
            self.func(**self.args)
        else:
            raise TypeError('args must be list, tuple, or dictionary. Instead got: "%s"' % self.args)

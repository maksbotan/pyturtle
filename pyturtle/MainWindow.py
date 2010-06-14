from ParseErrorException import ParseErrorException
from TurtleDrawerGTK import TurtleDrawerGTK

class MainWindow:
    """Class MainWindow
    """
    # Attributes:
    new_command = None  # (Signal) 
    screen = None  # (Gdk.Drawable) 
    __drawer = None  # (TurtleDrawerGTK) 
    
    # Operations
    def __init__(self):
        """function __init__
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def reset(self):
        """function reset
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def run(self):
        """function run
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def new_command(self):
        """function new_command
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def parse_failed(self, exception):
        """function parse_failed
        
        exception: ParseErrorException
        
        returns 
        """
        return None # should raise NotImplementedError()
    


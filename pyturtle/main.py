from misc import ParseErrorException

class Main:
    """Class Main
    """
    # Attributes:
    new_drawline_task = None  # (Signal) 
    new_fill_task = None  # (Signal) 
    new_bg_task = None  # (Signal) 
    new_reset_task = None  # (Signal) 
    new_parsefailed = None  # (Signal) 
    new_drawturtle_task = None  # (Signal) 
    __turtle = None  # (Turtle) 
    
    # Operations
    def __init__(self, gui):
        """function __init__
        
        gui: string
        
        returns 
        """
        
        wndmod = __import__('pyturtle.MainWindow'+gui,fromlist=['MainWindow'+gui])
        wnd = wndmod.MainWindow()

        wnd.run()
        


class Turtle:
    """Class Turtle
    """
    # Attributes:
    __colors = {'0':[0,0,0]}  # (dict of RGB lists) 
    __position = (0,0)  # (tuple of coordinates) 
    
    # Operations
    def __init__(self):
        """function __init__
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def exec_command(self, command):
        """function exec_command
        
        command: list
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __convert_color(self, color):
        """function convert_color
        
        color: 
        
        returns RGB list
        """
        return None # should raise NotImplementedError()
    
    def __fw(self, steps):
        """function fw
        
        steps: 
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __bw(self, steps):
        """function bw
        
        steps: 
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __rt(self, angle):
        """function rt
        
        angle: 
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __lt(self, angle):
        """function lt
        
        angle: 
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __pen_up(self):
        """function pen_up
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __pen_down(self):
        """function pen_down
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __goto(self, place):
        """function goto
        
        place: tuple of coordinates
        
        returns 
        """
        return None # should raise NotImplementedError()
    
class TurtleParser:
    """Class TurtleParser
    """
    # Attributes:
    
    # Operations
    def __init__(self):
        """function __init__
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def parse_command(self, cmd):
        """function parse_command
        
        cmd: string
        
        returns list
        """
        return None # should raise NotImplementedError()

from TurtleParser import TurtleParser
from MainWindow import MainWindow
from Turtle import Turtle

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
        return None # should raise NotImplementedError()
    


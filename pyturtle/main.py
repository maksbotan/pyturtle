from misc import ParseErrorException
import threading
from notify.signal import Signal

class Main:

    def __init__(self, gui):
        
        self.new_drawline_task = Signal()
        self.new_fill_task = Signal()
        self.new_bg_task = Signal()
        self.new_reset_task = Signal()
        self.new_parsefailed = Signal()
        self.new_parsesuccess = Signal()
        self.new_drawturtle_task = Signal()

        self.signals = {
            'drawline': self.new_drawline_task,
            'fill': self.new_fill_task,
            'bg': self.new_bg_task,
            'reset': self.new_reset_task,
            'parsefailed': self.new_parsefailed,
            'parsesuccess': self.new_parsesuccess,
            'drawturtle': self.new_drawturtle_task,
        }

        self.__turtle = Turtle(self.signals)
        self.__parser = TurtleParser()

        wndmod = __import__('pyturtle.MainWindow'+gui,fromlist=['MainWindow'+gui])
        self.wnd = wndmod.MainWindow(self.signals)

        self.wnd.new_command.connect(self.dispatch_command)

        self.gui_thread = threading.Thread(target=self.wnd.run)
        self.gui_thread.start()

    def dispatch_command(self,command):
        try:
            cmd = self.__parser.parse_command(command)
        except ParseErrorException as e:
            self.new_parsefailed(e.command,e.type)
            return
        self.new_parsesuccess()


class Turtle:
    """Class Turtle
    """
    # Attributes:
    __colors = {
        '0':[0,0,0],
        '1':[0,0,255],
        '2':[0,255,0],
        '3':[0,255,255],
        '4':[255,0,0],
        '5':[255,0,255],
        '6':[255,205,0],
        '7':[255,255,255],
        '8':[150,75,0],
        '9':[210,180,140],
        #'10': forest?! That weird! Lets find it out later.
        }  # (dict of RGB lists) 
    __position = (0,0)  # (tuple of coordinates) 
    __angle = 0

    __pen_states = {
        'up': True,
        'down': False,
    }

    __pen_state = __pen_states['up']

    # Operations
    def __init__(self,signals):
        self.signals = signals
    
    def exec_command(self, command):
        return None # should raise NotImplementedError()
    
    def __convert_color(self, color):
        return __colors[color]
    
    def __fw(self, steps):
        return None # should raise NotImplementedError()
    
    def __bw(self, steps):
        return None # should raise NotImplementedError()
    
    def __rt(self, angle):
        self.angle += angle
        self.signals['drawturtle'](self.__position, self.__angle)
   
    def __lt(self, angle):
        self.angle -= angle
        self.signals['drawturtle'](self.__position, self.__angle)

    def __pen_up(self):
        self.__pen_state = self.__pen_states['up']
    
    def __pen_down(self):
        self.__pen_state = self.__pen_states['down']
    
    def __goto(self, place):
        self.__position = place
        self.signals['drawturtle'](self.__position, self.__angle)
    
class TurtleParser:

    def __init__(self):
        """function __init__
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def parse_command(self, cmd):
        raise ParseErrorException(cmd,'Not implemented yet')

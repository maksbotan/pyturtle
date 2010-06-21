"""
main.py: Main, Turtle and TurtleParser classes
This file defines classes that are core of Logo interpreter
"""

from misc import ParseErrorException
import threading
import Queue
from notify.signal import Signal
from math import sin, cos
from pyturtle.parser import ParserThread

import sys
sys.path.insert(1, '/home/maks/pyturtle')

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

        ParserThread.init_parser()

        self.__turtle = Turtle(self.signals)

        wndmod = __import__('pyturtle.MainWindow'+gui,fromlist=['MainWindow'+gui])
        self.wnd = wndmod.MainWindow(self.signals)

        self.wnd.new_command.connect(self.dispatch_command)

        self.wnd.run()

    def dispatch_command(self, command):
        try:
            cmd = self.parse_command(command)
        except ParseErrorException as e:
            self.new_parsefailed(e.command, e.type)
            return
        self.new_parsesuccess()

    def parse_command(self, command):
        response = []
        ParserThread({}, command, response).start()
        raise ParseErrorException(command, 'Not implemented yet')

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
    def __init__(self, signals):
        self.signals = signals
    
    def exec_command(self, command):
        return None # should raise NotImplementedError()
    
    def __convert_color(self, color):
        return self.__colors[color]
    
    def __fw(self, steps):
        new_pos = \
            (self.__position[0] + steps * sin(self.__angle),
            self.__position[1] + steps * cos(self.__angle))
        self.signals['drawline'](self.__position, new_pos)
        self.__position = new_pos
    
    def __bw(self, steps):
        new_pos = \
            (self.__position[0] - steps * sin(self.__angle),
            self.__position[1] - steps * cos(self.__angle))
        self.signals['drawline'](self.__position, new_pos)
        self.__position = new_pos
    
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


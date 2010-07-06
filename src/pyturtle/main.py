"""
main.py: Main, Turtle and TurtleParser classes
This file defines classes that are core of Logo interpreter
"""

from misc import Event, ExecutionError
import threading
import Queue
import sys
from notify.signal import Signal
from math import sin, cos, radians
from pyturtle.parser import parser


class Main:

    def __init__(self, gui):
        
        self.new_drawline_task = Signal()
        self.new_fill_task = Signal()
        self.new_bg_task = Signal()
        self.new_reset_task = Signal()
        self.new_parsefailed = Signal()
        self.new_parsesuccess = Signal()
        self.new_drawturtle_task = Signal()
        self.queue_task = Signal()

        self.signals = {
            'queue_task': self.queue_task,
            'drawline': self.new_drawline_task,
            'fill': self.new_fill_task,
            'bg': self.new_bg_task,
            'reset': self.new_reset_task,
            'parsefailed': self.new_parsefailed,
            'parsesuccess': self.new_parsesuccess,
            'drawturtle': self.new_drawturtle_task,
        }

        self.q = Queue.Queue()
        self.back_q = Queue.Queue()

        self.vars = {}
        self.resp = []

        self.__turtle = Turtle(self.signals, self.back_q)
        self.__parser = parser(
                self.vars,
                self.q,
                self.dispatch_command
            )
        
        wndmod = __import__(
            'pyturtle.MainWindow'+gui,
            fromlist=['MainWindow'+gui])
        self.wnd = wndmod.MainWindow(
            self.signals,
            self.q,
            self.back_q
        )

        self.wnd.new_command.connect(
            self.parse_command)
        self.wnd.gui_exit.connect(
            Event(
                sys.exit, (None, )
                )
            )

        threading.Thread(target=self.wnd.iteration).start()

        while 1:
            event = self.q.get()
            event()

    def dispatch_command(self, command):
        print 'Main.dispatch_command in thread "%s"' % threading.current_thread().name
        if command[0] == 'error':
            self.new_parsefailed(
                command[1]
            )
        else:
            result = self.__turtle.exec_command(command)
            if result is not None:
                self.new_parsefailed(
                    result
                )
            else:
                self.new_parsesuccess()
    
    def parse_command(self, command):
        thrd = threading.Thread(
                target=self.__parser.parse,
                kwargs={'cmd': command}
            )
        thrd.start()
        del thrd

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

    __scale = (640, 380)

    # Operations
    def __init__(self, signals, gui_queue):
        self.signals = signals
        self.q = gui_queue
        
        self.__functions = [
            { 
                'aliases': ['fw', 'forward'],
                'executable': self.__fw,
        #        'arguments': [int, ]
            },
            {
                'aliases': ['rt'],
                'executable': self.__rt,
        #        'arguments': [int]
            }
        ]

    def prototype_checker(arguments):
        def wrapper(f):
            def decorator(*args):
                if len(args) != len(arguments):
                    raise ExecutionError(
                        'Called function takes %d arguments, but only %d given' % (
                            len(arguments),
                            len(args),
                        )
                    )
                for index, arg in enumerate(args):
                    if type(args) != arguments[index]:
                        raise ExecutionError(
                            'Invalid argument "%s" of type "%s": expected "%s"' % (
                                arg,
                                type(arg),
                                arguments(index)
                            )
                        )
                return f(*args)
            return decorator
         return wrapper


    def exec_command(self, command):
        print 'Turtle.exec_command: executing command "%s" in thread "%s"' % (command, threading.current_thread().name)
        try:
            function = self.__check_prototype(*command)
        except ExecutionError as e:
            return e.reason

        function[0](*function[1])
    
    def __convert_color(self, color):
        return self.__colors[color]
    
    def __offscreen_paint(self, new_pos):
        checking_list = [[new_pos[i], self.__scale[i]/2] for i in range(2)]

        def check_if_offscreen(coord, scale):
            if coord > scale:
                return scale
            else:
                return coord

        return [check_if_offscreen(coord, scale) for coord, scale in checking_list]

    def __get_executable(self, func, args):
        for fun in self.__functions:
            print args 
            if func in fun['aliases']:
                if len(args) != len(fun['arguments']) or args == []:
                    raise ExecutionError(
                        '"%s" function takes %d arguments, got %d' % (func, len(fun['arguments']), len(args))
                    )
                for i, arg in enumerate(fun['arguments']):
                    if type(args[i]) != arg:
                        raise ExecutionError(
                            'Invalid argument "%s", expected "%s"' % (args[i], arg)
                        )
                return [fun['executable'], args]
        raise ExecutionError('Unknown function: "%s"' % func)

    @prototype_checker([int])
    def __fw(self, steps):
        new_pos = \
            (self.__position[0] + steps * sin(radians(self.__angle)),
            self.__position[1] + steps * cos(radians(self.__angle)))

        print self.__offscreen_paint(new_pos)

        self.signals['queue_task'](
            self.signals['drawline'],
            (self.__position, new_pos)
        )

        self.__position = new_pos
    
    def __bw(self, steps):
        new_pos = \
            (self.__position[0] - steps * sin(self.__angle),
            self.__position[1] - steps * cos(self.__angle))
        self.signals['drawline'](self.__position, new_pos)
        self.__position = new_pos
    
    def __rt(self, angle):
        self.__angle += angle
        self.signals['drawturtle'](self.__position, self.__angle)
   
    def __lt(self, angle):
        self.__angle -= angle
        self.signals['drawturtle'](self.__position, self.__angle)

    def __pen_up(self):
        self.__pen_state = self.__pen_states['up']
    
    def __pen_down(self):
        self.__pen_state = self.__pen_states['down']
    
    def __goto(self, place):
        self.__position = place
        self.signals['drawturtle'](self.__position, self.__angle)


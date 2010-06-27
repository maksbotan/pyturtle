"""
MainWindowGTK.py: GUI for pyturte Logo intrepreter in GTK
"""

from pyturtle.misc import Event

from TurtleDrawerGTK import TurtleDrawerGTK

import gtk
import gtk.glade
import glib
import gobject
import goocanvas

from notify.all import Signal

class MainWindow:

    """
    MainWindow class imported by pyturtle.main
    Contains functions ("slots") called by interpreter
    """
    
    
    def __init__(self, signals, gui_to_main_queue, main_to_gui_queue):
        
        """Constructor for MainWindow class

        Argumets:

        signals -- Dictionary with all signals defined by Main
        """

        gobject.threads_init()
        gtk.gdk.threads_init()

        self.widgets = gtk.glade.XML(
            'pyturtle/mainwindow.glade'
            ) #Load widgets from Glade-3 file
        #Dictionary of signals defined in Glade file
        signals_dict = {
            'on_commandline_key_press_event':
                self.commandline_key_press,
        }

        self.widgets.signal_autoconnect(signals_dict)
        #Connect GUI signals with handlers in this class

        self.wnd = self.widgets.get_widget('main_window')
        #Get 'main_window' widget from Glade XNL tree

        #TODO: add goocanvas creation
        self.screen = goocanvas.Canvas()
        self.screen.set_size_request(640, 380)
        
        self.widgets.get_widget('vbox1').add(self.screen)
        
        self.wnd.show_all()
        #Show main_window and all containing widgets
        
        self.command_area = self.widgets.get_widget(
            'commands')
        #Get widget representing stack for entered commands

        self.commandline = self.widgets.get_widget(
            'commandline')
        #Get widget representing input line dor new command

        self.new_command = Signal()
        #Initialize new_command signal
        self.gui_exit = Signal()
        #Initialize gui_exit signal

        self.wnd.connect('destroy', self.gui_exit)
        #Connect destroy event window of gui_exit signal

        self.__drawer = TurtleDrawerGTK(self.screen)
        #Initialize drawer

        #Connect signals in main with handlers in drawer and this class
        signals['drawline'].connect(
            self.__drawer.draw_line)
        signals['fill'].connect(
            self.__drawer.fill)
        signals['bg'].connect(
            self.__drawer.paint_background)
        signals['parsefailed'].connect(
            self.parse_failed)
        signals['parsesuccess'].connect(
            self.parse_success)
    
        self.gui_to_main_q =  gui_to_main_queue
        self.main_to_gui_q = main_to_gui_queue

        glib.idle_add(self.recieve_task)

    def reset(self):
        """function reset
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def iteration(self):
        gtk.main()
    
    def parse_failed(self, command, typ):
        print 'parsefailed!'
        dialog = gtk.MessageDialog(
            type=gtk.MESSAGE_ERROR,
            message_format='Error parsing command "%s"' % command
        )
        dialog.format_secondary_text('Reason: "%s"' % typ)
        dialog.show()

    def parse_success(self):
        iter = self.command_area.get_buffer().get_end_iter()
        self.command_area.get_buffer().insert(iter,self.commandline.get_text()+'\n')
        self.commandline.set_text('')
        
    def commandline_key_press(self,widget,event):
        if event.keyval == 65293:
            self.gui_to_main_q.put_nowait(
                Event(
                    self.new_command, (widget.get_text(), )
                    )
                )
            return True
        return False

    def recieve_task(self):
        if not self.main_to_gui_q.empty():
            import threading
            print 'MainWindowGTK.recieve_task in thread "%s"' % threading.current_thread().name
            event = self.main_to_gui_q.get()
            event()
        return True

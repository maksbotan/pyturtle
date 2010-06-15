from TurtleDrawerGTK import TurtleDrawerGTK

import gtk
import gtk.glade

from notify.all import Signal

class MainWindow:
    """Class MainWindow
    """
    # Attributes:
    new_command = None  # (Signal) 
    screen = None  # (Gdk.Drawable) 
    __drawer = None  # (TurtleDrawerGTK) 
    
    # Operations
    def __init__(self,signals):
        self.widgets = gtk.glade.XML('pyturtle/mainwindow.glade') 
        signals_dict = {
            'on_commandline_key_press_event': self.commandline_key_press,
        }

        self.widgets.signal_autoconnect(signals_dict)

        self.wnd = self.widgets.get_widget('main_window')
        self.wnd.connect('destroy',gtk.main_quit)

        self.wnd.show_all()
        
        self.screen = self.widgets.get_widget('screen')
        self.command_area = self.widgets.get_widget('commands')
        self.commandline = self.widgets.get_widget('commandline')

        self.new_command = Signal()
        
        self.__drawer = TurtleDrawerGTK(self.screen) 

        signals['drawline'].connect(self.__drawer.draw_line)
        signals['fill'].connect(self.__drawer.fill)
        signals['bg'].connect(self.__drawer.paint_background)
        signals['parsefailed'].connect(self.parse_failed)
        signals['parsesuccess'].connect(self.parse_success)
    
    def reset(self):
        """function reset
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def run(self):
        gtk.main()
    
    def parse_failed(self, command, typ):
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, message_format='Error parsing command "%s"' % command)
        dialog.format_secondary_text('Reason: "%s"' % typ)
        dialog.show()

    def parse_success(self):
        iter = self.command_area.get_buffer().get_end_iter()
        self.command_area.get_buffer().insert(iter,self.commandline.get_text())
        self.commandline.set_text('')
        
    def commandline_key_press(self,widget,event):
        if event.keyval == 65293:
            self.new_command(widget.get_text())
            return True
        return False

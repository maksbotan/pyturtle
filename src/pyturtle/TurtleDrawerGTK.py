import goocanvas

class TurtleDrawerGTK:
    """Class TurtleDrawerGTK
    """
    # Attributes:
    
    # Operations
    def __init__(self, screen):
        """function __init__
        
        screen: Gdk.Drawable
        
        returns 
        """

        self.canvas = screen
        self.root = screen.get_root_item()
                
        return None # should raise NotImplementedError()
    
    def draw_line(self, start, end, color = [255,255,255]):
        import threading
        print 'TurtleDrawerGTK.draw_line in thread "%s" from %s to %s' % (threading.current_thread().name, start, end)
       
        start = self.__convert_position(start)
        end = self.__convert_position(end)

        goocanvas.polyline_new_line(
            self.root,
            *start+end
        )

        return False # should raise NotImplementedError()
    
    def fill(self, color):
        """function fill
        
        color: RGB list
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def paint_background(self, color = [0,0,0]):
        """function paint_background
        
        color: RGB list
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def draw_turtle(self, place, angle):
        """function draw_turtle
        
        place: tuple
        
        returns 
        """
        return None # should raise NotImplementedError()
    
    def __convert_position(self, position):
        canvas_scale = (640, 380)

        position = [position[i] + canvas_scale[i]/2 if i == 0 else canvas_scale[i] - (position[i] + canvas_scale[i]/2) for i in range(2)]


        real_scale = (
            self.canvas.allocation.width,
            self.canvas.allocation.height
        )

        return tuple(
            [position[i] * real_scale[i]/canvas_scale[i] for i in range(2)]
        )

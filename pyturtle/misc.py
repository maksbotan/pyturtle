
class ParseErrorException(Exception):
    """Class ParseErrorException
    """
    # Attributes:
    command = None  # () 
    type = None  # () 
    
    # Operations
    def __init__(self, command, type):
        """function __init__
        
        command: 
        type: 
        
        returns 
        """
        self.command = command
        self.type = type

"""Text class adapted to handle variables."""
from tkinter import StringVar, END, Text

class VarText(Text):
    """Text class adapted to handle variables."""
    
    variable: StringVar

    def __init__(self, *args, variable=None, **kwargs):
        """Create a text adapted to handle variables."""
        super().__init__(*args, **kwargs)
        self.variable = variable

        if variable is not None:
            # bind the stringvar and the text
            self.bind('<KeyRelease>', self.set_stringvar)
            self.variable.trace("w", self.get_stringvar)
        
    def get_stringvar(self, *args):
        """Fire when the StringVar gets updated."""
        self.replace("1.0", END, self.variable.get())

    def set_stringvar(self, *args):
        """Fire when the text gets updated."""
        self.variable.set(self.get("1.0", END))

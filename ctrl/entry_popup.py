"""Package with a custom popup asking for a string."""
from tkinter import ttk
from tkinter import StringVar, Toplevel

def ask_string(message: str) -> str:
    """Create a popup asking for a string."""
    var = StringVar()
    popup = Toplevel()
    popup.title(message)
    frame = ttk.Frame(popup)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.grid(sticky='nsew')

    def dismiss():
        popup.grab_release()
        popup.destroy()
    
    ttk.Label(frame, text=message + ":").grid(sticky='ew', column=0, row=0)   # something to interact with
    ttk.Entry(frame, textvariable=var).grid(sticky='ew', column=1, row=0)   # something to interact with
    ttk.Button(frame, text="Done", command=dismiss).grid(column=0, row=1, columnspan=2)
    popup.protocol("WM_DELETE_WINDOW", dismiss) # intercept close button
    # popup.transient(root)   # dialog window is related to main
    popup.wait_visibility() # can't grab until window appears, so we wait
    popup.grab_set()        # ensure all input goes to our window
    popup.wait_window()     # block until window is destroyed

    return var.get()

"""Start the program."""
from tkinter import *
from tkinter import ttk

if __name__ == "__main__":
    root = Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    content = ttk.Frame(root)
    content.grid(sticky='nsew')
    content.rowconfigure(0, weight=1)
    content.columnconfigure(1, weight=1)
    content.columnconfigure(2, weight=1)

    f1 = ttk.Frame(content)
    f1['padding'] = (10,)
    f1.grid(row=0, column=1, sticky='nsew')
    f2 = ttk.Frame(content)
    f2['padding'] = (5,15)
    f2['borderwidth'] = 1
    f2['relief'] = 'groove'
    f2.grid(row=0, column=2, sticky='nsew')

    l1 = ttk.Label(f1, text="First label")
    l1.grid()
    l2 = ttk.Label(f1, text="Second label")
    l2.grid()
    l3 = ttk.Label(f1, text="Third label")
    l3.grid()
    l4 = ttk.Label(f2, text="4th label")
    l4.grid()

    b1 = ttk.Button(f2, text="Clk m!", command=lambda: print('weee'))
    b1.grid()
    b2 = ttk.Button(f2, text="M t!", command=lambda: b1.invoke())
    b2.grid()
    
    def disable():
        c1.instate(['!disabled'], lambda: c1.state(['disabled'])) 
        b1.instate(['!disabled'], lambda: b1.state(['disabled']))    # execute 'cmd' if the button is not disabled
        name['show'] = '§'
    def enable():
        c1.instate(['disabled'], lambda: c1.state(['!disabled']))
        b1.instate(['disabled'], lambda: b1.state(['!disabled']))    # execute 'cmd' if the button is not disabled
        name['show'] = ''
    b3 = ttk.Button(f2, text="Enable!", command=enable)
    b3.grid()
    b4 = ttk.Button(f2, text="Disable!", command=disable)
    b4.grid()

    check = StringVar()
    def checkChanged():
        print(c1.instate(['alternate']), c2.instate(['alternate']))
        print(check.get())
    c1 = ttk.Checkbutton(f1, text="Check des 23", command=checkChanged, variable=check, onvalue='True', offvalue='False')
    c1.grid(sticky='ew')
    c2 = ttk.Checkbutton(f1, text="Check des 23...", command=checkChanged, variable=check, onvalue='', offvalue='True')
    c2.grid(sticky='ew')


    phone = StringVar()
    home = ttk.Radiobutton(f2, text='Home', variable=phone, value='home')
    office = ttk.Radiobutton(f2, text='Office', variable=phone, value='office')
    cell = ttk.Radiobutton(f2, text='Mobile', variable=phone, value='cell')
    home.grid()
    office.grid()
    cell.grid()


    import model.nvn as n
    username = StringVar()
    def validateNVNcallback(input):
        return all(c in n.ALPHABET for c in input)

    name = ttk.Entry(f2, textvariable=username)
    reg = f2.register(validateNVNcallback) # Register the callback function
    name['validate'] = "key"
    name['validatecommand'] = (reg, '%P')
    print('current value is %s' % name.get())
    name.grid(columnspan=2, rowspan=1)
    name.delete(0,'end')          # delete between two indices, 0-based
    name.insert(0, 'your name')   # insert new text at a given index

    #t = Text(f1, width=40, height=10)
    t = Text(f1, wrap="word")
    t.grid(sticky='ew')

    root.mainloop()

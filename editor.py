"""Editor for the Novan lexical network."""
from tkinter import Tk, font
from tkinter import ttk
from view.editor import setup_verb_ui
from ctrl.editor import VerbEditorController

if __name__ == "__main__":
    # verb mode
    # create UI
    root = Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    content = ttk.Frame(root)
    content.grid(sticky='nsew')
    content.rowconfigure(1, weight=1)
    content.columnconfigure(0, weight=2)
    content.columnconfigure(2, weight=1)

    # load model/controller
    controller = VerbEditorController(root)

    # fill UI
    setup_verb_ui(content, controller)

    # change font
    for font_name in ["TkDefaultFont",
            "TkTextFont",
            "TkFixedFont",
            "TkMenuFont",
            "TkHeadingFont",
            "TkCaptionFont",
            "TkSmallCaptionFont",
            "TkIconFont",
            "TkTooltipFont"]:
        font_ = font.nametofont(font_name)
        font_.configure(size=font_["size"] - 6)

    # run
    root.mainloop()

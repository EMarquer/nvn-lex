"""Editor for the Novan lexical network."""
from tkinter import Tk, font
from ctrl.editor import EditorController

if __name__ == "__main__":
    # verb mode
    # create UI
    root = Tk()

    # load model/controller
    controller = EditorController()

    # fill UI
    controller.setup_ui(root)

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

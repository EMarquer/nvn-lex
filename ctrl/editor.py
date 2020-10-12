"""Controller of the editor for the Novan lexical network verbs."""
from tkinter import Tk, ttk, VERTICAL, messagebox
from model import Verb
from .verb_data import VerbDataController
from .verb_list import VerbSelectorController
from .verb_editor import VerbEditorController
from .generator import GeneratorController

class EditorController:
    """Controller of the editor for the Novan lexical network verbs."""

    root: Tk
    content: ttk.Frame
    verb_data_controller: VerbDataController
    verb_list_controller: VerbSelectorController
    wordform_generator_controller: GeneratorController

    def __init__(self):
        """Create a controller of the editor for the Novan lexical network verbs."""
        self.root = None
        self.content = None
        self.verb_data_controller = VerbDataController()
        self.verb_list_controller = VerbSelectorController(self.verb_data_controller)
        self.verb_list_controller.editor_refresh = self.refresh
        self.verb_editor_controller = VerbEditorController(self.verb_list_controller)
        self.wordform_generator_controller = GeneratorController(self.verb_data_controller)

    def refresh(self):
        """Update view with data from the model."""
        verb = self.verb_list_controller.current_verb

        if verb is not None:
            self.root.title(f"{verb.nvn} - Novan Lexical Network Editor")
        else:
            self.root.title(f"Novan Lexical Network Editor")

        self.verb_editor_controller.refresh()

    def setup_ui(self, parent: Tk):
        """Initialize the view.
        
        Parameters:
            parent: The parent widget.
        """
        # setup parent
        self.root = parent
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.content = ttk.Frame(self.root)
        self.content.grid(sticky='nsew')
        self.content.rowconfigure(1, weight=1)
        self.content.columnconfigure(0, weight=2)
        self.content.columnconfigure(2, weight=1)

        # sub-ui frames
        ui_right_frame = ttk.Frame(self.content)
        ui_right_frame.rowconfigure(0, weight=1)
        ui_right_frame.columnconfigure(0, weight=1)
        ui_right_frame.columnconfigure(1, weight=1)
        ui_right_frame.columnconfigure(2, weight=1)
        ui_right_frame.grid(sticky='nsew', row=1, column=0)
        sep = ttk.Separator(self.content, orient=VERTICAL)
        sep.grid(sticky='ns', row=1, column=1)
        ui_list_frame = ttk.Frame(self.content)
        ui_list_frame.grid(sticky='nsew', row=1, column=2)

        # notebook
        tabs = ttk.Notebook(ui_right_frame)
        tabs.grid(sticky='nsew', row=0, columnspan=3)
        tab_edit = ttk.Frame(tabs)
        tab_relate = ttk.Frame(tabs)
        tab_statistics = ttk.Frame(tabs)
        tabs.add(tab_edit, text="Edit Verb")
        tabs.add(tab_relate, text="Relate Verbs")
        tabs.add(tab_statistics, text="Statistics")

        # buttons
        button_new = ttk.Button(ui_right_frame, text="New Verb", command=self.create_verb)
        button_remove = ttk.Button(ui_right_frame, text="Remove Verb", command=self.remove_verb)
        button_save = ttk.Button(ui_right_frame, text="Save", command=self.verb_data_controller.save)
        button_new.grid(sticky='nsew', row=1, column=0)
        button_remove.grid(sticky='nsew', row=1, column=1)
        button_save.grid(sticky='nsew', row=1, column=2)
        self.root.bind("<Control-s>", lambda x: button_save.invoke())

        # sub-ui setup
        self.verb_editor_controller.setup_ui(tab_edit)
        self.verb_list_controller.setup_ui(ui_list_frame)

        # generator window
        self.wordform_generator_controller.setup_ui(self.root)

    def create_verb(self):
        """Create a verb and set it active."""
        # If the new verb is in the list, select it
        verb = Verb(nvn="#", en="new verb", prime="Not a prime")
        self.verb_data_controller.verbs.append(verb)
        self.verb_list_controller.current_verb = verb
        self.verb_list_controller.refresh()
        self.verb_editor_controller.refresh()

    def remove_verb(self):
        """Delete the currently selected verb."""
        verb = self.verb_list_controller.current_verb

        if messagebox.askokcancel(
                message=f'Are you sure you want to remove "{verb.nvn}"?',
                icon='warning', title='Remove verb'):
            self.verb_data_controller.verbs.remove(verb)
            self.verb_list_controller.current_verb = None
            self.verb_list_controller.refresh()
            self.verb_editor_controller.refresh()

"""Verb editor controller."""
from tkinter import StringVar, BooleanVar, VERTICAL
from tkinter import ttk
from view.var_text import VarText
from .verb_list import VerbSelectorController
from .wordform import WordformController
from .constants import PRIME_TYPES

class VerbEditorController:
    """Verb list and selector controller class."""

    verb_list_controller: VerbSelectorController

    nvn_controller: WordformController
    nvn_description_controller: WordformController

    var_en: StringVar

    var_is_generic: BooleanVar
    var_is_state: BooleanVar
    var_is_process: BooleanVar
    var_is_cognition: BooleanVar
    var_is_transfer: BooleanVar
    var_prime: StringVar

    def __init__(self, verb_list_controller: VerbSelectorController):
        """Create a verb list and selector controller.
        
        Parameters:
            verb_list_controller: The controller handling the verb selection.
        """
        self.verb_list_controller = verb_list_controller

        self.nvn_controller = WordformController()
        self.nvn_description_controller = WordformController()

        self.var_en = StringVar("")
        self.var_is_generic = BooleanVar(False)
        self.var_is_state = BooleanVar(False)
        self.var_is_process = BooleanVar(False)
        self.var_is_cognition = BooleanVar(False)
        self.var_is_transfer = BooleanVar(False)
        self.var_prime = StringVar("")

        self.var_en_desc = StringVar("")

    def refresh(self):
        """Update view with data from the model."""
        verb = self.verb_list_controller.current_verb

        if verb is not None:
            self.nvn_controller.nvn.set(verb.nvn)
            self.nvn_controller.nvn_syllables.set('|'.join(verb.nvn_syllables))
            self.var_en.set(verb.en)
            self.var_is_generic.set(verb.is_generic)
            self.var_is_state.set(verb.is_state)
            self.var_is_process.set(verb.is_process)
            self.var_is_cognition.set(verb.is_cognition)
            self.var_is_transfer.set(verb.is_transfer)
            self.var_prime.set(verb.prime)

            self.nvn_description_controller.nvn.set(verb.nvn_desc)
            self.var_en_desc.set(verb.en_desc)

        else:
            self.nvn_controller.nvn.set("")
            self.var_en.set("")
            self.var_is_generic.set(False)
            self.var_is_state.set(False)
            self.var_is_process.set(False)
            self.var_is_cognition.set(False)
            self.var_is_transfer.set(False)
            self.var_prime.set("")

            self.nvn_description_controller.nvn.set("")
            self.var_en_desc.set("")

    def update(self, *args):
        """Update model with data from the view."""
        verb = self.verb_list_controller.current_verb

        if verb is None:
            return

        try:
            verb.set_nvn(self.nvn_controller.nvn.get())
        except ValueError:
            return

        verb.en = self.var_en.get()
        verb.is_generic = self.var_is_generic.get()
        verb.is_state = self.var_is_state.get()
        verb.is_process = self.var_is_process.get()
        verb.is_cognition = self.var_is_cognition.get()
        verb.is_transfer = self.var_is_transfer.get()
        verb.prime = self.var_prime.get()

        verb.nvn_desc = self.nvn_description_controller.nvn.get()
        verb.en_desc = self.var_en_desc.get()

        self.verb_list_controller.refresh()

    def setup_ui(self, parent):
        """Initialize the view.
        
        Parameters:
            parent: The parent widget.
        """
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        nvn_en_frame = ttk.Frame(parent)
        type_frame = ttk.Frame(parent)
        desc_frame = ttk.Frame(parent)
        nvn_en_frame.grid(sticky='nsew', row=0, column=0)
        type_frame.grid(sticky='nsew', row=1, column=0)
        desc_frame.grid(sticky='nsew', row=2, column=0)
        
        self._setup_nvn_en_ui(nvn_en_frame)
        self._setup_type_ui(type_frame)
        self._setup_desc_ui(desc_frame)

        self.refresh()

    def _setup_nvn_en_ui(self, parent):
        """Initialize the wordform entries, syllable display and prime type selector of the view.
        
        Parameters:
            parent: The parent widget.
        """
        parent.columnconfigure(1, weight=1)

        # Novan
        nvn_label = ttk.Label(parent, text="Novan ")
        nvn_entry = ttk.Entry(parent, textvariable=self.nvn_controller.nvn)
        # Novan syllables
        nvn_syllables_label = ttk.Label(parent, text="Syllables ")
        nvn_syllables = ttk.Label(parent, textvariable=self.nvn_controller.nvn_syllables)
        nvn_play = ttk.Button(parent, text="Play", command=self.nvn_controller.pronounce)
        # English
        en_label = ttk.Label(parent, text="English ")
        en_entry = ttk.Entry(parent, textvariable=self.var_en)
        # Prime type
        prime_label = ttk.Label(parent, text="Prime type ")
        prime_box = ttk.Combobox(parent, textvariable=self.var_prime, values=tuple(PRIME_TYPES), state="readonly")

        nvn_label.grid(sticky='ew', row=0, column=0)
        nvn_entry.grid(sticky='ew', row=0, column=1, columnspan=2)
        nvn_syllables_label.grid(sticky='ew', row=1, column=0)
        nvn_syllables.grid(sticky='ew', row=1, column=1)
        nvn_play.grid(sticky='ew', row=1, column=2)
        en_label.grid(sticky='ew', row=2, column=0)
        en_entry.grid(sticky='ew', row=2, column=1, columnspan=2)
        prime_label.grid(sticky='ew', row=3, column=0)
        prime_box.grid(sticky='ew', row=3, column=1, columnspan=2)

        # Bindings
        reg = parent.register(lambda x: self.nvn_description_controller.validate_entry(nvn_entry, x))
        nvn_entry['validate'] = "key"
        nvn_entry['validatecommand'] = (reg, '%P')

        nvn_entry.bind("<KeyRelease>", self.update)
        en_entry.bind("<KeyRelease>", self.update)
        prime_box.bind("<<ComboboxSelected>>", self.update)

    def _setup_type_ui(self, parent):
        """Initialize the verb type selector of the view.
        
        Parameters:
            parent: The parent widget.
        """
        parent.columnconfigure(0, weight=1)
        type_frame = ttk.Labelframe(parent, text='Verb type')
        type_frame.grid(sticky='nsew')
        generic = ttk.Checkbutton(type_frame, text='Generic action', variable=self.var_is_generic)
        state = ttk.Checkbutton(type_frame, text='State', variable=self.var_is_state)
        process = ttk.Checkbutton(type_frame, text='Process', variable=self.var_is_process)
        cognition = ttk.Checkbutton(type_frame, text='Cognition', variable=self.var_is_cognition)
        transfer = ttk.Checkbutton(type_frame, text='Transfer', variable=self.var_is_transfer)
        generic.grid(sticky='ew', row=1, column=0)
        state.grid(sticky='ew', row=2, column=0)
        process.grid(sticky='ew', row=3, column=0)
        cognition.grid(sticky='ew', row=4, column=0)
        transfer.grid(sticky='ew', row=5, column=0)
        
        # bindings
        for checkbutton in [generic, state, process, cognition, transfer]:
            checkbutton["command"] = self.update

    def _setup_desc_ui(self, parent):
        """Initialize the description editors of the view.

        TODO:
            Add Novan description validation.
        
        Parameters:
            parent: The parent widget.
        """
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        desc_label = ttk.Labelframe(parent, text='Description')
        desc_label.grid(sticky='nsew')
        desc_label.columnconfigure(0, weight=1)
        desc_label.rowconfigure(0, weight=1)
        desc = ttk.Panedwindow(desc_label, orient=VERTICAL)
        desc.grid(sticky='nsew')

        # Labelframes
        nvn_desc_label = ttk.Labelframe(desc, text='Novan')
        en_desc_label = ttk.Labelframe(desc, text='English')
        nvn_desc_label.grid(sticky='nsew')
        en_desc_label.grid(sticky='nsew')
        nvn_desc_label.columnconfigure(0, weight=1)
        en_desc_label.columnconfigure(0, weight=1)
        nvn_desc_label.rowconfigure(0, weight=1)
        en_desc_label.rowconfigure(0, weight=1)
        desc.add(nvn_desc_label)
        desc.add(en_desc_label)

        # Text fields
        # Novan
        self.text_nvn_desc = VarText(nvn_desc_label, wrap="word", height=10, width=60,
            variable=self.nvn_description_controller.nvn)
        self.text_nvn_desc.grid(sticky='nsew', column=0, row=0)
        nvn_scrollbar = ttk.Scrollbar(nvn_desc_label, orient=VERTICAL, command=self.text_nvn_desc.yview)
        self.text_nvn_desc.configure(yscrollcommand=nvn_scrollbar.set)
        nvn_scrollbar.grid(sticky='nse', column=1, row=0)
        
        # English
        self.text_en_desc = VarText(en_desc_label, wrap="word", height=10, width=60, variable=self.var_en_desc)
        self.text_en_desc.grid(sticky='nsew', column=0, row=0)
        en_scrollbar = ttk.Scrollbar(en_desc_label, orient=VERTICAL, command=self.text_en_desc.yview)
        self.text_en_desc.configure(yscrollcommand=en_scrollbar.set)
        en_scrollbar.grid(sticky='nse', column=1, row=0)

        # Bindings
        self.text_nvn_desc.bind("<KeyRelease>", self.update)
        self.text_en_desc.bind("<KeyRelease>", self.update)

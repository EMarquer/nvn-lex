"""Verb list and selector controller."""
from tkinter import StringVar, BooleanVar, ttk, Listbox, VERTICAL
import typing as t
from model import Verb
from .verb_data import VerbDataController
from .constants import PRIME_TAGS

class VerbSelectorController:
    """Verb list and selector controller class."""

    verb_data_controller: VerbDataController # verb list and I/O
    current_verb: Verb
    editor_refresh: t.Callable

    var_filter: StringVar
    var_is_nvn: BooleanVar
    var_check_prime: BooleanVar
    var_check_completion: BooleanVar
    
    current_verbs: t.List[Verb]
    var_verbs: StringVar
    listbox_verbs: Listbox

    def __init__(self, verb_data_controller: VerbDataController):
        """Create a verb list and selector controller.
        
        Parameters:
            verb_data_controller: The data controller handling the verb data to use.
        """
        self.verb_data_controller = verb_data_controller
        self.current_verb = None
        self.editor_refresh = None

        # Vars
        self.var_is_nvn = BooleanVar(value=True)
        self.var_filter = StringVar(value="")
        self.var_check_prime = BooleanVar(value=False)
        self.var_check_completion = BooleanVar(value=False)

        self.var_verbs = StringVar()
        self.current_verbs = None

    def refresh(self):
        """Update view with data from the model."""
        self.filter_verbs()

        # If the currently edited verb is in the list, select it
        if self.current_verb is not None and self.current_verb in self.current_verbs:
            index = self.current_verbs.index(self.current_verb)
            self.listbox_verbs.selection_clear(0, len(self.current_verbs))
            self.listbox_verbs.selection_set(index, index)

        if self.editor_refresh is not None:
            self.editor_refresh()

    def update(self, *args):
        """Update model with data from the view."""
        pass

    def setup_ui(self, parent):
        """Initialize the view.
        
        Parameters:
            parent: The parent widget.
        """
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)
        search_ui = ttk.Labelframe(parent, text="Search verbs")
        search_ui.columnconfigure(0, weight=1)
        search_ui.columnconfigure(1, weight=1)
        search_ui.grid(sticky='nsew', row=1, column=0, columnspan=2)

        # searchbar -> filter list
        entry_search = ttk.Entry(search_ui, textvariable=self.var_filter)
        entry_search.grid(sticky='nsew', row=0, column=0, columnspan=2)
        entry_search.bind("<KeyRelease>", self.refresh)

        # search options
        radio_nvn = ttk.Radiobutton(search_ui, text="Novan", variable=self.var_is_nvn, value=True,
            command=self.refresh)
        radio_en = ttk.Radiobutton(search_ui, text="English", variable=self.var_is_nvn, value=False,
            command=self.refresh)
        check_prime = ttk.Checkbutton(search_ui, text='Prime label', variable=self.var_check_prime)
        check_completion = ttk.Checkbutton(search_ui, text='Completion rate', variable=self.var_check_completion)
        radio_nvn.grid(sticky='ew', row=1, column=0)
        radio_en.grid(sticky='ew', row=1, column=1)
        check_prime.grid(sticky='ew', row=2, column=0)
        check_completion.grid(sticky='ew', row=2, column=1)
        check_prime["command"] = self.refresh
        check_completion["command"] = self.refresh

        # list
        self.listbox_verbs = Listbox(parent, height=10, listvariable=self.var_verbs)
        self.listbox_verbs.bind("<<ListboxSelect>>", self.select_event)
        scrollbar = ttk.Scrollbar(parent, orient=VERTICAL, command=self.listbox_verbs.yview)
        self.listbox_verbs.configure(yscrollcommand=scrollbar.set)
        self.listbox_verbs.grid(sticky='nsew', row=2, columnspan=2)
        scrollbar.grid(sticky='nse', row=2, column=2)

        self.refresh()

    def select_event(self, *args):
        """Update the current verb in accordance to the selected verb in the list."""
        if len(indices := self.listbox_verbs.curselection()) == 1:
            index = int(indices[0])
            self.current_verb = self.current_verbs[index]
            self.refresh()

    def filter_verbs(self):
        """Filter the list of verbs from the data controller."""
        verb_list = []
        for verb in self.verb_data_controller.verbs:
            # get label in the correct language
            verb_label = verb.nvn if self.var_is_nvn.get() else verb.en

            # add completion rate
            if self.var_check_completion.get():
                criterion = (
                    any((verb.is_cognition,
                        verb.is_generic,
                        verb.is_process,
                        verb.is_state,
                        verb.is_transfer)),
                    verb.nvn != "",
                    verb.en != "",
                    verb.nvn_desc != "",
                    verb.en_desc != "",
                    verb.prime != "")
                verb_label = f"[{sum(criterion)}/{len(criterion)}] " + verb_label

            # add prime label
            if self.var_check_prime.get():
                verb_label = PRIME_TAGS.get(verb.prime, "?") + " " + verb_label

            # filtering
            if not (search := self.var_filter.get().strip().lower()) or search in verb_label:
                verb_list.append((verb_label, verb,))

        verb_list = sorted(verb_list, key=lambda x: x[0])

        self.current_verbs = [x[1] for x in verb_list]
        self.var_verbs.set(tuple(x[0] for x in verb_list))

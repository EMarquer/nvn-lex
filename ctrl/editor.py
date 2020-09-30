"""Controller of the editor for the Novan lexical network."""
from tkinter import StringVar, BooleanVar, Listbox, Tk, messagebox, Text, END
from tkinter import ttk
import typing as t
from model import Verb
from model.nvn import ALPHABET, is_valid
import pandas as pd
from ast import literal_eval

PRIME_TYPES = ["Action", "Meta", "Thing"]
START = "0.0"
class VerbEditorController:
    """Controller of the editor for the Novan lexical network."""

    root: Tk
    data_path: str
    verbs: t.List[Verb]
    current_verb: Verb
    var_is_modified: BooleanVar

    # verb list
    var_search: StringVar
    var_is_search_nvn: BooleanVar
    var_show_prime: BooleanVar
    var_show_completion: BooleanVar
    var_list_verbs: StringVar
    current_verb_list: t.List[Verb]
    list_verbs: Listbox

    # verb editor
    var_nvn: StringVar
    var_nvn_syllables: StringVar
    var_en: StringVar
    text_nvn_desc: Text
    text_en_desc: Text
    var_is_generic: BooleanVar
    var_is_state: BooleanVar
    var_is_process: BooleanVar
    var_is_cognition: BooleanVar
    var_is_transfer: BooleanVar
    var_prime: StringVar

    def __init__(self, root: Tk, data_path: str="data/verbs.csv"):
        self.data_path = data_path
        self.load_()

        self.current_verb = None
        self.var_is_search_nvn = BooleanVar(value=True)
        self.var_search = StringVar(value="")
        self.var_list_verbs = StringVar()
        self.list_verbs = None
        self.root = root
        self.var_show_prime = BooleanVar(value=False)
        self.var_show_completion = BooleanVar(value=False)
        self.var_is_modified = BooleanVar(value=False)

        self.var_nvn = StringVar(value="")
        self.var_nvn_syllables = StringVar(value="")
        self.var_en = StringVar(value="")
        self.text_nvn_desc = None
        self.text_en_desc = None
        self.var_is_generic = BooleanVar(value=False)
        self.var_is_state = BooleanVar(value=False)
        self.var_is_process = BooleanVar(value=False)
        self.var_is_cognition = BooleanVar(value=False)
        self.var_is_transfer = BooleanVar(value=False)
        self.var_prime = StringVar(value="")

        self.update_verb_list()
    
    def save_(self):
        """Save the verb data to the CSV file."""
        df = pd.DataFrame.from_records([v.__dict__ for v in self.verbs])
        df.to_csv(self.data_path)
        
    def load_(self):
        """Load the verb data from the CSV file."""
        self.verbs = []
        try:
            df = pd.read_csv(self.data_path, index_col=0, keep_default_na=False,
                converters={'nvn_syllables': literal_eval})
            for index, row in df.iterrows():
                verb_dict = {name: value for name, value in zip(df.columns, row)}
                verb = Verb(**verb_dict)
                self.verbs.append(verb)
        except Exception as e:
            print(f"Unable to load file '{self.data_path}', aborting: {e}")

    def update_verb_list(self, *args):
        verb_list = []
        for verb in self.verbs:
            # get label in the correct language
            verb_label = verb.nvn if self.var_is_search_nvn.get() else verb.en

            # add completion rate
            if self.var_show_completion.get():
                count = 0
                if any((verb.is_cognition,
                        verb.is_generic,
                        verb.is_process,
                        verb.is_state,
                        verb.is_transfer)):
                    count += 1
                if verb.nvn: count += 1
                if verb.en: count += 1
                if verb.nvn_desc: count += 1
                if verb.en_desc: count += 1
                verb_label = f"[{count}/5] " + verb_label

            # add prime label
            if self.var_show_prime.get():
                if verb.prime in PRIME_TYPES:
                    verb_label = verb.prime[0] + " " + verb_label
                else:
                    verb_label = ". " + verb_label

            # filtering
            if not (search := self.var_search.get().strip().lower()) or search in verb_label:
                verb_list.append((verb_label, verb,))

        verb_list = sorted(verb_list, key=lambda x: x[0])

        self.current_verb_list = [x[1] for x in verb_list]
        self.var_list_verbs.set(tuple(x[0] for x in verb_list))

        # If the currently edited verb is in the list, select it
        if self.list_verbs is not None and self.current_verb is not None and self.current_verb in self.current_verb_list:
            index = self.current_verb_list.index(self.current_verb)
            self.list_verbs.selection_clear(0, len(self.current_verb_list))
            self.list_verbs.selection_set(index, index)

    def select(self, *args):
        if self.list_verbs is not None and len(indices := self.list_verbs.curselection()) == 1:
            index = int(indices[0])
            self.current_verb = self.current_verb_list[index]
            self.update_verb()

    def update_verb(self):
        """Synchronize the verb variables with the actual verb values."""
        if self.current_verb is not None:
            self.var_nvn.set(self.current_verb.nvn)
            self.var_nvn_syllables.set('-'.join(self.current_verb.nvn_syllables))
            self.var_en.set(self.current_verb.en)
            self.set_text(self.text_nvn_desc, self.current_verb.nvn_desc)
            self.set_text(self.text_en_desc, self.current_verb.en_desc)
            self.var_is_generic.set(self.current_verb.is_generic)
            self.var_is_state.set(self.current_verb.is_state)
            self.var_is_process.set(self.current_verb.is_process)
            self.var_is_cognition.set(self.current_verb.is_cognition)
            self.var_is_transfer.set(self.current_verb.is_transfer)
            self.var_prime.set(self.current_verb.prime)
        else:
            self.var_nvn.set("")
            self.var_nvn_syllables.set("")
            self.var_en.set("")
            self.var_nvn_description.set("")
            self.var_en_description.set("")
            self.var_is_generic.set(False)
            self.var_is_state.set(False)
            self.var_is_process.set(False)
            self.var_is_cognition.set(False)
            self.var_is_transfer.set(False)
            self.var_prime.set("")

        self.change_win_title()

    def validate_nvn_entry(self, entry: ttk.Entry, nvn):
        """Validates an entry."""
        is_alphabetic = all(c in ALPHABET for c in nvn)
        if not is_valid(nvn):
            entry_invalid_style = ttk.Style()
            entry_invalid_style.configure("BW.TEntry", foreground='red')
            entry.config(style="BW.TEntry")
        else:
            entry.config(style="")
        return is_alphabetic
    def validate_nvn_text(self, text: Text, nvn):
        """Validates an entry."""
        is_alphabetic = all(c in ALPHABET for c in nvn)
        if not is_valid(nvn):
            text.config(foreground='red')
        else:
            text.config(foreground='red')
        return is_alphabetic

    def update_nvn(self, *args):
        if self.current_verb is not None:
            try:
                self.current_verb.set_nvn(self.var_nvn.get())
                self.var_nvn_syllables.set('-'.join(self.current_verb.nvn_syllables))
            except ValueError:
                return
        self.update_verb_list()
    def update_nvn_desc(self, *args):
        if self.current_verb is not None:
            self.current_verb.nvn_desc = self.text_nvn_desc.get(START, END)
    def update_en_desc(self, *args):
        if self.current_verb is not None:
            self.current_verb.en_desc = self.text_en_desc.get(START, END)
    def set_text(self, text: Text, value: str):
        text.delete(START, END)
        text.insert(START, value)

    def update_en(self, *args):
        if self.current_verb is not None:
            self.current_verb.en = self.var_en.get()
        self.update_verb_list()
    def update_verb_type(self):
        if self.current_verb is not None:
            self.current_verb.is_generic = self.var_is_generic.get()
            self.current_verb.is_state = self.var_is_state.get()
            self.current_verb.is_process = self.var_is_process.get()
            self.current_verb.is_cognition = self.var_is_cognition.get()
            self.current_verb.is_transfer = self.var_is_transfer.get()
        self.update_verb_list()
    def update_prime(self):
        if self.current_verb is not None:
            self.current_verb.prime = self.var_prime.get()
        self.update_verb_list()

    def create_new_verb(self):
        # If the new verb is in the list, select it
        self.current_verb = Verb(nvn="#", en="New Verb")
        self.verbs.append(self.current_verb)
        self.update_verb()
        self.update_verb_list()

    def save(self):
        if messagebox.askokcancel(
                message=f'Are you sure you want to overwrite the data?',
                icon='warning', title='Save'):
            self.save_()

    def remove_verb(self):
        if messagebox.askokcancel(
                message=f'Are you sure you want to remove "{self.current_verb.nvn}"?',
                icon='warning', title='Remove verb'):
            self.verbs.remove(self.current_verb)
            self.current_verb = None
            self.update_verb()
            self.update_verb_list()

    def pronounce(self):
        self.current_verb.nvn_syllables
        pass

    def change_win_title(self):
        if self.current_verb is not None:
            self.root.title(f"{self.current_verb.nvn} - Novan Lexical Network Editor")
        else:
            self.root.title(f"Novan Lexical Network Editor")
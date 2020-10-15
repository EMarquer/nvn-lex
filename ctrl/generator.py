"""Wordform generator controller."""
from tkinter import StringVar, BooleanVar, HORIZONTAL, Toplevel, messagebox
from tkinter import ttk
import typing as t
from .verb_data import VerbDataController
from .wordform import WordformController
from .entry_popup import ask_string
from model.nvn import CONSONANTS, VOWELS
from model.generator import Generator
import pandas as pd

PAD = 5
MINSIZE = 300
GENERATORS_PATH = "data/generators.csv"
class GeneratorController:
    """Wordform generator controller class."""

    verb_data_controller: VerbDataController
    wordform_controller: WordformController

    var_vowels: t.Dict[str, StringVar]
    var_consonants: t.Dict[str, StringVar]
    var_generator: StringVar
    var_limit_generator: BooleanVar
    var_syllable_count: StringVar

    generators: t.Dict[str, Generator]
    generator_combobox: ttk.Combobox

    def __init__(self, verb_data_controller: VerbDataController):
        """Create a wordform generator controller.
        
        Parameters:
            verb_list_controller: The controller handling the verb selection.
        """
        self.var_generator = StringVar()
        self.var_vowels = {v: StringVar() for v in VOWELS}
        self.var_consonants = {c: StringVar() for c in CONSONANTS}
        self.var_syllable_count = StringVar(value="1")
        self.var_limit_generator = BooleanVar(value=True)

        self.verb_data_controller = verb_data_controller
        self.wordform_controller = WordformController()
        self.generator_combobox = None

        self.load_generators()

    def load_generators(self):
        """Load the generator dictionary."""
        self.generators = {}
        try:
            df = pd.read_csv(GENERATORS_PATH, index_col=0, keep_default_na=False)
            for index, row in df.iterrows():
                weight_map = {name: value for name, value in zip(df.columns, row)}
                generator_name = weight_map.pop('generator_name')
                generator = Generator(weight_map)
                self.generators[generator_name] = generator
        except Exception as e:
            print(f"Unable to load file '{GENERATORS_PATH}', aborting: {e}")
            self.generators = {
                "Custom": Generator()
            }

    def save_generators(self):
        """Save the generator dictionary."""
        if messagebox.askokcancel(
                message=f'Are you sure you want to overwrite the generator data?',
                icon='warning', title='Save'):
            df = pd.DataFrame.from_records([
                {'generator_name': generator_name, **generator.weight_map}
                for generator_name, generator in self.generators.items()])
            df.to_csv(GENERATORS_PATH)

    def current_generator(self) -> Generator:
        """Return the currently active wordform generator."""
        return self.generators[self.var_generator.get()]

    def new_generator(self) -> Generator:
        """Create a new wordform generator."""
        self.generators[ask_string("Enter the name of the new generator")] = Generator()
        self.generator_combobox["values"] = tuple(self.generators.keys())
        self.refresh()

    def generate(self):
        """Generate a wordform using the currently selected generator."""
        forbidden = [
            v.nvn for v in self.verb_data_controller.verbs
        ] if self.var_limit_generator.get() else []
        wordform = self.current_generator().generate(int(self.var_syllable_count.get()), forbidden)
        self.wordform_controller.nvn.set(wordform)

    def refresh(self):
        """Update view with data from the model."""
        # Load the values from the weight dict
        for key in self.var_consonants.keys():
            self.var_consonants[key].set(self.current_generator().weight_map[key] * 100)
        for key in self.var_vowels.keys():
            self.var_vowels[key].set(self.current_generator().weight_map[key] * 100)

    def update(self, *args):
        """Update model with data from the view."""
        # Set the values of the weight dict
        for key in self.var_consonants.keys():
            self.current_generator().weight_map[key] = float(self.var_consonants[key].get()) / 100
        for key in self.var_vowels.keys():
            self.current_generator().weight_map[key] = float(self.var_vowels[key].get()) / 100
        self.current_generator().update_weights()

    def setup_ui(self, parent):
        """Initialize the view.
        
        Parameters:
            parent: The parent widget.
        """
        window = Toplevel(parent)
        window.protocol("WM_DELETE_WINDOW", parent._root().destroy)
        window.title("Wordform Generator - Novan Lexical Network Editor")
        content = ttk.Frame(window)
        content.grid(sticky='nsew')
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        wordform_frame = ttk.Frame(content)
        wordform_frame.grid(sticky='nsew', column=0, row=0)
        wordform_frame.columnconfigure(0, weight=1)
        selector_frame = ttk.Frame(content)
        selector_frame.grid(sticky='nsew', column=0, row=1)
        selector_frame.columnconfigure(0, weight=1)
        vowels_frame = ttk.Frame(content)
        vowels_frame.grid(sticky='nsew', column=0, row=2)
        vowels_frame.columnconfigure(0, weight=1)
        consonants_frame = ttk.Frame(content)
        consonants_frame.grid(sticky='nsew', column=1, row=0, rowspan=3)
        consonants_frame.columnconfigure(0, weight=1)

        # generator entry (readonly) and buttons
        self._setup_wordform_ui(wordform_frame)

        # generator selector
        self._setup_selector_ui(selector_frame)

        # generator parameters
        self._setup_vowels_ui(vowels_frame)
        self._setup_consonants_ui(consonants_frame)

        self.refresh()

    def _setup_wordform_ui(self, parent):
        """Initialize the generator output and controll view.
        
        Parameters:
            parent: The parent widget.
        """
        nvn = ttk.Label(parent, textvariable=self.wordform_controller.nvn)
        nvn_syllables = ttk.Label(parent, textvariable=self.wordform_controller.nvn_syllables)
        generate = ttk.Button(parent, text="Generate", command=self.generate)
        nvn_play = ttk.Button(parent, text="Play", command=self.wordform_controller.pronounce)
        nvn.grid(sticky='ew', row=0, column=0, padx=PAD)
        nvn_syllables.grid(sticky='ew', row=1, column=0, padx=PAD)
        generate.grid(sticky='ew', row=0, column=1)
        nvn_play.grid(sticky='ew', row=1, column=1)

    def _setup_selector_ui(self, parent):
        """Initialize the generator selection view.
        
        Parameters:
            parent: The parent widget.
        """
        frame = ttk.Labelframe(parent, text='Generator')
        frame.grid(sticky='nsew')
        frame.columnconfigure(0, weight=2)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        self.generator_combobox = ttk.Combobox(frame, textvariable=self.var_generator, state="readonly",
            values=tuple(self.generators.keys()))
        self.var_generator.set(self.generator_combobox['values'][0])
        self.generator_combobox.grid(sticky='ew', row=0, columnspan=3)
        self.generator_combobox.bind("<<ComboboxSelected>>", lambda x: self.refresh())

        checkbox = ttk.Checkbutton(frame, text='Process', variable=self.var_limit_generator)
        checkbox.grid(sticky='ew', row=1, column=0)
        label = ttk.Label(frame, text="Syllables ")
        label.grid(sticky='nsw', column=1, row=1)
        syllable_count = ttk.Spinbox(frame, width=5, from_=1, to=10, textvariable=self.var_syllable_count)
        syllable_count.grid(sticky='nsew', column=2, row=1)

        button = ttk.Button(frame, text="New generator", command=self.new_generator)
        button.grid(sticky='ew', row=2, column=0)
        button = ttk.Button(frame, text="Save generators", command=self.save_generators)
        button.grid(sticky='ew', row=2, column=1, columnspan=2)

    def _setup_vowels_ui(self, parent):
        """Initialize the vowels weights view.
        
        Parameters:
            parent: The parent widget.
        """
        frame = ttk.Labelframe(parent, text='Vowels')
        frame.grid(sticky='nsew')
        frame.columnconfigure(1, weight=1, minsize=MINSIZE)

        for i, v in enumerate(VOWELS):
            var = self.var_vowels[v]
            label = ttk.Label(frame, text=v)
            label.grid(sticky='nsw', column=0, row=i, padx=PAD)
            scale = ttk.Scale(frame, orient=HORIZONTAL, from_=0, to=100, variable=var, command=self.update)
            scale.grid(sticky='nsew', column=1, row=i, padx=PAD)
            spinbox = ttk.Spinbox(frame, textvariable=var, command=self.update, width=5, from_=0, to=100)
            spinbox.grid(sticky='nse', column=2, row=i, padx=PAD)

    def _setup_consonants_ui(self, parent):
        """Initialize the consonant weights view.
        
        Parameters:
            parent: The parent widget.
        """
        frame = ttk.Labelframe(parent, text='Consonants')
        frame.grid(sticky='nsew')
        frame.columnconfigure(1, weight=1, minsize=MINSIZE)

        for i, c in enumerate(CONSONANTS):
            var = self.var_consonants[c]
            label = ttk.Label(frame, text=c)
            label.grid(sticky='nsw', column=0, row=i, padx=PAD)
            scale = ttk.Scale(frame, orient=HORIZONTAL, from_=0, to=100, variable=var, command=self.update)
            scale.grid(sticky='nsew', column=1, row=i, padx=PAD)
            spinbox = ttk.Spinbox(frame, textvariable=var, command=self.update, width=5, from_=0, to=100)
            spinbox.grid(sticky='nse', column=2, row=i, padx=PAD)

"""Wordform controller.

Handles the processes to go manipulate wordforms and the corresponding sounds.
"""
from tkinter import StringVar, Text, ttk
import typing as t
from model.nvn import ALPHABET, is_valid, syllabify

class WordformController:
    """Wordform controller class.

    Handles the processes to go manipulate wordforms and the corresponding sounds.
    """

    nvn: StringVar # str
    nvn_syllables: StringVar # t.List[str]

    def __init__(self, nvn: str = "", nvn_syllables: t.Iterable[str] = []):
        """Create a wordform controller.

        Handles the processes to go manipulate wordforms and the corresponding sounds.

        Parameters:
            nvn: The Novan wordform.
            nvn_syllables: The syllables corresponding to the Novan wordform.
        """
        self.nvn = StringVar(nvn)
        self.nvn_syllables = StringVar(tuple(syl for syl in nvn_syllables))
        self.nvn.trace("w", self.syllabify)

    def pronounce(self):
        """Plays audio corresponding to the syllables."""
        print(f"Pronouncing {self.nvn_syllables.get()}.")
        raise NotImplementedError

    def validate_entry(self, entry: ttk.Entry, nvn: t.Optional[str] = None):
        """Validate the content of a Tkinter entry.

        The return is meant to be bound to an entry event.

        Example:
            # Register the callback function
            reg = parent.register(lambda x: controller.validate_entry(entry, nvn))
            entry['validate'] = "key"
            entry['validatecommand'] = (reg, '%P')
        
        Parameters:
            entry: The entry to validate.
        
        Returns:
            `True` if the provided text is composed of Novan characters, `False` otherwise.
        """
        if nvn is None:
            nvn = self.nvn.get()

        is_alphabetic = all(c in ALPHABET for c in nvn)

        if not is_valid(nvn):
            entry_invalid_style = ttk.Style()
            entry_invalid_style.configure("BW.TEntry", foreground='red')
            entry.config(style="BW.TEntry")
        else:
            entry.config(style="")

        return is_alphabetic

    @DeprecationWarning
    def validate_text(self, text: Text, nvn: t.Optional[str] = None):
        """[Not tested] Validate the content of a Tkinter text field.

        The return is meant to be bound to an entry event.

        Example:
            # Register the callback function
            reg = parent.register(lambda x: controller.validate_entry(entry, nvn))
            entry['validate'] = "key"
            entry['validatecommand'] = (reg, '%P')
        
        Parameters:
            text: The text field to validate.
        
        Returns:
            `True` if the provided text is composed of Novan characters, `False` otherwise.
        """
        if nvn is None:
            nvn = self.nvn.get()
        
        is_alphabetic = all(c in ALPHABET for c in nvn)

        if not is_valid(nvn):
            text.config(foreground='red')
        else:
            text.config(foreground='')
        
        return is_alphabetic

    def syllabify(self, *args):
        """Fire when nvn gets updated."""
        nvn = self.nvn.get()
        if is_valid(nvn):
            self.nvn_syllables.set(tuple(syl for syl in syllabify(nvn)))

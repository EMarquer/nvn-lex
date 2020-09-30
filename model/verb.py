"""Verb entry."""
from .entry import AbstractEntry

class Verb(AbstractEntry):
    """Verb entry class."""
    
    is_generic: bool
    is_state: bool
    is_process: bool
    is_cognition: bool
    is_transfer: bool

    def __init__(self,
            is_generic: bool = False,
            is_state: bool = False,
            is_process: bool = False,
            is_cognition: bool = False,
            is_transfer: bool = False,
            **kwargs):
        """Construct a verb entry.

        Parameters:
            nvn: The Novan wordform of the entry.
            nvn_syllables: The syllables of the Novan wordform.
                Use in case the standard syllabification is invalid (not recommended).
            en: The English wordform of the entry.
            is_generic: `True` if the verb is a generic action verb, `False` otherwise.
            is_state: `True` if the verb is a state verb, `False` otherwise.
            is_process: `True` if the verb is a process verb, `False` otherwise.
            is_cognition: `True` if the verb is a cognition verb, `False` otherwise.
            is_transfer: `True` if the verb is a transfer verb, `False` otherwise.
            **kwargs: Other keyword arguments.
        """
        super().__init__(**kwargs)

        self.is_generic = is_generic
        self.is_state = is_state
        self.is_process = is_process
        self.is_cognition = is_cognition
        self.is_transfer = is_transfer

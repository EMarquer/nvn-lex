"""Generic lexical entry.

Handles URI, Novan wordform and syllables, and English wordform storage.
Handles calls to `nvn.syllabify` and `nvn.is_valid` when setting the Novan wordform.
"""
import typing as t
from .nvn import syllabify, is_valid
from abc import ABC

class AbstractEntry(ABC):
    """Abstract class for lexical entries.

    Handles URI, Novan wordform and syllables, and English wordform storage.
    Handles calls to `nvn.syllabify` and `nvn.is_valid` when setting the Novan wordform.
    """

    uri: str
    nvn: str
    nvn_syllables: t.List[str]
    en: str
    nvn_desc: str
    en_desc: str
    prime: str

    def __init__(self,
            nvn: str = "",
            nvn_syllables: t.List[str] = None,
            en: str = "",
            uri: str = "",
            nvn_desc: str = "",
            en_desc: str = "",
            prime: str = "",
            **kwargs):
        """Construct a lexical entry.

        Parameters:
            nvn: The Novan wordform of the entry.
            nvn_syllables: The syllables of the Novan wordform.
                Use in case the standard syllabification is invalid (not recommended).
            en: The English wordform of the entry.
            uri: The URI (Universal Ressource Identifier) of the entry.
            nvn_desc: The Novan description/definition of the entry.
            en_desc: The English description/definition of the entry.
            prime: The kind of semantic prime of the verb if the entry is a semantic prime, `` otherwise.
            **kwargs: Extra arguments (ignored).
        """
        self.uri = uri
        self.set_nvn(nvn)
        if nvn_syllables:
            self.nvn_syllables = nvn_syllables
        self.en = en
        self.nvn_desc = nvn_desc
        self.en_desc = en_desc
        self.prime = prime

    def set_nvn(self, nvn):
        """Set the Novan wordform of the entry.
        
        Parameters:
            nvn: the Novan wordform of the entry.
        
        Raises:
            ValueError: The provided `nvn` is not a valid wordform in Novan.
        """
        if is_valid(nvn):
            self.nvn = nvn
            self.nvn_syllables = syllabify(self.nvn)
        else:
            raise ValueError(f"Form '{nvn}' is invalid in Novan.")
        
    def set_nvn_desc(self, nvn):
        """Set the Novan description/definition of the entry.
        
        Parameters:
            nvn: the Novan description/definition of the entry.
        
        Raises:
            ValueError: The provided `nvn` is not a valid text in Novan.
        """
        if True:
            raise NotImplementedError
        else:
            raise ValueError(f"Form '{nvn}' is invalid in Novan.")

    def __hash__(self):
        """Generate a hash for the entry."""
        return hash(self.__dict__)

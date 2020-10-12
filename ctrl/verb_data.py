"""Verb data controller.

Controlls I/O of verb data between the model and the actual data.
"""

from tkinter import messagebox
import typing as t
from model import Verb
import pandas as pd
from ast import literal_eval

class VerbDataController:
    """Verb data controller class.

    Controlls I/O of verb data between the model and the actual data.
    """

    data_path: str
    verbs: t.List[Verb]
    #is_modified: bool

    def __init__(self, data_path: str = "data/verbs.csv"):
        """Create a verb data controller.

        Controlls I/O of verb data between the model and the actual data.

        Parameters:
            data_path: Path to the verb data CSV.
        """
        self.data_path = data_path
        self.verbs = []
        self.load()

    def save(self):
        """Save the verb data to the CSV file."""
        if messagebox.askokcancel(
                message=f'Are you sure you want to overwrite the data?',
                icon='warning', title='Save'):
            df = pd.DataFrame.from_records([v.__dict__ for v in self.verbs])
            df.to_csv(self.data_path)
        
    def load(self):
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

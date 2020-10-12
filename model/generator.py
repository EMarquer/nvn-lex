"""Package to generate Novan wordforms."""
from .nvn import CONSONANTS, VOWELS, ALPHABET, is_valid
import typing as t
import random
# import scipy.special.softmax as softmax

SYL = ['V', 'CV', 'VC', 'CVC']
SYLS = list(VOWELS)
SYLS += [c + v for c in CONSONANTS for v in VOWELS]
SYLS += [v + c for c in CONSONANTS for v in VOWELS]
SYLS += [c + v + cc for c in CONSONANTS for cc in CONSONANTS for v in VOWELS]
class Generator:
    """Generator class with a specific distribution of syllables."""

    weights: t.List[float]
    weight_map: t.Dict[str, float]

    def __init__(self, weight_map: t.Optional[t.Dict[str, float]] = None):
        """Create a generator with a specific distribution of syllables.
        
        Parameters:
            weight_map: If provided, this mapping from characters to probabilities are used to weight the syllables
                during generation.
        """
        if weight_map is None:
            self.weight_map = {char: 1 for char in ALPHABET}
        else:
            self.weight_map = weight_map
        self.update_weights()

    def generate(self, n: int = 1, forbidden: t.Iterable[str] = []) -> str:
        """Generate a Novan wordform.
        
        Parameters:
            n: The number of syllables.
            forbidden: An iterable of wordform to avoid.

        Returns:
            A randomely generated wordform.
        """
        wordform = ""
        while not is_valid(wordform) or wordform == "" or wordform in forbidden:
            wordform = "".join(random.choices(
                SYLS,
                self.weights, k=n))
        return wordform

    def update_weights(self):
        """Compute the weights of the syllables from the individual weights of the characters."""
        self.weights = []
        for syl in SYLS:
            self.weights.append(self.p(syl))

    def p(self, syl: str) -> float:
        """Compute the probability of a syllable to appear given the generator settings.
        
        Parameters:
            syl: The syllable to evaluate.
        
        Returns:
            The probability of the syllable.
        """
        prod = 1
        for char in syl:
            prod *= self.weight_map[char]
        return prod

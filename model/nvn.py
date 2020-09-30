"""Package with tools and constants to handle Novan wordforms."""
import typing as t

VOWELS = "ieaou"
BREATH_CONSONANT = "h"
CENTRAL_CONSONANTS = "ltpf"
THROAT_CONSONANTS = "kgx"
NOSE_CONSONANTS = "nm"
TONGUE_CONSONANTS = "zs"
CONSONANTS = BREATH_CONSONANT + CENTRAL_CONSONANTS + THROAT_CONSONANTS + NOSE_CONSONANTS + TONGUE_CONSONANTS
ALPHABET = CONSONANTS + VOWELS

SYLLABLES = list(VOWELS)
SYLLABLES += [c + v for c in CONSONANTS for v in VOWELS]
SYLLABLES += [v + c for c in CONSONANTS for v in VOWELS]
SYLLABLES += [c + v + cc for c in CONSONANTS for cc in CONSONANTS for v in VOWELS]

def are_compatible(a: str, b: str) -> bool:
    """Check if character `a` can be followed by character `b` in a single Novan wordform.

    Parameters:
        a: first letter to check, must precede `b`.
        b: second letter to check, must follow `a`.

    Returns:
        `True` if `a` can be followed by `b` in a single Novan wordform, `False` otherwise.
    """
    if a == BREATH_CONSONANT:
        return False

    # forbid duplicate letters
    if a == b:
        return False

    if ((a in THROAT_CONSONANTS and b in THROAT_CONSONANTS) or
            (a in NOSE_CONSONANTS and b in NOSE_CONSONANTS) or
            (a in TONGUE_CONSONANTS and b in TONGUE_CONSONANTS)):
        return False

    return True

def is_valid(nvn: str) -> bool:
    """Check if wordform is valid in Novan.
    
    Parameters:
        nvn: string of characters in Novan corresponding to a wordform.
    
    Returns:
        `True` if the input is a valid wordform in Novan, `False` otherwise.
    """
    # Forbid single consonants
    if len(nvn) == 1 and nvn in CONSONANTS:
        return False

    # Check if each pair of letters is valid
    pair_compatibility = all(are_compatible(nvn[i], nvn[i + 1]) for i in range(len(nvn) - 1))
    
    # Check if no more than 2 consonants follow each other
    no_consonant_chain = not any((nvn[i] in CONSONANTS and nvn[i + 1] in CONSONANTS and nvn[i + 2] in CONSONANTS)
        for i in range(len(nvn) - 2))

    # Check that there is no sequence of consonants at the begining or the end
    no_double_consonant = len(nvn) < 2 or not ((nvn[0] in CONSONANTS and nvn[1] in CONSONANTS) or
        (nvn[-2] in CONSONANTS and nvn[-1] in CONSONANTS))

    return pair_compatibility and no_consonant_chain and no_double_consonant

def cvify(nvn: str) -> str:
    """Compute the CV (consonant-vowel) form of a Novan wordform.
    
    Parameters:
        nvn: string of characters in Novan corresponding to a wordform.
    
    Returns:
        Return.
    """
    cv_labels = "".join(["V" if char in VOWELS else "C" for char in nvn])
    return cv_labels

def syllabify(nvn: str) -> t.List[str]:
    """Split a wordform into syllables using a recursive process.

    This functions prioritizes the onset over the coda.
    Typically, a `VCV` form will be split into `V-CV` rather than `VC-V`.

    Parameters:
        nvn: string of characters in Novan corresponding to a wordform.
    
    Returns:
        A list of syllables corresponding to the input.
    """
    cv = cvify(nvn)

    # ...C-C... or ...V-V...
    for i in range(len(nvn) - 1):
        if cv[i] == cv[i + 1]:
            return syllabify(nvn[:i + 1]) + syllabify(nvn[i + 1:])

    # ...V-CV...
    for i in range(len(nvn) - 2):
        if cv[i] == cv[i + 2] == "V" and cv[i + 1] == "C":
            return syllabify(nvn[:i + 1]) + syllabify(nvn[i + 1:])

    return [nvn]

import logging
import re
from time import time
from typing import Dict

from modules_api.postprocessing.termpostprocessor import TermPostProcessor

logger = logging.getLogger("Term Post Processing - Accent Removal")


class AccentRemovalPostProcessor(TermPostProcessor):
    def __init__(self, trigger_condition: str):
        super().__init__(trigger_condition)

    def __call__(self, terms, parameters: Dict[str, str] = None):
        return AccentRemovalPostProcessor.__remove_accents(terms)

    @staticmethod
    def __remove_tilds(s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b)
        return s

    @staticmethod
    def __remove_accents(terms):
        start_time = time()
        til = []
        list_accents = []
        for term in terms:
            accent = re.search("[áéíóúÁÉÍÓÚ]+", term)
            if accent is not None:
                sin = AccentRemovalPostProcessor.__remove_tilds(term)
                list_accents.append(term)
                til.append(sin)
            else:
                til.append(term)

        til2 = []
        delete = []
        for term in til:
            if term not in til2:
                til2.append(term)
            else:
                delete.append(term)

        indices = []
        delete2 = []
        for term in terms:
            if term in delete and term not in indices:
                indices.append(term)
                delete2.append(term)
        for term in delete2:
            ind = terms.index(term)
            terms.pop(ind)

        terms.sort()
        elapsed_time = time() - start_time

        return terms

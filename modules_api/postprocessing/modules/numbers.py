import logging
from time import time
from typing import Dict

from modules_api.configuration import PARAMS
from modules_api.postprocessing.termpostprocessor import TermPostProcessor

logger = logging.getLogger("Term Post Processing -- Number Removal")


class NumberRemovalPostProcessor(TermPostProcessor):
    def __init__(self, trigger_condition:str):
        super().__init__(trigger_condition)

    def __call__(self, terms, parameters: Dict[str, str] = None):
        return self.__delete_numbers(terms)

    def __delete_numbers(self, terms):
        start_time = time()
        file = open(PARAMS['es_numlist'], 'r', encoding='utf-8')
        read = file.readlines()
        cont = 0
        deletes = []
        for i in read:
            if (i[-1:] == '\n'):
                i = i[:-1]
                for j in terms:
                    if (' ' + i + ' ' in ' ' + j + ' '):
                        deletes.append(j)
                        ind = terms.index(j)
                        cont = cont + 1
                        terms.pop(ind)
        # list_.sort()
        elapsed_time = time() - start_time
        txt = 'NUMBERS, DELETE' + ' (' + str(cont) + ') NEW LIST SIZE: (' + str(len(terms)) + ') TIME: (' + str(
            elapsed_time) + ')'
        joind = ', '.join(deletes)
        # print('NUMEROS DELETE', cont, len(terms), elapsed_time)
        logger.debug(txt, 'TERMS REMOVED: ' + joind)
        return (terms)

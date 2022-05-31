import logging
from abc import abstractmethod, ABC
from time import time
from typing import List, Dict

from nltk.corpus import stopwords
from pycond import parse_cond

from modules_api import configuration

LANG_MAP = {'en': 'english', 'es': 'spanish'}

logger  = logging.getLogger("Term Post Processing")

class TermPostProcessor(ABC):
    def __init__(self, trigger_condition: str):
        self._condition_string = trigger_condition
        self._condition = parse_cond(trigger_condition)[0]

    @abstractmethod
    def __call__(self, terms, parameters: Dict[str, str] = None):
        pass


def _clean_terms(termlist, lang_in):
    start_time = time()
    stop = []
    with open(configuration.PARAMS[f'{lang_in}_stopwords'], 'r', encoding='utf-8') as swfp:
        stop = stopwords.words(LANG_MAP[lang_in])
        stop.extend(swfp.readlines())

    clean_list = []
    to_remove = []
    for term in termlist:
        term = term.strip(',.:')
        if (term.lower() in stop) or (term in stop):
            to_remove.append(term)
        elif (term.lower() not in stop) or (term not in stop):
            clean_list.append(term.replace(',', '').replace('-', ''))

    cont = len(termlist) - len(clean_list)
    elapsed_time = time() - start_time

    txt = f'CLEAN_TERMS, DELETE ( {str(cont)}) NEW LIST SIZE: ({str(len(clean_list))}) TIME: ({str(elapsed_time)})'
    joind = ', '.join(to_remove)
    # conts_log.information(txt, 'TERMS REMOVED: ' + joind)
    logger.debug(txt)

    return clean_list


class TermPostProcessorRegistry(TermPostProcessor):
    def __init__(self):
        super().__init__("")
        self.registry = []  # type: List[TermPostProcessor]

    def register(self, post_processors=List[TermPostProcessor]):
        self.registry.extend(post_processors)

    def __call__(self, terms, parameters: Dict[str, str] = None):
        processed_terms = _clean_terms(terms, parameters['source_language'])
        for processor in self.registry:
            logger.debug(f"Checking {processor._condition_string} against {parameters}")
            if processor._condition(state=parameters):
                logger.debug("Triggering processor" + str(processor))
                processed_terms = processor(processed_terms, parameters)
        processed_terms = _clean_terms(processed_terms, parameters['source_language'])
        return processed_terms

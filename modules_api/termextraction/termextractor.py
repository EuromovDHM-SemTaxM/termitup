import logging
from abc import ABC, abstractmethod
from typing import Dict, List

from pycond import parse_cond

logger = logging.getLogger("Term Extraction")


class TermExtractor(ABC):
    def __init__(self, trigger_condition: str):
        self._condition_string = trigger_condition
        self._condition = parse_cond(trigger_condition)[0]

    @abstractmethod
    def __call__(self, corpus: str, parameters: Dict[str, str] = None):
        pass


class TermExtractorRegistry(TermExtractor):
    def __init__(self):
        super().__init__("")
        self.registry = []  # type: List[TermExtractor]

    def register(self, extractors=List[TermExtractor]):
        self.registry.extend(extractors)

    def __call__(self, corpus, parameters: Dict[str, str] = None):
        result = []
        for extractor in self.registry:
            logger.debug(f"Checking {extractor._condition_string} against {parameters}")
            if extractor._condition(state=parameters):
                logger.debug("Triggering processor" + str(extractor))
                result = extractor(corpus, parameters)
                break
        return result

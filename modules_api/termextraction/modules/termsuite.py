from typing import Dict

import requests

from modules_api.configuration import PARAMS
from modules_api.termextraction.termextractor import TermExtractor


class TermsuiteTermExtractor(TermExtractor):
    def __init__(self, trigger_condition:str ):
        super().__init__(trigger_condition)

    def __call__(self, corpus: str, parameters: Dict[str, str] = None):
        result = requests.post(f"{PARAMS['termsuite_endpoint']}?language={parameters['source_language']}", data=corpus,
                               headers={'Accept': 'application/json', 'Content-Type': 'plain/text'}).json()

        words = {word['lemma'] for word in result['words']}

        return list(words)

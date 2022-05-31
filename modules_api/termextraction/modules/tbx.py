import re
from tempfile import gettempdir
from typing import Dict

import uuid

from modules_api.configuration import PARAMS
from modules_api.termextraction.TBXTools import TBXTools
from modules_api.termextraction.termextractor import TermExtractor


class TBXTermExtractor(TermExtractor):

    def __init__(self, trigger_condition: str):
        super().__init__(trigger_condition)

    def __call__(self, corpus: str, parameters: Dict[str, str] = None):
        lang_in = parameters['source_language']

        sw_spanish = PARAMS["es_stopwords"]
        sw_english = PARAMS["en_stopwords"]

        inner_spanish = PARAMS["es_innerstop"]
        inner_english = PARAMS["en_innerstop"]
        if lang_in == "es":
            lang = lang_in + "p"
        elif lang_in == "en":
            lang = lang_in + "g"
        # print(lang)
        extractor = TBXTools()

        temp_dir = gettempdir()
        random_id = str(uuid.uuid4())
        # db_file_name = random_id + "_statistical8.sqlite"

        extractor.create_project(":memory:", lang, overwrite=True)
        extractor.load_sl_corpus_s(corpus)
        extractor.ngram_calculation(nmin=1, nmax=3, minfreq=3)
        if lang == "esp":
            extractor.load_sl_stopwords(sw_spanish)
            extractor.load_sl_inner_stopwords(inner_spanish)
        elif lang == "eng":
            extractor.load_sl_stopwords(sw_english)
            extractor.load_sl_inner_stopwords(inner_english)

        extractor.statistical_term_extraction(minfreq=4)
        # aquí junta los términos que son iguales pero están en mayus y en minus
        extractor.case_normalization(verbose=True)
        # esto no sé muy bien lo que hace pero saca menos términos que si no se pone, lo cual es mejor, creo que quita basurilla
        extractor.nest_normalization(verbose=True)
        extractor.regexp_exclusion(verbose=True)
        extractor.load_sl_exclusion_regexps(PARAMS['exclusion_regexps'])
        extractor.regexp_exclusion(verbose=True)
        # para extraer unigramas, descomenta esto
        # extractor.select_unigrams("unigrams.txt",position=-1)
        out = extractor.save_term_candidates(f"{temp_dir}/{random_id}_terms.txt")
        new_output = []
        chars = ['\'', '\"', '!', '<', '>', ',', '.', ':']
        for i in out:
            t = i.replace("\t", ",")
            s = re.sub("\d+", "", t)
            # print(s)
            for c in chars:
                if c in s:
                    term = s.replace(c, '')
                    term = term.strip(",;:. ")
                    # print(term)
                    new_output.append(term)
                    new_output = list(dict.fromkeys(new_output))
        return new_output

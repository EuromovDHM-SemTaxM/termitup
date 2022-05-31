from time import time
from typing import Dict

import requests

from modules_api import conts_log
from modules_api.configuration import PARAMS
from modules_api.postprocessing.termpostprocessor import TermPostProcessor


class TimeExPostProcessor(TermPostProcessor):
    def __init__(self, trigger_condition:str):
        super().__init__(trigger_condition=trigger_condition)

    def __call__(self, terms, parameters: Dict[str, str] = None):
        terms = '| '.join(terms).replace('-', '').replace(',', '').replace(';', '')
        terms = TimeExPostProcessor.__annotate_timex(terms, parameters['source_language'])
        terms.sort()
        return terms

    @staticmethod
    def __annotate_timex(text, lang, domain="legal"):

        f = open('texto.txt', 'w')
        f.write(text)
        start_time = time()

        url = PARAMS['timex_annotador_endpoint']
        params = {
            'inputText': text,
            'inputDate': '',
            'domain': domain,
            'lan': lang,
            'format': 'timex3'
        }
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        # response=requests.post(url, data=params)
        response = requests.request("POST", url, headers=headers, json=params)
        textanotador = response.text
        print('ENTRA ANOTADOR')
        print(textanotador)

        code = response.status_code
        annotations = textanotador.split('|')
        print(annotations)

        deletes = []
        cont = 0
        for annotation in annotations:
            if '<' in annotation and len(annotation) > 2:
                cont = cont + 1
                deletes.append(annotation)
                ind = annotations.index(annotation)
                annotations.pop(ind)
        for annotation in annotations:
            if '<' in annotation and len(annotation) > 2:
                print(annotation)
                cont = cont + 1
                deletes.append(annotation)
                ind = annotations.index(annotation)
                annotations.pop(ind)

        anotador = []
        for annotation in annotations:
            anotador.append(annotation.strip().replace(',', ''))

        if code != 200:
            print('WARNING: Annotador is down. Temporal expressions could not be removed.')
            anotador = text.split('| ')
            conts_log.error('Annotador is down. Temporal expressions could not be removed.', code)
        else:
            elapsed_time = time() - start_time
            txt = 'AÑOTADOR, DELETE (' + str(cont) + ') NEW LIST SIZE: (' + str(len(anotador)) + ') TIME: (' + str(
                elapsed_time) + ')'
            joind = ', '.join(deletes)
            print('AÑOTADOR DELETE', cont, len(anotador), elapsed_time)
            conts_log.information(txt, 'TERMS REMOVED: ' + joind)

        return anotador

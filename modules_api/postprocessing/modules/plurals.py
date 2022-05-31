from time import time
from typing import Dict

from modules_api import conts_log
from modules_api.configuration import PARAMS
from modules_api.postprocessing.termpostprocessor import TermPostProcessor


class PluralPostProcessor(TermPostProcessor):
    def __init__(self, trigger_condition:str):
        super().__init__(trigger_condition)

    def __call__(self, terms, parameters: Dict[str, str] = None):
        return self.__remove_plurals(terms)

    def __remove_plurals(self, valuelist):
        start_time = time()
        file = open(PARAMS['es_numlist'], 'r', encoding='utf-8')
        read = file.readlines()
        plural = []
        cont = 0
        for i in valuelist:
            ind = valuelist.index(i)
            term = i.replace(',', '').replace('-', ' ')
            valuelist[ind] = term
            plu = ''
            if ('es' in term[-2:] or 's' in term[-1:]):
                slp = term.split(' ')

                for n in read:
                    if (n[:-1] in slp):
                        plu = i

                if not len(plu):
                    for j in slp:
                        if (('es' in j[-2:]) and 't' not in j[-3:-2] and 'l' not in j[-3:-2] or ('les' in j[-3:])):
                            plu += ' ' + j[:-2]

                            if ('on' in plu[-2:]):
                                plu = ' ' + plu[:-2] + 'ón'
                            if ('v' in plu[-1:]):
                                plu = ' ' + plu + 'e'
                            if ('bl' in plu[-2:]):
                                plu = ' ' + plu + 'e'
                            if ('br' in plu[-2:]):
                                plu = ' ' + plu + 'e'

                        elif (('s' in j[-1:])):
                            plu += ' ' + j[:-1]
                            pos = slp.index(j)

                            if (pos > 0):
                                bef = slp[0]
                                if ('n' in bef[-1:] and 'ón' not in bef[-2:]):

                                    splb = plu.split(' ')

                                    firts = splb[1]

                                    if ('n' not in firts[-1:]):
                                        pass
                                    else:
                                        plu0 = firts[:-1]
                                        join1 = ' '.join(splb[2:])

                                        plu = plu0 + ' ' + join1



                        else:
                            plu += ' ' + j

                ind = valuelist.index(term)
                valuelist[ind] = plu.strip()
                cont = cont + 1
        quit_plu = []
        nuevalista = set(valuelist)
        for i in nuevalista:
            quit_plu.append(i)

        deletes = []
        new = []
        for i in valuelist:
            if i not in new:
                new.append(i)
            else:
                deletes.append(i)
        # print('plurañes eliminadas ->', deletes)
        elapsed_time = time() - start_time
        txt = 'PLURAL, DELETE' + ' (' + str(len(valuelist) - len(quit_plu)) + ') NEW LIST SIZE: (' + str(
            len(quit_plu)) + ') TIME: (' + str(elapsed_time) + ')'
        joind = ', '.join(deletes)
        print('PLURALES DELETE', len(valuelist) - len(quit_plu), len(quit_plu), elapsed_time)
        conts_log.information(txt, 'TERMS REMOVED: ' + joind)
        return (quit_plu)

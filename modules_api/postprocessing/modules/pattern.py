import logging
from time import time
from typing import Dict

import spacy
import stanza

from modules_api.postprocessing.termpostprocessor import TermPostProcessor

logger = logging.getLogger("Term Post Processing -- Pattern Filter")


class PatternCleaningProcessor(TermPostProcessor):

    def __init__(self, trigger_condition: str):
        super().__init__(trigger_condition)
        stanza.download('es')
        stanza.download('en')
        self.__taggers = {
            'en': stanza.Pipeline('es'),
            'es': stanza.Pipeline('en')
        }

        self.__nlp_pipeline = {
            'en': spacy.load('en_core_web_sm'),
            'es': spacy.load('es_core_news_sm')
        }

    def __call__(self, terms, parameters: Dict[str, str] = None):
        terms = PatternCleaningProcessor.__delete_pattern(terms, self.__taggers[parameters['lang_in']],
                                                          self.__nlp_pipeline['lang_in'])
        return terms

    # 2.1 patrones es
    @staticmethod
    def __delete_pattern(annotations, pos_tagger, nlp):
        total = 0
        deletes = []
        start_time = time()
        lemmas_list = []
        cont = 0
        cont_inf = 0
        cont_post = 0
        for annotation in annotations:
            logger.debug(annotation)
            if (len(annotation) > 1):
                # print( i, i.split(' ') )
                # pos_tagger = CoreNLPParser('https://corenlp.run/', tagtype='pos')
                # si se cae el de lynx, probar con este https://corenlp.run/
                # print(i)
                doc = pos_tagger(annotation)
                # print(doc)
                sent = doc.sentences[0]
                word = sent.words
                tag = []
                for token in word:
                    pos = token.upos
                    term = token.text
                    tupla = (term, pos)
                    tag.append(tupla)
                    logger.debug(token.text)
                    logger.debug(pos)
                # tag=pos_tagger.tag(i.split(' '))
                logger.debug(tag)
                total = total + 1
                joini = annotation
                list_pos = []
                spl = joini.split(' ')
                if (joini != ''):
                    join_tag = ''
                    for t in tag:

                        print(t)
                        if t[1] == 'AUX':
                            doc = nlp(t[0])
                            lemlist = [tok.lemma_ for tok in doc]
                            lem = ''.join(lemlist)
                            lemmas_list.append(lem)
                            if (lem == annotation):
                                lem = t[0]
                            list_pos.append('aux--' + str(lem))
                            if (len(spl) == 1):
                                ind = annotations.index(str(annotation))
                                annotations[ind] = str(lem)
                        if (t[1] == 'NOUN'):
                            list_pos.append('noun-' + str(t[0]))
                        if (t[1] == 'VERB'):
                            cont_inf = cont_inf + 1
                            doc = nlp(t[0])
                            for tok in doc:
                                l = tok.lemma_
                                if (l != t[0]):
                                    cont_post = cont_post + 1
                            lemlist = [tok.lemma_ for tok in doc]
                            lem = ''.join(lemlist)
                            lemmas_list.append(lem)
                            if lem == annotation:
                                lem = t[0]
                            list_pos.append('verb-' + str(lem))
                            if len(spl) == 1:
                                ind = annotations.index(str(annotation))
                                annotations[ind] = str(lem)
                        if (t[1] == 'ADV'):
                            list_pos.append('adv--' + str(t[0]))
                        if (t[1] == 'ADJ'):
                            list_pos.append('adj--' + str(t[0]))
                        if (t[1] == 'SCONJ'):
                            list_pos.append('sconj' + str(t[0]))

                    spl_i = joini.split(' ')

                    if (len(list_pos) == 1):
                        pos1 = list_pos[0]
                        if (pos1[0:4] == 'adv-'):
                            term = pos1[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1

                    elif (len(list_pos) == 2 and len(spl_i) == 2):
                        pos1 = list_pos[0]
                        pos2 = list_pos[1]
                        term = ''
                        if (pos1[0:4] == 'aux-' and pos2[0:4] == 'verb'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'aux-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'verb'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'verb'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'aux-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adv-' and pos2[0:4] == 'adj-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adj-' and pos2[0:4] == 'adv-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adv-' and pos2[0:4] == 'aux-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'aux-' and pos2[0:4] == 'adv-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adv-' and pos2[0:4] == 'verb'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'aux-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'adv-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adv-' and pos2[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'adv-'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'aux-' and pos2[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adj-' and pos2[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1

                    elif (len(list_pos) == 3 and len(spl_i) == 3):
                        # print(list_pos, spl_i,'-', len(list_pos), len(spl_i))
                        pos1 = list_pos[0]
                        pos2 = list_pos[1]
                        pos3 = list_pos[2]
                        term = ''
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'verb' and pos3[0:4] == 'verb'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'aux-' and pos3[0:4] == 'verb'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'aux-' and pos3[0:4] == 'aux-'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'verb' and pos3[0:4] == 'aux-'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1

                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'verb' and pos3[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'aux-' and pos3[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'noun' and pos3[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'noun' and pos3[0:4] == 'verb'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'aux-' and pos2[0:4] == 'noun' and pos3[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'noun' and pos3[0:4] == 'aux-'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'aux-' and pos2[0:4] == 'verb' and pos3[0:4] == 'noun'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'verb' and pos3[0:4] == 'adj-'):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'verb' and pos3[
                                                                            0:4] == 'noun' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'noun' and pos3[
                                                                            0:4] == 'adj-' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'aux-' and pos3[
                                                                            0:4] == 'adj-' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'adv-' and pos3[
                                                                            0:4] == 'adj-' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adj-' and pos2[0:4] == 'adv-' and pos3[
                                                                            0:4] == 'adj-' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'noun' and pos2[0:4] == 'adv-' and pos3[
                                                                            0:4] == 'scon' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adj-' and pos2[0:4] == 'scon' and pos3[
                                                                            0:4] == 'adv-' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'aux-' and pos2[0:4] == 'noun' and pos3[
                                                                            0:4] == 'adj-' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'verb' and pos2[0:4] == 'verb' and pos3[
                                                                            0:4] == 'verb' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1
                        if (pos1[0:4] == 'adj-' and pos2[0:4] == 'noun' and pos3[
                                                                            0:4] == 'adj-' and joini in annotations):
                            term = pos1[5:] + ' ' + pos2[5:] + ' ' + pos3[5:]
                            deletes.append(joini)
                            ind = annotations.index(joini)
                            # anotador.pop(ind)
                            cont = cont + 1

        for annotation in deletes:
            if (annotation in annotations):
                ind = annotations.index(annotation)
                annotations.pop(ind)

        elapsed_time = time() - start_time
        txt = 'PATRONES, DELETE' + ' (' + str(cont) + ') NEW LIST SIZE: (' + str(len(annotations)) + ') TIME: (' + str(
            elapsed_time) + ')'
        joind = ', '.join(deletes)
        # logger.debug('PATRONES DELETE', cont, len(annotations), elapsed_time)
        logger.debug(txt, 'TERMS REMOVED: ' + joind)
        return (annotations)

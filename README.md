# TermitUp


TermitUp is a tool for terminology enrichment: given a domain specific corpus, TermitUp performs statistical terminology extraction and post-process the resulting term list with a series of liguistic processes and external tools such as the Añotador (https://annotador.oeg.fi.upm.es/), to clean temporal expressions. Then, it queries several language resources (some part of the Linguistic Linked Open Data cloud) for candidate terms matching those in the term list. 

TermitUp builds sense indicators for both the source and the candidate terms, and performs a Word Sense Disambiguation process (with Semantic Web Company's service), matching those concepts with the closest domain. From the concepts matched in the external resources, TermitUp retrieves every piece of information available (translations, synonyms, definitions, usage notes and terminological relations), already disambiguated, and enriches the source term lists, creating links amongst the resources in the LLOD. 

See TermitUp Architecture: 

<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/termitup_architecture.png" width="70%" />


Afterwards, TermitUp offers the possibility of creating hierarchical relations amongst the terms in the source list and also of validating the synonymy relations retrieved from the external resources, by applying linguistic patterns and additional language resources. Finally, the results are published in separate json-ld files, modeled in SKOS and Ontolex (users' choice). Finally, TermitUp API publishes the enriched terminologies generated in a Virtuoso Enpoint, where the can be freely queried.

Examples of the SKOS and Ontolex models followed are shown below: 

<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/skos_model.png" width="30%" />
<img src="https://github.com/Pret-a-LLOD/termitup/blob/master/static/images/ontolex_model.png" width="40%" />


These models, however, are not able to model certain pieces of data that are very relevant when building enriched terminologies from heterogeneous data sources. Those limitations are discussed in the Wiki of the W3C Ontology-Lexicon Community Group, as a proposal for good practives to model enriched terminologies: https://www.w3.org/community/ontolex/wiki/Terminology


Visit TermitUp home: https://termitup.oeg.fi.upm.es/
Try TermitUp API: https://termitup.oeg.fi.upm.es/swagger/
Access TerrmitUp SPARQL Endpoint: https://termitup.oeg.fi.upm.es/sparql

Feedback is very welcome!




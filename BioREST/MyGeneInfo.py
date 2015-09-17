# coding=utf-8
"""
http://docs.mygene.info/en/latest/index.html
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import logging
from BioREST.Service import REST, list2string, check_param_in_list

log = logging.getLogger(__name__)

class MyGeneInfo(REST):

    _url = "http://mygene.info/v2"

    def __init__(self):
        super(BioCyc, self).__init__(name="MyGeneInfo", url=MyGeneInfo._url)

    __valid_fields = ['entrezgene', 'ensemblgene', 'symbol', 'name', 'alias', 'summary', 'refseq', 'unigene',
    'homologene', 'accession', 'ensembltranscript', 'ensemblprotein', 'uniprot', 'pdb', 'prosite', 'pfam', 'interpro',
    'mim', 'pharmgkb', 'reporter', 'reagent', 'go', 'hgnc', 'hrpd', 'mgi', 'rgb', 'flybase', 'wormbase', 'zfin', 'tair',
    'xenbase', 'mirbase', 'retired']

    def GeneQuery(self, query, fields, species, size, from, sort, facets, species_facet_filter, entrezonly, ensemblonly,
                  callback, dotfield, filter, limit, skip, email):
        """
        http://docs.mygene.info/en/latest/doc/query_service.html
        """
        url = 'query'
        raise NotImplementedError

    def __add_fielded_queries(self, field, param):
        """
        """
        if check_param_in_list(field, self.__valid_fields, name=None):
            return str(field)+":"+str(param)
        else:
            raise ValueError("")

    def GeneAnnotation(self):
        """
        http://docs.mygene.info/en/latest/doc/annotation_service.html
        """
        raise NotImplementedError

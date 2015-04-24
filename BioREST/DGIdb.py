# coding=utf-8
"""
DGIdb, mining the druggable
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import logging
from BioREST.Service import REST, list2string
log = logging.getLogger(__name__)


class DGIdb(REST):
    """
    Interface to the DGIdb  : http://dgidb.genome.wustl.edu/api

    """

    _url = 'http://dgidb.genome.wustl.edu'

    def __init__(self):
        """
        **Constructor** DGIdb
        """
        super(DGIdb, self).__init__(name="DGIdb", url=DGIdb._url)

    def Search_Interactions(self, genes, interaction_sources=None, interaction_types=None, drug_types=None,
                            gene_categories=None, source_trust_levels=None):
        """
        The interactions endpoint can be used to return interactions for a given set of gene names or symbols. It also
        allows you to filter returned interactions.
        :return:
        """
        query = 'api/v1/interactions.json'
        params = {'genes': list2string(genes, space=False)}

        if interaction_sources is not None:
            params['interaction_sources'] = str(interaction_sources)

        if interaction_types is not None:
            params['interaction_types'] = str(interaction_types)

        if drug_types is not None:
            params['drug_types'] = str(drug_types)

        if gene_categories is not None:
            params['gene_categories'] = str(gene_categories)

        if source_trust_levels is not None:
            params['source_trust_levels'] = str(source_trust_levels)

        res = self.http_get(query=query, params=params)
        return res

    def Interaction_Type(self):
        """
        The interaction types endpoint can be used to retrieve a current list of supported interaction types for use
        in the interactions endpoint.
        :return:
        """
        query = 'api/v1/interaction_types.json'
        res = self.http_get(query=query)
        return res

    def Interaction_Source(self):
        """
        The interaction sources endpoint can be used to retrieve a current list of supported interaction sources for
        use in calls to the interactions endpoint.
        :return:
        """
        query = 'api/v1/interaction_sources.json'
        res = self.http_get(query=query)
        return res

    def Drug_Types(self):
        """
        The drug types endpoint can be used to retrieve a current list of supported drug types for use in calls to the
        interactions endpoint.
        :return:
        """
        query = 'api/v1/drug_types.json'
        res = self.http_get(query=query)
        return res

    def Gene_Categories(self):
        """
        The gene categories endpoint can be used to retrieve a current list of supported gene categories for use in
        calls to the interactions endpoint.
        :return:
        """
        query = 'api/v1/gene_categories.json'
        res = self.http_get(query=query)
        return res

    def Source_Trust_Levels(self):
        """
        The source trust levels endpoint can be used to retrieve a current list of supported source trust levels for
        use in calls to the interactions endpoint.
        :return:
        """
        query = 'api/v1/source_trust_levels.json'
        res = self.http_get(query=query)
        return res

    def Related_Genes(self, genes):
        """
        The related genes endpoint can be used to return Entrez gene symbols for other genes that are known to interact
        in pathways with your gene list
        :return:
        """
        query = 'api/v1/related_genes.json'
        params = {'genes': list2string(genes, space=False)}
        res = self.http_get(query=query, params=params)
        return res

    def Genes_in_Category(self, category):
        """
        The Genes in Category endpoint can be used to get a list of all genes in DGIdb that are known to be in a
        specific category.
        :return:
        """
        query = 'api/v1/interaction_types.json'
        params = {'category': str(category)}
        res = self.http_get(query=query, params=params)
        return res

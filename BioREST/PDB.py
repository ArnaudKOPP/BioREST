# coding=utf-8
"""
http://www.rcsb.org/pdb/software/rest.do
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import logging
from BioREST.Service import REST, check_range, check_param_in_list

log = logging.getLogger(__name__)


class PDB(REST):
    def __init__(self):
        super(PDB, self).__init__(name="PDB", url="http://www.rcsb.org/pdb/rest/")

    def describe_pdb(self, id):
        url = 'describePDB?structureId='
        url += str(id)
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def status_pdb(self, id):
        url = 'idStatus?structureId='
        url += str(id)
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def describe_pdb_entity(self, id):
        url = 'describeMol?structureId='
        url += str(id)
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def describe_chemical_comp(self, id):
        url = 'describeHet?chemicalID='
        url += str(id)
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def get_current_PDB_ids(self):
        url = 'getCurrent'
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def get_obsolete_PDB_ids(self):
        url = 'getObsolete'
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def get_unreleased(self, id=None):
        url = 'getUnreleased'
        if id is not None:
            url += '?structureId='+str(id)
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def get_ligand(self, id):
        url = 'ligandInfo?structureId='
        url += str(id)
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def get_gene_ontology(self, id):
        url = 'goTerms?structureId='
        url += str(id)
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def get_pfam_annot(self, id=None, tab_frmt=False):
        url = 'hmmer'
        if id is not None:
            url += '?structureId='+str(id)
        if tab_frmt:
            if id is None:
                url += '?file=hmmer_pdb_all.txt'
        res = self.http_get(query=url, frmt='xml')
        res = self.easyXML(res)
        return res

    def smiles_query(self, query, search_type='exact', similarity=None):
        __valid_search_type = ['exact', 'substructure', 'superstructure', 'similarity']
        check_param_in_list(search_type, __valid_search_type)
        params = {'smiles': query, 'seach_type' : search_type}
        if similarity is not None:
            check_range(similarity, 0, 1)
            params['similarity'] = similarity
        url = 'smilesQuery'
        res = self.http_get(query=url, frmt='xml', params=params)
        res = self.easyXML(res)
        return res

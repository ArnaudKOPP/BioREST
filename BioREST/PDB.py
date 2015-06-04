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
from BioREST.Service import REST

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

    def describe_pdb_entity(self):
        raise NotImplementedError

    def describe_chemical_comp(self):
        raise NotImplementedError

    def get_ligand(self):
        raise NotImplementedError

    def release_status(self):
        raise NotImplementedError

    def get_released_pdb(self):
        raise NotImplementedError

    def get_unreased_pdb(self):
        raise NotImplementedError

    def get_pre_released_sequence(self):
        raise NotImplementedError

    def get_pdb_chains_anno(self):
        raise NotImplementedError

    def get_uniprot_mapping(self):
        raise NotImplementedError

    def get_pfam_mapping(self):
        raise NotImplementedError

    def get_onto_terms(self):
        raise NotImplementedError

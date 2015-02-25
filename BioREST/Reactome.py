# coding=utf-8
"""
Reactome interface using REST
REACTOME is an open-source, open access, manually curated and peer-reviewed
pathway database. Pathway annotations are authored by expert biologists, in
collaboration with Reactome editorial staff and cross-referenced to many
bioinformatics databases. These include NCBI Entrez Gene, Ensembl and UniProt
databases, the UCSC and HapMap Genome Browsers, the KEGG Compound and ChEBI
small molecule databases, PubMed, and Gene Ontology

URL: http://www.reactome.org/ReactomeGWT/entrypoint.html
REST: http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/ReactomeRESTFulAPI.html

    # from BioREST import Reactome, ReactomeAnalysis
    # r = Reactome()
    # print(r.front_page_items("homo sapiens"))
    # print(r.get_list_pathways())
    # print(r.get_species())
    # print(r.biopax_exporter(109581))
    # res = r.highlight_pathway_diagram("68875", genes="CDC2", frmt='PDF')
    # f = open("reactome.pdf", "w")
    # f.write(res)
    # f.close()
    # res = r.list_by_query("Pathway", name='Apoptosis')
    # identifiers = [x['dbId'] for x in res]
    # print(identifiers)
    # print(r.pathway_hierarchy("homo sapiens"))
    # print(r.pathway_participantes(109581))
    # print(r.pathway_complexes(109581))
    # print(r.query_by_id("Pathway", "109581"))
    # print(r.query_by_ids("Pathway", "CDC2"))
    # print(r.query_pathway_for_entities(170075))
    # print(r.query_hit_pathways('CDC2'))
    # print(r.query_hit_pathways(['CDC2']))
    # print(r.species_list())
    # print(r.SBML_exporter(109581))
    # ra = ReactomeAnalysis()
    # res = ra.identifiers('TP53')
    # import json
    # print(json.dumps(res, indent=4, separators=(',', ': ')))

    # res = ra.identifier(170075)
    # import json
    # print(json.dumps(res, indent=4, separators=(',', ': ')))

    # res = ra.species(48895)
    # import json
    # print(json.dumps(res, indent=4, separators=(',', ': ')))

"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import logging
from BioREST.Service import REST, list2string, check_param_in_list

log = logging.getLogger(__name__)


class Reactome(REST):
    """
    Reactome interface
    """

    _url = "http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/RESTfulWS"

    def __init__(self):
        super(Reactome, self).__init__("Reactome", url=Reactome._url)
        # buffer
        self._list_pathways = None

    def _download_list_pathways(self):
        if self._list_pathways is None:
            res = self.session.get("http://www.reactome.org/download/current/ReactomePathways.txt")
            if res.status_code == 200:
                res = res.text
                res = res.strip()
                self._list_pathways = [x.split("\t") for x in res.split("\n")]
            else:
                log.error("Could not fetch the pathways")
                raise IOError
        return self._list_pathways

    def get_list_pathways(self):
        """
        Return list of pathways from reactome website
        """
        res = self._download_list_pathways()
        return res

    def get_species(self):
        """
        Return list of species from all pathways
        """
        self._download_list_pathways()
        res = set([x[2] for x in self.get_list_pathways()])
        return res

    def biopax_exporter(self, identifier, level=2):
        """
        Get BioPAX file
        The passed identifier has to be a valid evend identifier. If there is no matching ID in the database,it will
        return an empty string

        s = Reactome()
        res = s.biopax_exporter(109581)
        :param level: BioPAX level 2 or 3
        :param identifier: Event database identifier
        """
        res = self.http_get("biopaxExporter/Level{0}/{1}".format(level, identifier), frmt=None)
        return res

    def front_page_items(self, species):
        """
        Get list of front page items listed in the Reactome Pathways Browser

        s = Reactome()
        res = s.front_page_items("homo sapiens")

        :param species: full species name
        Pathway Browser <http://www.reactome.org/PathwayBrowser/>
        """
        species = species.replace(" ", "+")
        res = self.http_get("frontPageItems/{0}".format(species))
        return res

    def highlight_pathway_diagram(self, identifier, genes, frmt="PDF"):
        """
        Highlight a diagram for a specified pathways based on its identifier.This method should be used after method
        queryHitPathways
        :param frmt: pdf or png
        :param genes: gene symbol delimited by comma(no space)
        :param identifier: pathway databse identifier
        """
        check_param_in_list(frmt, ['PDF', 'PNG'])
        url = "highlightPathwayDiagram/{0}/{1}"
        genes = list2string(genes, space=False)
        res = self.http_post(url.format(identifier, frmt), frmt="txt", data=genes)
        return res

    def list_by_query(self, classname, **kargs):
        """
        Get list of objects from Reactome database
        To query a list of pathways with names as 'Apoptosis'

        s = Reactome()
        res = list_by_query("Pathway", name='Apoptosis')
        identifiers = [x['dbId'] for x in res]
        :param kargs: key, value
        :param classname: class name
        """
        url = "listByQuery/{0}".format(classname)
        # NOTE: without the content-type this request fails with error 415
        # fixed by
        res = self.http_post(url, frmt='json', data=kargs, headers={'Content-Type': "application/json;odata=verbose"})
        return res

    def pathway_diagram(self, identifier, frmt="PNG"):
        """
        Retrieve pathway diagram

        s = Reactome()
        s.pathway_diagram('109581', 'PNG', view=True)
        s.pathway_diagram('109584', 'PNG', save=True)

        if PNG or PDF, the output is base64 but there is no facility to easily save the results in a file for now
        :param frmt: pdf, png or xml
        :param identifier: pthway database identifier
        """
        check_param_in_list(frmt, ['PDF', 'PNG', 'XML'])
        url = 'pathwayDiagram/{0}/{1}'.format(identifier, frmt)
        res = self.http_get(url, frmt=frmt)
        return res

    def pathway_hierarchy(self, species):
        """
        Get the pathways hierarchy for a species as displayed in Reactome pathway browser

        s = Reactome()
        s.pathway_hierarchy("homo sapiens")
        :param species: full species name
        """
        species = species.replace(" ", "+")
        res = self.http_get("pathwayHierarchy/{0}".format(species), frmt="xml")
        return res

    def pathway_participantes(self, identifier):
        """
        Get list of pathway participants for a pathway

        s = Reactome()
        s.pathway_participantes(109581)
        :param identifier: pathway database identifier
        """
        res = self.http_get("pathwayParticipants/{0}".format(identifier))
        return res

    def pathway_complexes(self, identifier):
        """
        Get complexes belonging to a patway

        s = Reactome()
        s.pathway_complexes(109581)
        :param identifier: pathway database identifier
        """
        res = self.http_get("pathwayComplexes/{0}".format(identifier))
        return res

    def query_by_id(self, classname, identifier):
        """
        Get Reactome Database for a specific object

        s = Reactome()
        s.query_by_id("Pathway", "109581")
        :param identifier: instance database identifer
        :param classname: class name
        """
        url = "queryById/{0}/{1}".format(classname, identifier)
        res = self.http_get(url)
        return res

    def query_by_ids(self, classname, identifiers):
        """
        Get Reactome Database for a specific object

        s = Reactome()
        s.query_by_ids("Pathway", "CDC2")

        not sure if wrapping is correct
        :param identifiers: database identifiers or stable identifiers
        :param classname: class name
        """
        identifiers = list2string(identifiers)
        url = "queryByIds/{0}".format(classname)
        res = self.http_post(url, frmt="json", data=identifiers, headers={'Content-Type': "application/json"})
        return res

    def query_hit_pathways(self, query):
        """
        Get pathways that contain one or more genes passed in the query list.
        In the Reactome data model, pathways are organized in a
        hierarchical structure. The returned pathways in this method are pathways
        having detailed manually drawn pathway diagrams. Currently only human
        pathways will be returned from this method.

        s.query_hit_pathways('CDC2')
        s.query_hit_pathways(['CDC2'])
        :param query: Gene symbols
        """
        identifiers = list2string(query, space=False)
        res = self.http_post("queryHitPathways", frmt='json', data=identifiers,
                             headers={'Content-Type': "application/json"})
        return res

    def query_pathway_for_entities(self, identifiers):
        """
        Get pathway objects by specifying an array of PhysicalEntity database identifiers.
        The returned Pathways should
        contain the passed EventEntity objects. All passed EventEntity database
        identifiers should be in the database.
        :param identifiers:
        """
        identifiers = list2string(identifiers, space=False)
        res = self.http_post("pathwaysForEntities", frmt='json', data={'ID': identifiers},
                             headers={'Content-Type': "application/json"})
        return res

    def query_reviewed_pathways(self, personid):
        """
        This API lets you query the Reactome Database for pathways reviewed by a particular person. It requires the
        DB_ID for the Person class. Person IDs can be located with either the QueryPeopleByName or QueryPeopleByEmail
        methods

        reactome.queryReviewedPathways(1169275)

        :param personid: personn ID
        :return:
        """
        url = "queryReviewedPathways/{0}".format(personid)
        res = self.http_get(url)
        return res

    def query_people_by_name(self, name):
        """
        This API lets you query the Reactome Database for a particular person. It requires a full or partial name.
        NOTE: spaces must be escaped with '%20'.
        :param name: name of persone
        :return:
        """
        name = name.replace(' ', '%20')
        url = "queryPeopleByName/{0}".format(name)
        res = self.http_get(url)
        return res

    def query_people_by_email(self, email):
        """
        This API lets you query the Reactome Database for a particular person by a valid email address.
        :param email: name of persone
        :return:
        """
        url = "queryPeopleByEmail/{0}".format(email)
        res = self.http_get(url)
        return res

    def species_list(self):
        """
        Get the list of species used in the Swithc Species box in Reactome pathway browser
        """
        url = "speciesList"
        res = self.http_get(url)
        return res

    def disease_list(self):
        """
        Get a list of diseases and their disease ontology Ids (DOID)
        """
        url = "getDiseases"
        res = self.http_get(url)
        return res

    def get_uniprot_ref_seqs(self):
        """
        Get a list of Reactome proteins that have UniProt identifiers
        """
        url = "getUniProtRefSeqs"
        res = self.http_get(url)
        return res

    def sbml_exporter(self, identifier):
        """
        Get the SBML XML text of a pathway identifier

        s = Reactome()
        xml = s.SBML_exporter(109581)
        :param identifier:
        """
        url = "sbmlExporter/{0}".format(identifier)
        res = self.http_get(url, frmt='xml')
        return res


class ReactomeAnalysis(REST):
    """
    Pathway Analysis Service
    Provides an API for pathway over-representation and expression analysis as well as species comparison tool

    http://www.reactome.org/AnalysisService/
    """

    def __init__(self):
        super(ReactomeAnalysis, self).__init__("Reactome Analysis", url="http://www.reactome.org:80/AnalysisService")
        log.warning("Class in development.")

    def identifiers(self, genes, human_projection=False):
        """
        Analyse the post identifiers over the different species and projects the result to Homo Sapiens
        s.identifiers("TP53")
        :param human_projection: project result to homo sapiens
        :param genes: gene like TP53
        """
        pagesize = 8000
        page = 1
        sortby = 'ENTITIES_PVALUE'
        params = {'pageSize': str(pagesize), 'page': str(page), 'sortBy': sortby, 'order': 'ASC',
                  'ressource': 'TOTAL'}

        if human_projection:
            url = "identifiers/projection?"
        else:
            url = "identifiers/?"
        genes = list2string(genes)
        genes = genes.replace(" ", "")
        res = self.http_post(url, frmt="json", data=genes, params=params,
                             headers={"Content-Type": "text/plain;charset=UTF-8", "Accept": "application/json"})
        return res

    def download(self, token):
        """
        Download data
        :param token:
        """
        raise NotImplementedError

    def identifier(self, id, human_projection=False):
        """
        analyse identifier
        :param human_projection: project to human
        :param id: id of identifier
        """
        pagesize = 8000
        page = 1
        sortby = 'ENTITIES_PVALUE'
        params = {'pageSize': str(pagesize), 'page': str(page), 'sortBy': sortby, 'order': 'ASC',
                  'ressource': 'TOTAL'}

        if human_projection:
            url = "identifier/{}/projection/".format(id)
        else:
            url = "identifier/{}".format(id)

        res = self.http_get(url, params=params,
                            headers={"Content-Type": "text/plain;charset=UTF-8", "Accept": "application/json"})
        return res

    def species(self, dbid):
        """
        Compare homo sapiens to specified species
        ra.species(48895)

        :param dbid: dbId of species
        """
        pagesize = 8000
        page = 1
        sortby = 'ENTITIES_PVALUE'
        params = {'pageSize': str(pagesize), 'page': str(page), 'sortBy': sortby, 'order': 'ASC',
                  'ressource': 'TOTAL'}

        url = "/species/homoSapiens/{}".format(dbid)
        res = self.http_get(url, params=params,
                            headers={"Content-Type": "text/plain;charset=UTF-8", "Accept": "application/json"})
        return res

    def token(self, token):
        """
        Return token
        :param token:
        """
        raise NotImplementedError
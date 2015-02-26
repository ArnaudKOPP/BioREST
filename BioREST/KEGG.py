# coding=utf-8
"""
This class is for Kegg REST api
KEGG is a database resource for understanding high-level functions and
utilities of the biological system, such as the cell, the organism and the
ecosystem, from molecular-level information, especially large-scale molecular
datasets generated by genome sequencing and other high-throughput experimental
technologies (See Release notes for new and updated features).
Documentation : http://www.kegg.jp/kegg/rest/keggapi.html

KEGG Databases Names and Abbreviations
-------------------------------------------

Here is a list of databases used in KEGG API with their name and abbreviation:

===================================================================================
Database        Name        Abbrev      kid             Remark
===================================================================================
KEGG PATHWAY 	pathway 	path 	    map number
KEGG BRITE 	    brite 	    br 	        br number
KEGG MODULE 	module 	    md 	        M number
KEGG ORTHOLOGY 	orthology 	ko 	        K number
KEGG GENOME 	genome 	    genome 	    T number
KEGG GENOMES 	genomes 	gn 	        T number 	    Composite database: genome+egenome+mgenome
KEGG GENES 	    genes 	    - 	        - 	            Composite database: consisting of KEGG organisms
KEGG LIGAND 	ligand 	    ligand 	    - 	            Composite database: compound+glycan+reaction+rpair+rclass+enzyme
KEGG COMPOUND 	compound 	cpd 	    C number 	    Japanese version: compound_ja cpd_ja
KEGG GLYCAN 	glycan 	    gl 	        G number
KEGG REACTION 	reaction 	rn 	        R number
KEGG RPAIR 	    rpair 	    rp 	        RP number
KEGG RCLASS 	rclass 	    rc 	        RC number
KEGG ENZYME 	enzyme 	    ec 	        -
KEGG DISEASE 	disease 	ds 	        H number 	    Japanese version: disease_ja ds_ja
KEGG DRUG 	    drug 	    dr 	        D number 	    Japanese version: drug_ja dr_ja
KEGG DGOUP 	    dgroup 	    dg 	        DG number 	    Japanese version: dgroup_ja dg_ja
KEGG ENVIRON 	environ 	ev 	        E number 	    Japanese version: environ_ja ev_ja
===================================================================================

# #### KEGG REST TEST

    from BioREST import KEGG, KEGGParser
    k = KEGG(verbose=True)
    # print(k.tnumber_to_code("T01001"))
    # print(k.databases)
    # print(k.code_to_tnumber("hsa"))
    # print(k.is_organism("hsa"))
    # print(k.info())
    # print(k.info("hsa"))
    # print(k.info("T01001"))  # same as above
    # print(k.info("pathway"))
    # k.list('organism')
    # print(k.organismIds)
    # print(k.pathwayIds)
    # print(k.get("hsa:7535"))
    # print(k.list("pathway", organism="hsa"))
    # print(k.list("pathway"))  # returns the list of reference pathways
    # print(k.list("pathway", "hsa"))  # returns the list of human pathways
    # print(k.list("organism"))  # returns the list of KEGG organisms with taxonomic classification
    # print(k.list("hsa"))  # returns the entire list of human genes
    # print(k.list("T01001"))  # same as above
    # print(k.list("hsa:10458+ece:Z5100"))  # returns the list of a human gene and an E.coli O157 gene
    # print(k.list("cpd:C01290+gl:G00092"))  # returns the list of a compound entry and a glycan entry
    # print(k.list("C01290+G00092"))  # same as above
    # # search for pathways that contain Viral in the definition
    # print(k.find("pathway", "Viral"))
    # # for keywords "shiga" and "toxin"
    # print(k.find("genes", "shiga+toxin"))
    # # for keywords "shiga toxin"
    # print(k.find("genes", "shiga toxin"))
    # # for chemical formula "C7H10O5"
    # print(k.find("compound", "C7H10O5", "formula"))
    # # for chemical formula containing "O5" and "C7"
    # print(k.find("compound", "O5C7", "formula"))
    # # for 174.045 =< exact mass < 174.055
    # print(k.find("compound", "174.05", "exact_mass"))
    # # for 300 =< molecular weight =< 310
    # print(k.find("compound", "300-310", "mol_weight"))
    # # retrieves a compound entry and a glycan entry
    # print(k.get("cpd:C01290+gl:G00092"))
    # # same as above
    # print(k.get("C01290+G00092"))
    # # retrieves a human gene entry and an E.coli O157 gene entry
    # print(k.get("hsa:10458+ece:Z5100"))
    # # retrieves amino acid sequences of a human gene and an E.coli O157 gene
    # print(k.get("hsa:10458+ece:Z5100/aaseq"))
    # res = k.get("hsa05130/image")
    # # same as : res = s.get("hsa05130","image")
    # f = open("test.png", "wb")
    # f.write(res)
    # f.close()
    # # conversion from NCBI GeneID to KEGG ID for E. coli genes
    # print(k.conv("eco", "ncbi-geneid"))
    # # inverse of the above example
    # print(k.conv("eco", "ncbi-geneid"))
    # # conversion from KEGG ID to NCBI GI
    # print(k.conv("ncbi-gi", "hsa:10458+ece:Z5100"))
    # # KEGG pathways linked from each of the human genes
    # print(k.link("pathway", "hsa"))
    # # human genes linked from each of the KEGG pathways
    # print(k.link("hsa", "pathway"))
    # # KEGG pathways linked from a human gene and an E. coli O157 gene.
    # print(k.link("pathway", "hsa:10458+ece:Z5100"))
    # # show a pathway in the browser
    # k.show_pathway("path:hsa05416", scale=50)
    # # Same as above but also highlights some KEGG Ids (red for all)
    # k.show_pathway("path:hsa05416", dcolor="white", keggid=['1525', '1604', '2534'])
    # # You can refine the colors using a dictionary:
    # k.show_pathway("path:hsa05416", dcolor="white", keggid={'1525': 'yellow,red', '1604': 'blue,green', '2534': "blue"})
    # print(k.get_pathway_by_gene("7535", "hsa"))
    # s = KEGGParser()
    # data = s.get("hsa:7535")
    # dict_data = s.parse(data)
    # print(dict_data)
    # data = s.get("hsa04660")
    # dict_data = s.parse(data)
    # print(dict_data['gene'])
    # res = s.get("hsa04660", "kgml")
    # print(res)
    # res = s.parse_kgml_pathway("hsa04660")
    # # print(res)
    # res['relations']
    # print(res['relations'][0])

"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import webbrowser
import collections
import logging
from BioREST.Service import REST

log = logging.getLogger(__name__)


class KEGG(REST):
    """
    Interface to Kegg REST api

    This class provides an interface to the KEGG REST API. The weblink tools
    are partially accesible. All dbentries can be parsed into dictionaries using
    the :class:`KEGGParser`

    """

    def __init__(self):
        super(KEGG, self).__init__(name="KEGG", url="http://rest.kegg.jp")
        self.easyXMLConversion = False
        self._organism = None
        self._organisms = None
        self._pathway = None
        self._glycan = None
        self._compound = None
        self._ko = None
        self._enzyme = None
        self._reaction = None
        self._brite = None
        self._buffer = {}

    def __getattr__(self, req):
        if req.endswith("Ids"):
            db = req[0:-3]
            res = self.list(db)
            if db in [","]:
                ids = [x.split()[1] for x in res.split("\n") if len(x)]
            else:
                ids = [x.split()[0] for x in res.split("\n") if len(x)]
            return ids
        elif req in self.databases:
            res = self.list(req)
            return res

    def code_to_tnumber(self, code):
        """
        Converts organism code to its T number

        :param code:  code to convert
        """
        index = self.organismIds.index(code)
        return self.organismTnumbers[index]

    def tnumber_to_code(self, tnumber):
        """
        Converts organism T number to its code

        :param tnumber: code to convert
        """
        index = self.organismTnumbers.index(tnumber)
        return self.organismIds[index]

    def is_organism(self, org_id):
        """
        Check if orgId is a Kegg organism

        :param org_id: orgranism id to check
        """
        if org_id in self.organismIds:
            return True
        if org_id in self.organismTnumbers:
            return True
        else:
            return False

    def info(self, query="kegg"):
        """
        Display current statistics of given database or organism

        :param query: can be one of database: kegg (default), brite, module,
            disease, drug, environ, ko, genome, compound, glycan, reaction,
            rpair, rclass, enzyme, genomes, genes, ligand or any organismID

        """
        _valid_databases = ["pathway", "brite", "module", "ko", "genome", "compound", "glycan", "reaction", "rpair",
                            "rclass", "enzyme", "disease", "drug", "dgroup", "environ", "genomes", "genes", "ligand",
                            "kegg"]

        if query not in _valid_databases and not self.is_organism(query):
            raise ValueError('Database provided not available for this operation')
        url = "info/" + query
        res = self.http_get(url, frmt="txt")
        return res

    def list(self, query, organism=None):
        """
        Returns a list of entry identifiers and associated definition for a given database or a given set of
        database entries

        :param query:can be one of pathway, brite, module,
            disease, drug, environ, ko, genome, compound,
            glycan, reaction, rpair, rclass, enzyme, organism
            **or** an organism from the :attr:`organismIds` attribute **or** a valid
            dbentry (see below). If a dbentry query is provided, organism
            should not be used!
        :param organism: a valid organism identifier that can be
            provided. If so, database can be only "pathway" or "module". If
            not provided, the default value is chosen (:attr:`organism`)
        :return: A string with a structure that depends on the query

        Note, however, that there are convenient aliases to some of the databases.
        For instance, the pathway Ids can also be retrieved as a list from the
        :attr:`pathwayIds` attribute (after defining the :attr:`organism` attribute).

         note:: If you set the query to a valid organism, then the second
        argument rganism is irrelevant and ignored.

        note:: If the query is not a database or an organism, it is supposed
        to be a valid dbentries string and the maximum number of entries is 100.

        """
        _valid_databases = ["pathway", "brite", "module", "ko", "genome", "compound", "glycan", "reaction", "rpair",
                            "rclass", "enzyme", "disease", "drug", "dgroup", "environ", 'organism']
        if query not in _valid_databases and not self.is_organism(query):
            log.warning("Not a database and not a orgID, hop for you that it's a valid ID.")

        url = "list"
        if query:
            url += "/" + query

        if organism:
            if organism not in self.organismIds:
                raise Exception(
                    "Not a valid organism Invalid organism provided (%s). See the organismIds attribute" % organism)
            if query not in ["pathway", "module"]:
                log.error("""If organism is set, then the first argument (database) must be either 'pathway' or
                'module', you provided %s""" % query)
            url += "/" + organism

        res = self.http_get(url, "txt")
        return res

    def find(self, database, query, option=None):
        """
        finds entries with matching query keywords or other query data in a given database

        :param str database: can be one of pathway, module, disease, drug,
                environ, ko, genome, compound, glycan, reaction, rpair, rclass,
                enzyme, genes, ligand or an organism code or T number .
        :param str query: keywords
        :param str option: If option provided, database can be only 'compound'
                or 'drug'. Option can be 'formula', 'exact_mass' or 'mol_weight'

        note:: Keyword search against brite is not supported. Use /list/brite to
        retrieve a short list.

        """
        _valid_databases = ["pathway", "module", "ko", "genome", "compound", "glycan", "reaction", "rpair",
                            "rclass", "enzyme", "disease", "drug", "dgroup", "environ", "genes", "ligand"]

        isOrg = self.is_organism(database)
        if database not in _valid_databases and isOrg is False:
            raise ValueError('Database provided not available for this operation')

        _valid_options = ['formula', "exact_mass", "mol_weight"]
        _valid_db_options = ["compound", "drug"]

        url = "find/" + database + "/" + query

        if option:
            if database not in _valid_db_options:
                raise ValueError(
                    "Invalid database. Since option was provided, database must be in {}".format(_valid_db_options))
            if option not in _valid_options:
                raise ValueError("Invalid option. Must be in {}".format(_valid_options))
            url += "/" + option

        res = self.http_get(url, frmt="txt")
        return res

    def get(self, dbentries, option=None):
        """
        Retrieves given database entrie
        :param dbentries:  KEGG database entries involving the following
            database: pathway, brite, module, disease, drug, environ, ko, genome
            compound, glycan, reaction, rpair, rclass, enzyme **or** any organism
            using the KEGG organism code (see :attr:`organismIds`
            attributes) or T number (see :attr:`organismTnumbers` attribute).
        :param option: aaseq, ntseq, mol, kcf, image, kgml

        .note:: The input is limited up to 10 entries (KEGG restriction).
        """

        _valid_options = ["aaseq", "ntseq", "mol", "kcf", "image", "kgml"]

        url = "get/" + dbentries

        if option:
            if option not in _valid_options:
                raise AttributeError("Invalid Option. Must be in %s" % _valid_options)
            url += "/" + option

        res = self.http_get(url, frmt="txt")
        return res

    def conv(self, target, source):
        """
        Convert KEGG identifiers to/from outside identifiers

        :param target: target database (kegg orga)
        :param source: source database (uniprot or valid dbentries
        :return: dict with keys being the source and value being the target
        Here are the rules to set the target and source parameters.
        If the second argument is not a **dbentries**, source and target
        parameters can be of two types:
        #. gene identifiers. If the target is a KEGG Id, then the source
        must be one of *ncbi-gi*, *ncbi-geneid* or *uniprot*.

        note:: source and target can be swapped.
        #. chemical substance identifiers. If the target is one of the
        following kegg database: drug, compound, glycan then the source
        must be one of *pubchem* or *chebi*.

        note:: again, source and target can be swapped
        If the second argument is a **dbentries**, it can be again of two types:
        #. gene identifiers. The database used can be one ncbi-gi,
        ncbi-geneid, uniprot or any KEGG organism
        #. chemical substance identifiers. The database used can be one of
        drug, compound, glycan, pubchem or chebi only.

        note:: if the second argument is a dbentries, target and dbentries
        cannot be swapped.
        """

        isorg = self.is_organism(target)
        if isorg is False and target not in ['ncbi-gi', 'ncbi-geneid', 'uniprot', 'pubchem', 'chebi', 'drug',
                                             'compound', 'glycan']:
            raise AttributeError("Invalid syntax, target must be a KEGG id or one of the allowed database")

        url = "conv/" + target + "/" + source
        res = self.http_get(url, frmt="txt")

        try:
            t = [x.split("\t")[0] for x in res.strip().split("\n")]
            s = [x.split("\t")[1] for x in res.strip().split("\n")]
            return dict([(x, y) for x, y in zip(t, s)])
        except:
            return res

    def link(self, target, source):
        """
        find related entries by using database cross-reference
        :param target: kegg database target or organism
        :param source: kegg database target or organism or a valid dbentries involving one of the database

        the valid list of db is pathway, brite, module, disease, drug, environ, ko, genome, compound, glycan, reaction
        rpair, rclass, enzyme
        """
        _valid_databases = ["pathway", "brite", "module", "ko", "genome", "compound", "glycan", "reaction", "rpair",
                            "rclass", "enzyme", "disease", "drug", "dgroup", "environ", "genes"]

        if target not in _valid_databases and not self.is_organism(target):
            raise ValueError('Database target source provided not available for this operation')
        if source not in _valid_databases and not self.is_organism(source):
            log.warning("[list] Not a database and not a orgID, hop for you that it's a valid ID.")

        url = "link/" + target + "/" + source
        res = self.http_get(url, frmt="txt")
        return res

    @staticmethod
    def show_pathway(path_id, scale=None, dcolor="pink", keggid={}):
        """
        show a given path into webbrower

        :param path_id: valid path id
        :param scale: scale image between 0 and 100
        :param dcolor: default background color of nodes
        :param keggid: set color of entries contained in the pathways

        if scale is provided, keggid and dcolor is ignored

        """
        if path_id.startswith("path:"):
            path_id = path_id.split(":")[1]

        if scale:
            scale = int(scale / 100. * 100) / 100.  # just need 2 digits and a value in [0,1]
            url = "http://www.kegg.jp/kegg-bin/show_pathway?scale=" + str(scale)
            url += "&query=&map=" + path_id
        else:
            url = "http://www.kegg.jp/kegg-bin/show_pathway?" + path_id
            if dcolor:
                url += "/default%%3d%s/" % dcolor
            if isinstance(keggid, dict):
                if len(keggid.keys()) > 0:
                    for k, v in keggid.items():
                        if "," in v:
                            url += "/%s%%09%s/" % (k, v)
                        else:
                            url += "/%s%%09,%s/" % (k, v)
            elif isinstance(keggid, list):
                for k in keggid:
                    url += "/%s%%09,%s/" % (k, "red")

        res = webbrowser.open(url)
        return res

    def _get_db(self):
        return KEGG.info(self)

    databases = property(_get_db, doc="Returns list of valid KEGG databases.")

    def _get_database(self, dbname, mode=0):
        res = self.list(dbname)
        assert mode in [0, 1]
        return [x.split()[mode] for x in res.split("\n") if len(x)]

    def _get_organisms(self):
        if self._organisms is None:
            self._organisms = self._get_database("organism", 1)
        return self._organisms

    organismIds = property(_get_organisms, doc="Returns list of organism Ids")

    def _get_reactions(self):
        if self._reaction is None:
            self._reaction = self._get_database("reaction")
        return self._reaction

    reactionIds = property(_get_reactions, doc="returns list of reaction Ids")

    def _get_enzyme(self):
        if self._enzyme is None:
            self._enzyme = self._get_database("enzyme")
        return self._enzyme

    enzymeIds = property(_get_enzyme, doc="returns list of enzyme Ids")

    def _get_organisms_tnumbers(self):
        if self._organisms_tnumbers is None:
            self._organisms_tnumbers = self._get_database("organism")
        return self._organisms_tnumbers

    organismTnumbers = property(_get_organisms_tnumbers, doc="returns list of organisms (T numbers)")

    def _get_glycans(self):
        if self._glycan is None:
            self._glycan = self._get_database("glycan")
        return self._glycan

    glycanIds = property(_get_glycans, doc="Returns list of glycan Ids")

    def _get_brite(self):
        if self._brite is None:
            self._brite = self._get_database("brite")
        return self._brite

    briteIds = property(_get_brite, doc="returns list of brite Ids.")

    def _get_kos(self):
        if self._ko is None:
            self._ko = self._get_database("ko")
        return self._ko

    koIds = property(_get_kos, doc="returns list of ko Ids")

    def _get_compound(self):
        if self._compound is None:
            self._compound = self._get_database("compound")
        return self._compound

    compoundIds = property(_get_compound, doc="returns list of compound Ids")

    def _get_drug(self):
        if self._drug is None:
            self._drug = self._get_database("drug")
        return self._drug

    drugIds = property(_get_drug, doc="returns list of drug Ids")

    def _get_organism(self):
        return self._organism

    def _set_organism(self, organism):
        if organism in self.organismIds:
            self._organism = organism
            self._pathway = None
            self._module = None
            self._ko = None
            self._glycan = None
            self._compound = None
            self._enzyme = None
            self._drug = None
            self._reaction = None
            self._brite = None
        else:
            raise ValueError("Invalid organism. Check the list in :attr:`organismIds` attribute")

    def _get_pathways(self):
        if self._organism is None:
            log.warning("You must set the organism first (e.g., self.organism = 'hsa')")
            return

        if self._pathway is None:
            res = self.http_get("list/pathway/%s" % self.organism, frmt="txt")
            orgs = [x.split()[0] for x in res.split("\n") if len(x)]
            self._pathway = orgs[:]
        return self._pathway

    def _get_modules(self):
        if self._organism is None:
            log.warning("You must set the organism first (e.g., self.organism = 'hsa')")
            return

        if self._module is None:
            res = self.http_get("list/module/%s" % self.organism)
            orgs = [x.split()[0] for x in res.split("\n") if len(x)]
            self._module = orgs[:]
        return self._module

    def lookfor_organism(self, query):
        """
        Look for a specific organism
        :param str query: your search term. upper and lower cases are ignored
        :return: a list of definition that matches the query
        """
        matches = []
        definitions = [" ".join(x.split()) for x in self.list("organism").split("\n")]
        for i, item in enumerate(definitions):
            if query.lower() in item.lower():
                matches.append(i)
        return [definitions[i] for i in matches]

    def lookfor_pathway(self, query):
        """
        Look for a specific pathway
        :param str query: your search term. upper and lower cases are ignored
        :return: a list of definition that matches the query
        """
        matches = []
        definitions = [" ".join(x.split()) for x in self.list("pathway").split("\n")]
        for i, item in enumerate(definitions):
            if query.lower() in item.lower():
                matches.append(i)
        return [definitions[i] for i in matches]

    def parse_kgml_pathway(self, pathways_id, res=None):
        """
        Parse the pathway in KGML format and returns a dictionary (relations and entries)
        :param str pathways_id: a valid pathwayId e.g. hsa04660
        :param str res: if you already have the output of the query
            get(pathwayId), you can provide it, otherwise it is queried.
        :return: a tuple with the first item being a list of relations. Each
            relations is a dictionary with id2, id2, link, value, name. The
            second item is a dictionary that maps the Ids to
        ::
            res = s.parse_kgml_pathway("hsa04660")
            set([x['name'] for x in res['relations']])
            res['relations'][-1]
            {'entry1': u'15',
             'entry2': u'13',F
             'link': u'PPrel',
             'name': u'phosphorylation',
             'value': u'+p'}
            set([x['link'] for x in res['relations']])
            set([u'PPrel', u'PCrel'])
            res['entries'][4]
        ret = s.get("hsa04660", "kgml")
        .. seealso:: `KEGG API <http://www.kegg.jp/kegg/xml/docs/>`_
        """
        output = {'relations': [], 'entries': []}
        if res is None:
            res = self.easyXML(self.get(pathways_id, "kgml"))
        else:
            res = self.easyXML(res)
        # here entry1 and 2 are Id related to the kgml file

        # read and parse the entries
        entries = [x for x in res.findAll("entry")]
        for entry in entries:
            output['entries'].append({
                'id': entry.get("id"),
                'name': entry.get("name"),
                'type': entry.get("type"),
                'link': entry.get("link"),
                'gene_names': entry.find("graphics").get("name")
            })

        relations = [(x.get("entry1"), x.get("entry2"), x.get("type")) for x in res.findAll("relation")]
        subtypes = [x.findAll("subtype") for x in res.findAll("relation")]

        assert len(subtypes) == len(relations)

        for relation, subtype in zip(relations, subtypes):
            if len(subtype) == 0:
                pass
            else:
                for this in subtype:
                    value = this.get("value")
                    name = this.get("name")
                    output['relations'].append({
                        'entry1': relation[0],
                        'entry2': relation[1],
                        'link': relation[2],
                        'value': value,
                        'name': name})
        # we need to map back to KEgg IDs...
        return output

    def __str__(self):
        txt = self.info()
        return txt


def KEGGParser(res):
    """
    A dispatcher to parse all outputs returned by :meth:`KEGG.get`

    ENTRY       26153             CDS       T01001
    NAME        KIF26A
    DEFINITION  kinesin family member 26A
    ORTHOLOGY   K10404  kinesin family member 26
    ORGANISM    hsa  Homo sapiens (human)
    POSITION    14q32.33
    MOTIF       Pfam: Kinesin
    DBLINKS     NCBI-GI: 150170699
                NCBI-GeneID: 26153
                OMIM: 613231
                HGNC: 20226
                Ensembl: ENSG00000066735
                Vega: OTTHUMG00000154986
                UniProt: Q9ULI4
    AASEQ       1882


    :param str res: output of a KEGG.get
    :return: a dictionary
    """
    output = collections.OrderedDict()
    lines = res.split("\n")
    last_idx = None
    for line in lines:
        if line.startswith("///"):
            return output

        if line.startswith(" "):
            output.setdefault(last_idx, []).append(line.strip())
        else:
            last_idx = line.split()[0]
            output[last_idx] = [line[10:].strip()]
    return output
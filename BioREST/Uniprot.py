# coding=utf-8
"""
Uniprot class

http://www.uniprot.org/help/programmatic_access

# #### UNIPROT REST TEST

    # from BioREST import UniProt
    # u = UniProt(user='kopp@igbmc.fr')
    # print(u.mapping("ACC", "KEGG_ID", query='P43403 P29317'))
    # res = u.search("P43403")
    # print(res)
    # # u.download_flat_files()
    # # Returns sequence on the ZAP70_HUMAN accession Id
    # sequence = u.search("ZAP70_HUMAN", columns="sequence")
    # print(sequence)
    # fasta = u.retrieve([u'P29317', u'Q5BKX8', u'Q8TCD6'], frmt='fasta')
    # print(fasta[0])
    # res = u.retrieve("P09958", frmt="xml")
    # print(res)
    # res = u.get_fasta("P09958")
    # print(res)
    # print(u.get_fasta_sequence("P09958"))
    # print(u.search('zap70+AND+organism:9606', frmt='list'))
    # print(u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, columns="entry name,length,id, genes"))

"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import io
import urllib.request
import gzip
import os
import logging
import pandas as pd
from BioREST.Service import REST, list2string, check_param_in_list, tolist, reporthook
from BioREST.Fasta import FASTA

log = logging.getLogger(__name__)


class UniProt(REST):
    """
    Interface to the uniprot service
    u = UniProt()
    u.mapping("ACC", "KEGG_ID", query='P43403')
    defaultdict(<type 'list'>, {'P43403': ['hsa:7535']})
    res = u.search("P43403")
    # Returns sequence on the ZAP70_HUMAN accession Id
    sequence = u.search("ZAP70_HUMAN", columns="sequence")
    """
    _mapping = {"ACC/ID": "UniProTKB AC+ID",
                "ACC": "UniProTKB ACC",
                "ID": "UniProTKB ID",
                "UniParc": "UPARC",
                "UniRef50": "NF50",
                "UniRef90": "NF90",
                "UniRef100": "NF100",
                # Other sequence databses
                "EMBL/GenBank/DDBJ": "EMBL_ID",
                "EMBL/GenBank/DDBJ CDS": "EMBL",
                "PIR": "PIR",
                "UniGene": "UNIGENE_ID",
                "Entrez Gene (GeneID)": "P_ENTREZGENEID",
                "GI number*": "P_GI",
                "RefSeq Protein": "P_REFSEQ_AC",
                "RefSeq Nucleotide": "REFSEQ_NT_ID",
                # 3D structure database
                "PDB": "PDB_ID",
                "DisProt": "DISPROT_ID",
                # PP interaction database
                "BioGrid": "BIOGRID_ID",
                "DIP": "DIP_ID",
                "MINT": "MINT_ID",
                "STRING": "STRING_ID",
                # chemistry
                "ChEMBL": "CHEMBL_ID",
                "DrugBank": "DRUGBANK_ID",
                "GuidetoPHARMACOLOGY": "GUIDETOPHARMACOLOGY_ID",
                # protein family/group database
                "Allergome": "ALLERGOME_ID",
                "MEROPS": "MEROPS_ID",
                "mycoCLAP": "MYCOCLAP_ID",
                "PeroxiBase": "PEROXIBASE_ID",
                "PptaseDB": "PPTASEDB_ID",
                "REBASE": "REBASE_ID",
                "TCDB": "TCDB_ID",
                # PTM database
                "PhosSite": "PHOSSITE_ID",
                # polymorphism database
                "DMDM": "DMDM_ID",
                # 2D get databases
                "World-2DPAGE": "WORLD_2DPAGE_ID",
                # protocol and materials database
                "DNASU": "DNASU_ID",
                # Genome annotation databases
                "Ensembl": "ENSEMBL_ID",
                "Ensembl Protein": "ENSEMBL_PRO_ID",
                "Ensembl Transcript": "ENSEMBL_TRS_ID",
                "Ensembl Genomes": "ENSEMBLGENOME_ID",
                "Ensembl Genomes Protein": "ENSEMBLGENOME_PRO_ID",
                "Ensembl Genomes Transcript": "ENSEMBLGENOME_TRS_ID",
                "GeneID": "P_ENTREZGENEID",
                "GenomeReviews": "GENOMEREVIEWS_ID",
                "KEGG": "KEGG_ID",
                "PATRIC": "PATRIC_ID",
                "UCSC": "UCSC_ID",
                "VectorBase": "VECTORBASE_ID",
                # Organism-specific gene databases
                "ArachnoServer": "ARACHNOSERVER_ID",
                "CGD": "CGD",
                "ConoServer": "CONOSERVER_ID",
                "CYGD": "CYGD_ID",
                "dictyBase": "DICTYBASE_ID",
                "EchoBASE": "ECHOBASE_ID",
                "EcoGene": "ECOGENE_ID",
                "euHCVdb": "EUHCVDB_ID",
                "EuPathDB": "EUPATHDB_ID",
                "FlyBase": "FLYBASE_ID",
                "GeneCards": "GENECARDS_ID",
                "GeneFarm": "GENEFARM_ID",
                "GenoList": "GENOLIST_ID",
                "H-InvDB": "H_INVDB_ID",
                "HGNC": "HGNC_ID",
                "HPA": "HPA_ID",
                "LegioList": "LEGIOLIST_ID",
                "Leproma": "LEPROMA_ID",
                "MaizeGDB": "MAIZEGDB_ID",
                "MIM": "MIM_ID",
                "MGI": "MGI_ID",
                "neXtProt": "NEXTPROT_ID",
                "Orphanet": "ORPHANET_ID",
                "PharmGKB": "PHARMGKB_ID",
                "PomBase": "POMBASE_ID",
                "PseudoCAP": "PSEUDOCAP_ID",
                "RGD": "RGD_ID",
                "SGD": "SGD_ID",
                "TAIR": "TAIR_ID",
                "TubercuList": "TUBERCULIST_ID",
                "WormBase": "WORMBASE_ID",
                "WormBase Transcript": "WORMBASE_TRS_ID",
                "WormBase Protein": "WORMBASE_PRO_ID",
                "Xenbase": "XENBASE_ID",
                "ZFIN": "ZFIN_ID",
                # Phylogenomic database
                "eggNOG": "EGGNOG_ID",
                "GeneTree": "GENETREE_ID",
                "HOGENOM": "HOGENOM_ID",
                "HOVERGEN": "HOVERGEN_ID",
                "KO": "KO_ID",
                "OMA": "OMA_ID",
                "OrthoDB": "ORTHODB_ID",
                "ProtClustDB": "PROTCLUSTDB_ID",
                "TreeFarm": "TREEFRAM_ID",
                # Enzyme and pathway database
                "BioCyc": "BIOCYC_ID",
                "Reactome": "REACTOME_ID",
                "UniPathWay": "UNIPATHWAY_ID",
                # other
                "ChiTaRS": "CHITARS_ID",
                "GenomeRNAi": "GENOMERNAI_ID",
                "GeneWiki": "GENEWIKI_ID",
                "NextBio": "NEXTBIO_ID"}

    _url = "http://www.uniprot.org"
    _valid_columns = ['citation', 'clusters', 'comments', 'database', 'domains', 'domain', 'ec', 'id', 'entry name',
                      'existence', 'families', 'feature', 'features', 'genes', 'go', 'go-id', 'interpro', 'interactor',
                      'keywords', 'keyword-id', 'last-modified', 'length', 'organism', 'organism-id', 'pathway',
                      'protein names', 'reviewed', 'score', 'sequence', '3d', 'subcellular locations', 'taxonomy',
                      'tools', 'version', 'virus hosts', 'lineage-id', 'sequence-modified', 'proteome']

    def __init__(self, user="TransCellAssayUser"):
        """
        **Constructor**
        """
        super(UniProt, self).__init__(name="UniProt", url=UniProt._url)
        self.TIMEOUT = 100
        self.__uniprot_flt_file = None
        self.__headers = {'User-Agent': str(user)}

    def download_flat_files(self, directory=''):
        """
        Download uniprot swissprot fasta file
        :param directory: Where to save file
        """
        print('\033[0;32m[INFO]\033[0m Retrieving file')
        url = "ftp://ftp.ebi.ac.uk/pub/databases/uniprot/knowledgebase/uniprot_sprot.dat.gz"
        gzfile = os.path.join(directory, "uniprot_sprot.dat.gz")
        urllib.request.urlretrieve(url=url, filename=gzfile, reporthook=reporthook)

        print("\033[0;33m[WARNING]\033[0m Uncompressing file...")
        str_file = gzip.open("uniprot_sprot.dat.gz")
        content = str_file.read()
        self.__uniprot_flt_file = os.path.join(directory, "uniprot_sprot.fasta")
        f = open(self.__uniprot_flt_file, "wb")
        f.write(content)
        f.close()
        print('\033[0;32m[INFO]\033[0m Finish uncompressing file')

    def mapping(self, fr="ID", to="KEGG_ID", query="P13368"):
        """
        This is an interface to the UniProt mapping service
        :param fr: the source database identifier.
        :param to: the targetted database identifier.
        :param query: a string containing one or more IDs separated by a space
        It can also be a list of strings.
        :return: a list. The first element is the source database Id. The second
        is the targetted source identifier. Following elements are alternate
        of one the entry and its mapped Id. If a query has several mapped
        Ids, the query is repeated (see example with PDB mapping here below)
        e.g., ["From:ID", "to:PDB_ID", "P43403"]

        u.mapping("ACC", "KEGG_ID", 'P43403')
        defaultdict(<type 'list'>, {'P43403': ['hsa:7535']})
        u.mapping("ACC", "KEGG_ID", 'P43403 P00958')
        defaultdict(<type 'list'>, {'P00958': ['sce:YGR264C'], 'P43403': ['hsa:7535']})
        u.mapping("ID", "PDB_ID", "P43403")
        defaultdict(<type 'list'>, {'P43403': ['1FBV', '1M61', '1U59',
        '2CBL', '2OQ1', '2OZO', '2Y1N', '3ZNI', '4A4B', '4A4C', '4K2R']})

        """
        url = 'mapping/'  # the slash matters

        query = list2string(query, sep=" ", space=False)
        params = {'from': fr, 'to': to, 'format': "tab", 'query': query}
        result = self.http_post(url, frmt="txt", data=params, headers=self.__headers)

        try:
            result = result.split()
            del result[0]
            del result[0]
        except:
            print("\033[0;33m[WARNING]\033[0m Results seems empty...returning empty dictionary.")
            return {}

        if len(result) == 0:
            return {}
        else:
            from collections import defaultdict
            result_dict = defaultdict(list)

            keys = result[0::2]
            values = result[1::2]
            for i, key in enumerate(keys):
                result_dict[key].append(values[i])
        return result_dict

    def retrieve(self, uniprot_id, frmt="xml"):
        """
        Search for a uniprot ID in UniprotKB database

        u = UniProt()
        res = u.retrieve("P09958", frmt="xml")
        fasta = u.retrieve([u'P29317', u'Q5BKX8', u'Q8TCD6'], frmt='fasta')
        print(fasta[0])
        :param uniprot_id:
        :param frmt:
        """
        _valid_formats = ['txt', 'xml', 'rdf', 'gff', 'fasta']
        check_param_in_list(frmt, _valid_formats)
        queries = tolist(uniprot_id)

        url = ["uniprot/" + query + '.' + frmt for query in queries]
        res = self.http_get(url, frmt="txt", headers=self.__headers)
        if frmt == "xml":
            res = [self.easyXML(x) for x in res]
        if isinstance(res, list) and len(res) == 1:
            res = res[0]
        return res

    @staticmethod
    def get_fasta(id):
        """
        Returns FASTA string given a valid identifier
        :param id:
        """
        f = FASTA()
        f.load_fasta(id)
        return f.fasta

    @staticmethod
    def get_fasta_sequence(id):
        """
        Returns FASTA sequence

        :param id:
        warning:: this is the sequence found in a fasta file, not the fasta
        content itself. The difference is that the header is removed and the
        formatting of end of lines every 60 characters is removed.
        """
        f = FASTA()
        f.load_fasta(id)
        return f.sequence

    def search(self, query, frmt="tab", columns=None, include=False, sort="score", compress=False, limit=None,
               offset=None):
        """
        Provide some interface to the uniprot search interface.
        :param str query: query must be a valid uniprot query.
        See http://www.uniprot.org/help/text-search, http://www.uniprot.org/help/query-fields
        See also example below
        :param str frmt: a valid format amongst html, tab, xls, asta, gff,
        txt, xml, rdf, list, rss. If tab or xls, you can also provide the
        columns argument. (default is tab)
        :param str columns: comma-separated list of values. Works only if fomat
        is tab or xls. For UnitProtKB, some possible columns are:
        id, entry name, length, organism. Some column name must be followed by
        database name (e.g., "database(PDB)"). Again, see uniprot website
        for more details. See also :attr:`~bioservices.uniprot.UniProt._valid_columns`
        for the full list of column keyword.
        :param bool include: include isoform sequences when the frmt
        parameter is fasta. Include description when frmt is rdf.
        :param str sort: by score by default. Set to None to bypass this behaviour
        :param bool compress: gzip the results
        :param int limit: Maximum number of results to retrieve.
        :param int offset: Offset of the first result, typically used together
        with the limit parameter.

        To obtain the list of uniprot ID returned by the search of zap70 can be
        retrieved as follows::
        u.search('zap70+AND+organism:9606', frmt='list')
        u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, columns="entry name,length,id, genes")

        Entry name Length Entry Gene names
        CBLB_HUMAN 982 Q13191 CBLB RNF56 Nbla00127
        CBL_HUMAN 906 P22681 CBL CBL2 RNF55
        CD3Z_HUMAN 164 P20963 CD247 CD3Z T3Z TCRZ
        other examples::
        u.search("ZAP70+AND+organism:9606", limit=3, columns="id,database(PDB)")

        You can also do a search on several keywords. This is especially useful
        if you have a list of known entry names.::
        u.search("ZAP70_HUMAN+or+CBL_HUMAN", frmt="tab", limit=3, columns="entry name,length,id, genes")

        Entry name Length Entry Gene names
        .. warning:: this function request seems a bit unstable (UniProt web issue ?)
        so we repeat the request if it fails
        .. warning:: some columns although valid may not return anything, not even in
        the header: 'score', 'taxonomy', 'tools'. this is a uniprot feature
        """
        params = {}

        if frmt is not None:
            _valid_formats = ['tab', 'xls', 'fasta', 'gff', 'txt', 'xml', 'rss', 'list', 'rss', 'html']
            check_param_in_list(frmt, _valid_formats)
            params['format'] = frmt

        if columns is not None:
            check_param_in_list(frmt, ["tab", "xls"])

            if "," in columns:
                columns = [x.strip() for x in columns.split(",")]
            else:
                columns = [columns]

            for col in columns:
                if col.startswith("database(") is True:
                    pass
                else:
                    check_param_in_list(col, self._valid_columns)

            params['columns'] = ",".join([x.strip() for x in columns])

        if include is True and frmt in ["fasta", "rdf"]:
            params['include'] = 'yes'

        if compress is True:
            params['compress'] = 'yes'

        if sort:
            check_param_in_list(sort, ["score"])
            params['sort'] = sort

        if offset is not None:
            if isinstance(offset, int):
                params['offset'] = offset

        if limit is not None:
            if isinstance(limit, int):
                params['limit'] = limit

        params['query'] = query.replace("+", " ")

        res = self.http_get("uniprot/", frmt="txt", params=params, headers=self.__headers)
        return res

    def quick_search(self, query, include=False, sort="score", limit=None):
        """

        :param query:
        :param include:
        :param sort:
        :param limit:
        a specialised version of :meth:`search`

        This is equivalent to::

            u = uniprot.UniProt()
            u.search(query, frmt="tab", include=False, sort="score", limit=None)

        :returns: a dictionary.
        """
        res = self.search(query, "tab", include=include, sort=sort, limit=limit)

        if len(res) == 0:
            return res

        newres = {}
        for line in res.split("\n")[1:-1]:
            entry, a, b, c, d, e, f = line.split("\t")
            newres[entry] = {'Entry name': a, 'Status': b, 'Protein names': c, 'Gene names': d, 'Organism': e,
                             'Length': f}
        return newres

    def uniref(self, query):
        """
        Calls UniRef service

        u = UniProt()
        :param query:
        df = u.uniref("member:Q03063")
        df.Size
        """
        res = self.http_get("uniref/", params={"query": query, 'format': 'tab'}, frmt="txt", headers=self.__headers)
        res = pd.read_csv(io.StringIO(res.strip()), sep="\t")
        return res

    def get_df(self, entries, nchunk=100, organism=None):
        """
        Given a list of uniprot entries, this method returns a dataframe with all possible columns
        :param organism:
        :param entries: list of valid entry name. if list is too large (about>200), you need to split the list
        :param nchunk:
        :return: dataframe with indices being the uniprot id (e.g. DIG1_YEAST)

        to do : cleanup the content of the data frame to replace strings
        separated by ; into a list of strings. e.g. the Gene Ontology IDs
        .. warning:: requires pandas library
        """
        if isinstance(entries, str):
            entries = [entries]
        else:
            entries = list(set(entries))
        output = pd.DataFrame()

        nchunk = min(nchunk, len(entries))
        n, rest = divmod(len(entries), nchunk)
        for i in range(0, n + 1):
            this_entries = entries[i * nchunk:(i + 1) * nchunk]
            if len(this_entries):
                query = "+or+".join(this_entries)
                if organism:
                    query += "+and+" + organism
                res = self.search(query, frmt="tab", columns=",".join(self._valid_columns))
            else:
                break
            if len(res) == 0:
                print("\033[0;33m[WARNING]\033[0m some entries %s not found" % entries)
            else:
                df = pd.read_csv(io.StringIO(res), sep="\t")
                if isinstance(output, type(None)):
                    output = df.copy()
                else:
                    output = output.append(df, ignore_index=True)

        output.drop_duplicates(inplace=True)

        columns = ['PubMed ID', 'Comments', u'Domains', 'Protein families', 'Gene names', 'Gene ontology (GO)',
                   'Gene ontology IDs', 'InterPro', 'Interacts with', 'Keywords', 'Subcellular location']
        for col in columns:
            try:
                res = output[col].apply(lambda x: [this.strip() for this in str(x).split(";") if this != "nan"])
                output[col] = res
            except:
                print("\033[0;33m[WARNING]\033[0m column could not be parsed. %s" % col)

        output.Sequence = output['Sequence'].apply(lambda x: x.replace(" ", ""))
        return output
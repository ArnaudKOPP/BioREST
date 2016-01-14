# coding=utf-8
"""
REST class to QuicGo services
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V3.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import logging
from BioREST.Service import REST, check_param_in_list

log = logging.getLogger(__name__)


class QuickGo(REST):
    """
    Interface to the `QuickGO <http://www.ebi.ac.uk/QuickGO/WebServices.html>`_ service
    Retrieve information given a GO identifier:

        import QuickGO
        s = QuickGO()
        res = s.Term("GO:0003824")

    Retrieve information about a protein given its uniprot identifier, a
    taxonomy number. Let us also restrict the search to the UniProt database and
    print only 3 columns of information (protein name, GO identifier and GO
    name)::

        print(s.Annotation(protein="Q8IYB3", frmt="tsv", tax=9606,
            source="UniProt", col="proteinName,goID,goName"))

    Here is the Term output for a given GO identifier::

        print(s.Term("GO:0000016", frmt="obo"))
        [Term]
        id: GO:0000016
        name: lactase activity
        def: "Catalysis of the reaction: lactose + H2O = D-glucose + D-galactose."
        synonym: "lactase-phlorizin hydrolase activity" broad
        synonym: "lactose galactohydrolase activity" exact
        xref: EC:3.2.1.108
        xref: MetaCyc:LACTASE-RXN
        xref: RHEA:10079
        is_a: GO:0004553 ! hydrolase activity, hydrolyzing O-glycosyl compounds


    """
    _valid_col = ['proteinDB', 'proteinID', 'proteinSymbol', 'qualifier', 'goID', 'goName', 'aspect', 'evidence',
                  'ref', 'with', 'proteinTaxon', 'date', 'from', 'splice', 'proteinName', 'proteinSynonym',
                  'proteinType', 'proteinTaxonName', 'originalTermID', 'originalGOName']

    def __init__(self):
        """
        init
        """
        super(QuickGo, self).__init__(url="http://www.ebi.ac.uk/QuickGO", name="quickGO")

    def Term(self, goid, frmt="oboxml"):
        """
        Obtain Term information

        :param goid: go id to retrieve
        :param str frmt: the output format (mini, obo, oboxml).

        The format can be:

        * mini:   Mini HTML, suitable for dynamically embedding in popup boxes.
        * obo:    OBO format snippet.
        * oboxml: OBO XML format snippet.

            import QuickGO
            s = QuickGO()
            s.Term("GO:0003824")


        """
        check_param_in_list(frmt, ["mini", "obo", "oboxml"])
        if goid.startswith("GO:") is False:
            raise ValueError("GO id must start with 'GO:'")

        params = {'id': goid, 'format': frmt}
        res = self.http_get("GTerm", frmt="xml", params=params)

        return res

    def Annotation(self, goid=None, protein=None, frmt="tsv", limit=10000, gz=False, col=None, db=None, aspect=None,
                   termUse=None, evidence=None, source=None, ref=None, tax=9606, qualifier=None):
        """
        Calling the Annotation service
        Mutual exclusive parameters are goid, protein

        :param col: This parameter, which is currently only applicable to the tsv download format, allows you to specify
            a comma-separated list of columns that you want to be included in the returned data set.
            The list below shows the available column names; clicking on the name of a column will take you to the
            description of the column in the QuickGO help file. The default set of columns is shown in bold text.
        :param tax: NCBI taxonomic identifer of annotated protein
        :param protein: Specifies one or more sequence identifiers or accessions from available database(s)
        (see DB filter column)
        :param limit: download limit (number of lines) (default 10,000 rows,
            which may not be sufficient for the data set that you are
            downloading. To bypass this default, and return the entire data set,
            specify a limit of -1).
        :param frmt: one of "gaf", "gene2go", "proteinList", "fasta",
            "tsv" or "dict". The "dict" argument is the default and is a
            python dictionary.
        :param gz: gzips the downloaded file.
        :param goid: GO identifiers either directly or indirectly
            (descendant GO identifiers) applied in annotations.
        :param aspect: use this to limit the annotations returned to a
            specific ontology or ontologies (Molecular Function, Biological
            Process or Cellular Component). The valid character can be F,P,C.
        :param termUse:  if you set this parameter to slim, then QuickGO will
            use the supplied set of GO identifiers as a slim and will map the
            annotations up to these terms. See here for more details:
            http://www.ebi.ac.uk/QuickGO/GMultiTerm
        :param db: protein database (identifier type). Can be UniProtKB, UniGene, Ensembl.
        :param evidence: annotation evidence code category (Ev). Example of
            valid evidence are: be IDA, IC, ISS, IEA, IPI, ND, IMP, ISO, IGI
            should be either a string with comma separated values (e.g.,
            IEA,IDA) or a list of strings (e.g. ["IEA","IDA"]).
        :param source: annotation provider. Examples are 'InterPro', 'UniPathway',
            'MGI', 'FlyBase', 'GOC', 'Source', 'UniProtKB', 'RGD', 'ENSEMBL',
            'ZFIN', 'IntAct'.
        :param ref: PubMed or GO reference supporting annotation. Can refer to a
            specific reference identifier or category (for category level, use
            `*`  after ref type). Can be 'PUBMED:`*`', 'GO_REF:0000002'.
        :param qualifier: tags that modify the interpretation of an annotation.
             Examples are NOT, colocalizes_with, contributes_to.

            * Any number of fields can be specified; they will be AND'ed together.
            * Any number of values can be specified for each field; they will be OR'ed together.
            * Values should be URI encoded.

            print s.Annotation(protein='P12345', frmt='tsv', col="ref,evidence",
            ... ref='PMID:*')
            print s.Annotation(protein='P12345,Q4VCS5', frmt='tsv',
            ...     col="ref,evidence",ref='PMID:,Reactome:')



        """
        _valid_formats = ["gaf", "gpa", "gene2go", "proteinList", "fasta", "tsv"]
        _valid_db = ['UniProtKB', 'UniGene', 'Ensembl']
        _valid_aspect = ['P', 'F', 'C']

        check_param_in_list(frmt, _valid_formats)

        if isinstance(limit, int) is False:
            raise TypeError("limit parameter must be an integer greater than zero")

        # fill params with parameters that have default values.
        params = {'format': frmt, 'limit': limit}

        # beginning of the URL
        url = "GAnnotation?"

        # what is the ID being provided. We can have only one of:
        # protein, goid
        if protein is not None:
            url += "protein=" + protein
        elif goid is not None:
            url += "goid=" + goid
        elif tax is not None:
            url += "tax=" + str(tax)

        # need to check that there are mutualy exclusive
        if goid is None and protein is None and tax is None:
            raise ValueError("you must provide at least one of the following parameter: goid, protein")

        if aspect is not None:
            check_param_in_list(aspect, _valid_aspect)
            params['aspect'] = aspect

        if db is not None:
            check_param_in_list(db, _valid_db)
            params['db'] = db

        if termUse is not None:
            check_param_in_list(termUse, ["slim"])
            params['termUse'] = termUse

        if evidence:
            if isinstance(evidence, list):
                evidence = ",".join([x.strip() for x in evidence])
            elif isinstance(evidence, str):
                pass
            else:
                raise ValueError("Invalid parameter: evidence parameters must be a list of strings ['IDA','IEA'] or a "
                                 "string (e.g., 'IDA', 'IDA,IEA')")
            params['evidence'] = evidence

        if source:
            if isinstance(source, list):
                source = ",".join([x.strip() for x in source])
            elif isinstance(source, str):
                pass
            else:
                raise ValueError("Invalid parameter: source parameters must be a list of strings ['UniProtKB'] or a "
                                 "string (e.g., 'UniProtKB')")
            params['source'] = source

        if ref:
            if isinstance(ref, list):
                ref = ",".join([x.strip() for x in ref])
            elif isinstance(ref, str):
                pass
            else:
                raise ValueError("Invalid parameter: source parameters must be a list of strings ['PUBMED'] or a string "
                                 "(e.g., 'PUBMED:*') ")
            params['ref'] = ref

        if qualifier:
            # NOT, colocalizes_with, contributes_to
            if isinstance(qualifier, list):
                qualifier = ",".join([x.strip() for x in qualifier])
            elif isinstance(qualifier, str):
                pass
            params['qualifier'] = qualifier

        # col parameter
        if frmt == "tsv":
            if col is None:
                col = 'proteinDB,proteinID,proteinSymbol,qualifier,'
                col += 'goID,goName,aspect,evidence,ref,with,proteinTaxon,'
                col += 'date,from,splice,proteinName,proteinSynonym,proteinType,'
                col += 'proteinTaxonName,originalTermID,originalGOName'
            else:
                col = ",".join([x.strip() for x in col.split(",")])

            for c in col.split(','):
                check_param_in_list(c, self._valid_col)
            params["col"] = col

        if frmt not in ["tsv", "dict"]:
            # col is provided but format is not appropriate
            if col is not None:
                raise ValueError("You provided the 'col' parameter but the format is not correct. You should use the "
                                 "frmt='tsv' or frmt='dict' ")

        # gz parameter. do not expect values so need to be added afterwards.
        if gz is True:
            url += '&gz'

        res = self.http_get(url, frmt="txt", params=params)

        return res

    def Annotation_from_goid(self, goid, **kargs):
        """
        Returns a DataFrame containing annotation on a given GO identifier

        :param str goid: a GO identifier
        :return: all outputs are stored into a Pandas.DataFrame data structure.

        All parameters from :math:`Annotation` are also valid except **format** that
        is set to **tsv**  and cols that is made of all possible column names.

        """
        kargs["frmt"] = "tsv"
        cols = ",".join(self._valid_col)
        kargs['col'] = cols

        data = self.Annotation(goid=goid, **kargs)
        data = data.strip().split("\n")[1:]
        res = {}
        for c in cols.split(","):
            res[c] = []

        for entry in data:
            values = entry.split("\t")
            for k, v in zip(cols.split(","), values):
                res[k].append(v)
        try:
            import pandas as pd

            return pd.DataFrame(res)
        except:
            return res

    def Annotation_from_protein(self, protein, **kargs):
        """
        Returns a DataFrame containing annotation on a given protein

        :param str protein: a protein name
        :return: all outputs are stored into a Pandas.DataFrame data structure.

        All parameters from :math:`Annotation` are also valid except **format** that
        is set to **tsv**  and cols that is made of all possible column names.

        """
        kargs["frmt"] = "tsv"
        cols = ",".join(self._valid_col)
        kargs['col'] = cols

        data = self.Annotation(protein=protein, **kargs)
        data = data.strip().split("\n")[1:]
        res = {}
        for c in cols.split(","):
            res[c] = []

        for entry in data:
            values = entry.split("\t")
            for k, v in zip(cols.split(","), values):
                res[k].append(v)
        try:
            import pandas as pd

            return pd.DataFrame(res)
        except:
            return res

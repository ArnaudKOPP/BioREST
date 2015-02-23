# coding=utf-8
"""
Interface to the ArrayExpress web Service.

.. topic:: What is ArrayExpress ?

    :URL: http://www.ebi.ac.uk/arrayexpress/
    :REST: http://www.ebi.ac.uk/arrayexpress/xml/v2/experiments

    .. highlights::

        ArrayExpress is a database of functional genomics experiments that can be queried and the data downloaded. It
        includes gene expression data from microarray and high throughput sequencing studies. Data is collected to
        MIAME and MINSEQE standards. Experiments are submitted directly to ArrayExpress or are imported from the NCBI
        GEO database.

        -- ArrayExpress home page, Jan 2013

accession 	    Experiment primary or secondary accession
array 	        Array design accession or name
ef 	            Experimental factor, the name of the main variable under study in an experiment. E.g. if the factor is
                "sex" in a human study, the researchers would be comparing between male and female samples, and "sex"
                is not merely an  attribute the samples happen to have. Has EFO expansion.
efv 	        The value of an experimental factor. E.g. The values for "genotype" factor can be "wild type genotype",
                "p53-/-". Has EFO expansion.
expdesign 	    Experiment design type, related to the questions being addressed by the study, e.g. "time series design"
                 "stimulus or stress design", "genetic modification design". Has EFO expansion.
exptype 	    Experiment type, related to the assay technology used. Has EFO expansion.
gxa 	        Presence ("true") /absence ("false") of an ArrayExpress experiment in the Expression Atlas.
pmid 	        PubMed identifier
sa 	            Sample attribute values, e.g. "male", "liver". Has EFO expansion.
species 	    Species of the samples. Can use common name (e.g. "mouse") or binomial nomenclature/Latin names (e.g.
                "Mus musculus"). Has EFO expansion.


# ### Array Express REST TEST
    # from BioREST import ArrayExpress
    # ae = ArrayExpress()
    # res = ae.queryExperiments(species="Homo sapiens", ef="organism_part", efv="liver")
    # print(res)
    # res = ae.retrieveExperiment("E-MEXP-31")
    # print(res)

    # res = ae.queryExperiments(array="A-AFFY-33", species="Homo Sapiens", sortby="releasedate")
    # print(res)

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
from BioREST.Service import REST, check_param_in_list

log = logging.getLogger(__name__)


class ArrayExpress(REST):
    """
    Interface to the `ArrayExpress <http://www.ebi.ac.uk/arrayexpress>`_ service

    ArrayExpress allows to retrieve data sets used in various experiments. If
    you know the file and experiment name, you can retrieve a file as follows::

        from ArrayExpress import ArrayExpress
        s = ArrayExpress()
        # retrieve a specific file from a experiment
        res = s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")

    The main issue is that you may not know the experiment you are looking for.
    You can query experiments by keyword::

        # Search for experiments
        res = s.queryExperiments(keywords="cancer+breast", wholewords=True)

    keywords used in queries follows these rules:

    * Accession number and keyword searches are case insensitive
    * More than one keyword can be searched for using the + sign (e.g. keywords="cancer+breast")
    * Use an asterisk as a multiple character wild card (e.g. keywords="colo*")
    * use a question mark ? as a single character wild card (e.g. keywords="te?t")

    More complex queries can be constructed using the operators AND, OR or NOT.
    AND is the default if no operator is specified. Either experiments or
    files can be searched for. Examples are::

        keywords="prostate+AND+breast"
        keywords="prostate+breast"      # same as above
        keywords="prostate+OR+breast"
        keywords="prostate+NOT+breast "

    The returned objects are XML parsed with beautifulSoup. You can get all
    experiments using the getChildren method:

        res = s.queryExperiments(keywords="breast+cancer")
        len(res.getchildren())
        1487

    If you know what you are looking for, you can give the experiment name::

        res = s.retrieveExperiment("E-MEXP-31")
        exp = res.getchildren()[0]   # it contains only one experiment
        [x.text for x in exp.getchildren() if x.tag == "name"]
        ['Transcription profiling of mammalian male germ cells undergoing mitotic
        growth, meiosis and gametogenesis in highly enriched cell populations']

    Using the same example, you can retrieve the names of the files related to
    the experiment::

        files = [x.getchildren() for x in exp.getchildren() if x.tag == "files"]
        [x.get("name") for x in files[0]]
        ['E-MEXP-31.raw.1.zip',
         'E-MEXP-31.processed.1.zip',
         'E-MEXP-31.idf.txt',
         'E-MEXP-31.sdrf.txt']

    Then, you may want to download a particular file::

        s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")

    You can get json file instead of XML by setting the format to "json"::
        a.format = "json"
    """

    def __init__(self):
        """
        init
        """
        super(ArrayExpress, self).__init__(name="ArrayExpress", url="http://www.ebi.ac.uk/arrayexpress")
        self.easyXMLConversion = True
        self._format = "json"
        self.version = "v2"

    def _set_format(self, f):
        check_param_in_list(f, ["json", "xml"])
        self._format = f

    def _get_format(self):
        return self._format

    format = property(_get_format, _set_format, doc="Read/Write access to specify the output format (json or xml)")

    def _search(self, mode, **kargs):
        """
        common function to search for files or experiments
        """
        assert mode in ["experiments", "files"]
        url = "{0}/{1}/{2}".format(self.format, self.version, mode)

        defaults = {
            "accession": None,  # ex: E-MEXP-31
            "keywords": None,
            "species": None,
            "wholewords": "on",
            "expdesign": None,
            "exptype": None,
            "gxa": "true",
            "pmid": None,
            "sa": None,
            "ef": None,  # e.g., CellType
            "efv": None,  # e.g., HeLa
            "array": None,  # ex: A-AFFY-33
            "expandfo": "on",
            "directsub": "true",
            "sortby": ["accession", "name", "assays", "species", "releasedate", "fgem", "raw", "atlas"],
            "sortorder": ["ascending", "descending"],
        }

        for k in kargs.keys():
            check_param_in_list(k, list(defaults.keys()))

        # if len(kargs.keys()):
        # url += "?"
        params = {}

        for k, v in kargs.items():
            if k in ["expandfo", "wholewords"]:
                if v in ["on", True, "true", "TRUE", "True"]:
                    # params.append(k + "=on")
                    params[k] = "on"
            elif k in ["gxa", "directsub"]:
                if v in ["on", True, "true", "TRUE", "True"]:
                    # params.append(k + "=true")
                    params[k] = "true"
                elif v in [False, "false", "False"]:
                    # params.append(k + "=false")
                    params[k] = "false"
                else:
                    raise ValueError("directsub must be true or false")
            else:
                if k in ["sortby", "sortorder"]:
                    check_param_in_list(v, defaults[k])
                # params.append(k + "=" + v)
                params[k] = v

        # NOTE: + is a special character that is replaced by %2B
        # The + character is the proper encoding for a space when quoting
        # GET or POST data. Thus, a literal + character needs to be escaped
        # as well, lest it be decoded to a space on the other end
        for k, v in params.items():
            params[k] = v.replace("+", " ")

        res = self.http_get(url, frmt=self.format, params=params)
        if self.format == "xml":
            res = self.easyXML(res)
        return res

    def queryFiles(self, **kargs):
        """
        Retrieve a list of files associated with a set of experiments
        :param kargs:

            from ArrayExpress import ArrayExpress
            s = ArrayExpress()
            res = s.queryFiles(keywords="cancer+breast", wholewords=True)
            res = s.queryExperiments(array="A-AFFY-33", species="Homo Sapiens")
            res = s.queryExperiments(array="A-AFFY-33", species="Homo Sapiens", sortby="releasedate")
            res = s.queryExperiments(array="A-AFFY-33", species="Homo+Sapiens",
            ...     expdesign="dose response", sortby="releasedate", sortorder="ascending")
            dates = [x.findall("releasedate")[0].text for x in res.getchildren()]

        """
        res = self._search("files", **kargs)
        return res

    def queryExperiments(self, **kargs):
        """
        Retrieve experiments
            res = s.queryExperiments(keywords="cancer+breast", wholewords=True)
        :param kargs:
        """
        res = self._search("experiments", **kargs)
        return res

    def retrieveExperiment(self, experiment):
        """
        alias to queryExperiments if you know the experiment name

            s.retrieveExperiment("E-MEXP-31")
            # equivalent to
            s.queryExperiments(accession="E-MEXP-31")

        :param experiment:
        """
        res = self.queryExperiments(keywords=experiment)
        return res

    def retrieveFile(self, experiment, filename, save=False):
        """
        Retrieve a specific file from an experiment
        :param experiment:
        :param filename:
        :param save:
        :param str filename:
            s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")
        """
        frmt = self.format[:]
        self.format = "xml"
        files = self.retrieveFilesFromExperiment(experiment)
        self.format = frmt[:]

        assert filename in files, """Error. Provided filename does not seem to be correct.
            Files available for %s experiment are %s """ % (experiment, files)

        url = "files/" + experiment + "/" + filename

        if save:
            res = self.http_get(url, frmt="txt")
            f = open(filename, "w")
            f.write(res)
            f.close()
        else:
            res = self.http_get(url, frmt=None)
            return res

    def retrieveFilesFromExperiment(self, experiment):
        """
        Given an experiment, returns the list of files found in its description

        :param str experiment: a valid experiment name
        :return: the experiment files

            from ArrayExpress import ArrayExpress
            s = ArrayExpress(verbose=False)
            s.retrieveFilesFromExperiment("E-MEXP-31")
            ['E-MEXP-31.raw.1.zip', 'E-MEXP-31.processed.1.zip', 'E-MEXP-31.idf.txt', 'E-MEXP-31.sdrf.txt']


        .. warning:: if format is json, filenames cannot be found so you
            must use format set to xml
        """
        assert self.format == "xml", "json format not supported to retrieve the filenames"
        res = self.queryExperiments(keywords=experiment)
        exp = res.getchildren()[0]
        files = [x.getchildren() for x in exp.getchildren() if x.tag == "files"]
        return [x.get("name") for x in files[0]]
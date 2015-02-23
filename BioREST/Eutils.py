# coding=utf-8
"""
Interface to the EUtils web Service.

.. topic:: What is EUtils ?

    :URL: http://www.ncbi.nlm.nih.gov/books/NBK25497/

    .. highlights::

        The Entrez Programming Utilities (E-utilities) are a set of eight server-side programs that provide a stable
        interface into the Entrez query and database system at the National Center for Biotechnology Information (NCBI).
        The E-utilities use a fixed URL syntax that translates a standard set of input parameters into the values
        necessary for various NCBI software components to search for and retrieve the requested data. The E-utilities
        are therefore the structured interface to the Entrez system, which currently includes 38 databases covering a
        variety of biomedical data, including nucleotide and protein sequences, gene records, three-dimensional
        molecular structures, and the biomedical literature.

       -- from http://www.ncbi.nlm.nih.gov/books/NBK25497/, March 2013

# ### Eutils REST TEST
    # from BioREST import EUtils, EUtilsParser
    # eutils = EUtils(email='kopp@igbmc.fr', verbose=True)
    #
    # db = eutils.available_databases
    # print(db)
    #
    # einfo = eutils.EInfo(db='bioproject', retmode='json')
    # import json
    # print(json.dumps(einfo, indent=4, separators=(',', ': ')))
    #
    # einfo = eutils.EInfo(db='protein')
    # print(EUtilsParser(einfo))
    #
    # esearch = eutils.ESearch(db='protein', term='human', retmax=5)
    # print(esearch)

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
import logging
from BioREST.Service import REST, check_param_in_list

log = logging.getLogger(__name__)


class EUtils(REST):
    """
    Interface to NCBI Entrez Utilities <http://eutils.ncbi.nlm.nih.gov/entrez/eutils/> service

    The EUtils class has a method called EFetch so this is actually covering
    all Entrez functionalities.

    .. warning:: Read the `guidelines
        <http://www.ncbi.nlm.nih.gov/books/NBK25497/>`_ before sending requests.
        No more than 3 requests per seconds otherwise your IP may be banned.
        You should provide your email by filling the :attr:`email` so that
        before being banned, you may be contacted.

    """

    def __init__(self, email="unknown"):
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        super(EUtils, self).__init__(url=url, name="EUtils")
        warning = """

        NCBI recommends that users post no more than three URL requests per second.
        Failure to comply with this policy may result in an IP address being blocked
        from accessing NCBI. If NCBI blocks an IP address, service will not be
        restored unless the developers of the software accessing the E-utilities
        register values of the tool and email parameters with NCBI. The value of
        email will be used only to contact developers if NCBI observes requests
        that violate our policies, and we will attempt such contact prior to blocking
        access.  For more details see http://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.chapter2_table1

        This message will not appear if you set the email as a parameter::

            e = EUtils(email="name@adress")

        """
        self.databases = None
        self.tool = "TransCellAssay"
        self.email = email
        if self.email == "unknown":
            log.warning(str(warning))

    def get_databases(self):
        if self.databases is None:
            tmp = self.easyXML(self.http_get(query="einfo.fcgi?", frmt='xml'))
            self.databases = sorted([tag.contents[0] for tag in tmp.soup.find_all('dbname')])
        return self.databases

    available_databases = property(get_databases, doc="Returns list of valid databases")

    def _check_db(self, db):
        if db not in self.databases:
            raise ValueError("You must provide a valid databases from : ", self.databases)

    def _check_retmode(self, retmode):
        if retmode not in ['xml', 'json', 'text']:
            raise ValueError("Unsupported format")

    def _check_ids(self, sid):
        if isinstance(sid, int):
            sid = [sid]
        if isinstance(sid, list):
            sid = ",".join([str(x) for x in sid])
        # If there are commas, let us split, strip spaces and join back the ids
        sid = ",".join([x.strip() for x in sid.split(',') if x.strip() != ""])
        if len(sid.split(",")) > 200:
            raise ValueError("Number of comma separated IDs must be less than 200")
        return sid

    @staticmethod
    def open_query_doc():
        """
        Open in brower documentation for making query
        :return:
        """
        webbrowser.open('http://www.ncbi.nlm.nih.gov/books/NBK25499/')

    def ESearch(self, db, term, retmode='xml', **kwargs):
        """
        Return UIDs that match to request in specific database
        :param retmode:
        :param kwargs:
        :param db:
        :param term:
        :return: return UIDs
        """
        _valid_opt_param = ['usehistory', 'WebEnv', 'query_key', 'retstart', 'retmax', 'rettype', 'sort', 'field',
                            'datatype', 'reldata' 'mindata', 'maxdate']

        params = {'db': db, 'term': term, 'retmode': retmode, 'tool': self.tool, 'email': self.email}
        url = 'esearch.fcgi'
        for key, value in kwargs.items():
            if key in _valid_opt_param:
                params[key] = value
            else:
                print(key + ' Not a valid parameters')
        # TODO make a post call for long query ( several hundred char long)
        if retmode is 'xml':
            res = self.easyXML(self.http_get(url, frmt='xml', params=params))
        else:
            res = self.http_get(url, params=params)
        return res

    def EGQuery(self, term):
        """
        Return UIDs that match to requests in all database
        :param term: Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+'
            signs. For very long queries (more than hundred characters long), consider using HTTP POST call
        :return:
        """
        params = {'term': term, 'tool': self.tool, 'email': self.email}
        url = 'egquery.fcgi'
        res = self.easyXML(self.http_get(url, frmt='xml', params=params))
        return res

    def ESummary(self, db, sid, retmode='xml', **kwargs):
        """
        Return document Summary of list of UIDs
        :param kwargs:
        :param db:
        :param sid:
        :param retmode: xml or json
        :return: Return DocSum
        """
        params = {'db': db, 'id': sid, 'retmode': retmode, 'tool': self.tool, 'email': self.email}
        _valid_opt_param = ['query_key', 'WebEnv', 'retstart', 'retmax']
        url = 'esummary.fcgi'
        self._check_ids(sid)
        self._check_db(db)

        for key, value in kwargs.items():
            if key in _valid_opt_param:
                params[key] = value
        if retmode is 'xml':
            res = self.easyXML(self.http_get(url, frmt='xml', params=params))
        else:
            res = self.http_get(url, params=params)
        return res

    def EInfo(self, db, retmode='xml'):
        """
        Return detailed information about database : indexing fields
        :param db: database to get info
        :param retmode: xml or json
        :return: Return xml doc with field list, use with EutilsParser
        """
        params = {'db': db, 'retmode': retmode, 'tool': self.tool, 'email': self.email}
        self._check_db(db)
        url = "einfo.fcgi"
        if retmode is 'xml':
            res = self.easyXML(self.http_get(url, frmt=retmode, params=params))
        elif retmode is 'json':
            res = self.http_get(url, params=params)
        return res

    def EFetch(self, db, id, retmode='text', **kwargs):
        """
        Return formatted data records for a list of input id
        :param retmode: text, xml not recommended
        :param db: Database from which to retrieve UIDs, must be a valid entrez database
        :param id: UID list, limited to 200
        :param kwargs: rettype, could be fasta, summar
        """
        _valid_opt_param = ['query_key', 'WebEnv', 'retmode', 'rettype', 'retstart', 'retmax', 'strand', 'seq_start',
                            'seq_stop', 'complexity']
        params = {'db': db, 'id': id, 'retmode': retmode, 'tool': self.tool, 'email': self.email}

        url = 'efetch.fcgi'
        for key, value in kwargs.items():
            if key in _valid_opt_param:
                if key is 'strand':
                    check_param_in_list(value, [1, 2])
                    params[key] = value
                else:
                    raise ValueError('Strand must be 0 or 1')
                if key is 'complexity':
                    check_param_in_list(value, [0, 1, 2, 3, 4])
                    params[key] = value
                else:
                    raise ValueError("invalid complexity. must be a number in 0,1,2,3,4")
                params[key] = value
        res = self.http_get(url, frmt=retmode, params=params)
        return res

    def ELink(self, db, dbfrom, cmd, id, **kwargs):
        """
        The entrez links utility, Responds to a list of UIDs in a given database with either a list of
        related UIDs (and relevancy scores) in the same database or a list of linked
        UIDs in another Entrez database; checks for the existence of a specified link
        from a list of one or more UIDs; creates a hyperlink to the primary LinkOut
        provider for a specific UID and database, or lists LinkOut URLs and attributes
        for multiple UIDs.
        :param db:Database from which to retrieve UIDs. The value must be a valid Entrez database
                name. This is the destination database for the link operation.
        :param dbfrom: Database containing the input UIDs. The value must be a
                valid Entrez database name (default = pubmed). This is the origin database of
                the link operation. If db and dbfrom are set to the same database value, then
                ELink will return computational neighbors within that database. Please see the
                full list of Entrez links for available computational neighbors. Computational
                neighbors have linknames that begin with dbname_dbname (examples:
                protein_protein, pcassay_pcassay_activityneighbor).
        :param id: Either a single UID or a comma-delimited list of UIDs may be provided.
                All of the UIDs must be from the database specified by db. Limited to 200 Ids
        :param cmd: ELink command mode. The command mode specified which
                function ELink will perform. Some optional parameters only function for certain
                values of cmd (see http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink).
                Examples are neighbor, prlinks.
        :param kwargs:
        :return:
        """
        _valid_cmd = ['neighbor', 'neighbor_score', 'neighbor_history', 'acheck', 'ncheck', 'lcheck', 'llinks',
                      'llinkslib', 'prlinks']
        _valid_opt_param = ['query_key', 'WebEnv', 'linkname', 'term', 'holding', 'datetype', 'reldate', 'mindata',
                            'maxdata']
        url = 'elink.fcgi'
        params = {'db': db, 'dbfrom': dbfrom, 'id': id, 'tool': self.tool, 'email': self.email}
        if cmd in _valid_cmd:
            params['cmd'] = cmd
        for key, value in kwargs.items():
            if key in _valid_opt_param:
                params[key] = value
        res = self.easyXML(self.http_get(url, frmt='xml', params=params))
        return res

    def ESpell(self, db, term):
        """
        Retrieve spelling suggestions for a text query in a given databse
        :param db: database to search
        :param term: entrez query text, url encoded
        """
        url = 'espell.fcgi'
        params = {'db': db, 'term': term, 'tool': self.tool, 'email': self.email}
        res = self.easyXML(self.http_get(url, frmt='xml', params=params))
        return res

    def EPost(self, db, sid, **kwargs):
        """
        Accepts a list of UIDs from a given database, store the set on the history server, and responds with a query
        key and web env fro the uploaded dataset
        :param db: valid databse
        :param sid: list of string of string
        :param kwargs:
        """
        params = {'db': db, 'id': sid, 'tool': self.tool, 'email': self.email}
        _valid_opt_param = ['query_key', 'WebEnv']
        url = 'epost.fcgi'
        # TODO post call for more than 200 sid long requests
        for key, value in kwargs.items():
            if key in _valid_opt_param:
                params[key] = value
        res = self.easyXML(self.http_get(url, frmt='xml', params=params))
        return res

    def ECitMatch(self, db, bdata, retmode='xml'):
        """
        Retrieve PubMed IDs (PMIDs) that correspond to a set of input citation strings.
        :param db: database to search
        :param retmode: xml
        :param bdata: Citation strings
        """
        url = 'ecitmatch.cgi'
        params = {'db': db, 'bdata': bdata, 'retmode': retmode, 'tool': self.tool, 'email': self.email}
        res = self.easyXML(self.http_get(url, frmt=retmode, params=params))
        return res


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class EUtilsParser(AttrDict):
    """
    Convert xml returned by EUtils into a structure easier to manipulate
    Tested and used for EInfo, for discoving Field for each database
    Does not work for Esummary
    """

    def __init__(self, xml):
        super(EUtilsParser, self).__init__()
        try:
            children = xml.root.getchildren()[0].getchildren()
            self.__name = xml.root.getchildren()[0].tag
        except:
            children = xml.getchildren()

        for i, child in enumerate(children):
            if len(child.getchildren()) == 0:
                self[child.tag] = child.text
            else:
                # This is probably a list then
                self[child.tag] = []
                for subchild in child.getchildren():
                    self[child.tag].append(EUtilsParser(subchild))

    def __str__(self):
        name = self._EUtilsParser__name
        if name == "DbInfo":
            txt = ""
            for this in self.FieldList:
                txt += "{0:10}:  {1}\n".format(this.Name, this.Description)
            return txt
        else:
            print("Not implemented for {0}".format(name))
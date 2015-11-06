# coding=utf-8
"""
Interface to HGNC web service
REST : http://www.genenames.org/help/rest-web-service-help

"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

from BioREST.Service import REST, RestServiceError
import logging

log = logging.getLogger(__name__)


class HGNC(REST):
    """
    Wrapper to the genenames web service
    See details at http://www.genenames.org/help/rest-web-service-help
    """
    def __init__(self):
        url = "http://rest.genenames.org"
        super(HGNC, self).__init__("HGNC", url=url)
        self._info = self.info
        self._searchableFields = self._info['searchableFields']
        self._storedFields = self._info['storedFields']

    @property
    def info(self):
        query = 'info'
        header = self.get_headers(content='json')
        res = self.http_get(query=query, headers=header)
        return res

    def fetch(self, storedfield, term):
        """
        Fetch data
        :param storedfield:
        :param term:
        :return: :raise RestServiceError:
        """
        if storedfield not in self._storedFields:
            raise RestServiceError('StoredFields not valid')
        query = 'fetch/{0}/{1}'.format(storedfield, term)
        header = self.get_headers(content='json')
        res = self.http_get(query=query, headers=header)
        return res

    def search(self, searchablefields, term):
        """
        Search a searchable field (database) for a pattern

        The search request is more powerful than fetch for querying the
        database, but search will only returns the fields hgnc_id, symbol and
        score. This is because this tool is mainly intended to query the server
        to find possible entries of interest or to check data (such as your own
        symbols) rather than to fetch information about the genes. If you want
        to retrieve all the data for a set of genes from the search result, the
        user could use the hgnc_id returned by search to then fire off a fetch
        request by hgnc_id.

        :param searchablefields:
        :param term:
        :return: :raise RestServiceError:
        ::

            # Search all searchable fields for the tern BRAF
            h.search('BRAF')

            # Return all records that have symbols that start with ZNF
            h.search('symbol', 'ZNF*')

            # Return all records that have symbols that start with ZNF
            # followed by one and only one character (e.g. ZNF3)
            # Nov 2015 does not work neither here nor in within in the
            # official documentation
            h.search('symbol', 'ZNF?')

            # search for symbols starting with ZNF that have been approved
            # by HGNC
            h.search('symbol', 'ZNF*+AND+status:Approved')

            # return ZNF3 and ZNF12
            h.search('symbol', 'ZNF3+OR+ZNF12')

            # Return all records that have symbols that start with ZNF which
            # are not approved (ie entry withdrawn)
            h.search('symbol', 'ZNF*+NOT+status:Approved')
        """
        if searchablefields not in self._searchableFields:
            raise RestServiceError('SearchableFields not valid')
        query = 'seach/{0}/{1}'.format(storedfield, term)
        header = self.get_headers(content='json')
        res = self.http_get(query=query, headers=header)
        return res

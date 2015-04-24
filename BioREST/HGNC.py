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
    Interface to the `HGNC <http://www.genenames.org>`_ service
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
        query = 'fetch/'+str(storedfield)+'/'+str(term)
        header = self.get_headers(content='json')
        res = self.http_get(query=query, headers=header)
        return res

    def search(self, searchablefields, term):
        """
        Search data
        :param searchablefields:
        :param term:
        :return: :raise RestServiceError:
        """
        if searchablefields not in self._searchableFields:
            raise RestServiceError('SearchableFields not valid')
        query = 'seach/'+str(searchablefields)+'/'+str(term)
        header = self.get_headers(content='json')
        res = self.http_get(query=query, headers=header)
        return res

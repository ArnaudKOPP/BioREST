# coding=utf-8
"""
Encore REST services
REST Documentation : https://www.encodeproject.org/help/rest-api/

# ### Encode REST TEST
    # BioREST import Encode
    # encode = Encode()
    # response = encode.biosample('ENCBS000AAA')
    # encode.show_response(response)

"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V3.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import json
import logging
from BioREST.Service import REST

log = logging.getLogger(__name__)


class Encode(REST):
    """
    Class for doing REST requests to Encode
    """
    def __init__(self):
        super(Encode, self).__init__(name="Encode", url="https://www.encodeproject.org/")
        # Force return from the server in JSON format
        self.HEADERS = {'accept': 'application/json'}

    def biosample(self, accession_number):
        """
        Get biosample with accession number like ENCBS000AAA
        :param accession_number:
        :return: json object
        """
        url = "biosample/" + accession_number
        params = {'frame': 'object'}
        response = self.http_get(url, params=params, headers=self.HEADERS)
        return response

    @staticmethod
    def response_keys(response, first_level=True):
        """
        Get all keys from response
        :param response: reponse object from request
        :param first_level: only first level or with sublevel
        :return: list of keys
        """
        if first_level:
            keys = response.keys()
        else:
            keys = [key for key, value in response.iteritems()]
        return keys

    @staticmethod
    def show_response(response):
        """
        Print the response in pretty format
        :param response:
        :return:
        """
        print(json.dumps(response, indent=4, separators=(',', ': ')))

    def search(self, searchterm, embedded=False, **kwargs):
        """
        Make a search in Encode database
        :param searchterm:
        :param embedded:
        :param kwargs:
        :return: :raise ValueError:
        """
        __valid_params = ['file_format', 'experiment', 'dataset', 'type', 'md5sum']
        __valid_search_type = ['file', 'replicate', 'biosample']

        if embedded:
            params = {'searchTerm': searchterm, 'frame': 'embedded', 'format': 'json'}
        else:
            params = {'searchTerm': searchterm, 'frame': 'object', 'format': 'json'}
        url = "search/"

        for key, value in kwargs.items():
            if key in __valid_params:
                if key is 'type':
                    if value in __valid_search_type:
                        params[key] = value
                    else:
                        raise ValueError('Not valid type')
                else:
                    params[key] = value

        response = self.http_get(url, params=params, headers=self.HEADERS)
        return response

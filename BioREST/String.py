# coding=utf-8
"""
String-db REST services
Website : www.http://string-db.org
REST Documentation : http://string-db.org/help/index.jsp?topic=/org.string-db.docs/api.html

# ### String REST TEST
    # from TransCellAssay.IO.Rest.String import String
    # string = String(identity='kopp@igbmc.fr')

"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import webbrowser
import logging
from BioREST.Service import REST

log = logging.getLogger(__name__)


class String(REST):
    """
    Class for doing REST requests to String-db
    """

    def __init__(self, identity,  alternative_db=False, sister_db=False):
        self._identity = identity
        if alternative_db and sister_db:
            raise ValueError('Choose one DB')
        if alternative_db and not sister_db:
            super(String, self).__init__(name="String", url="http://string.embl.de/")
        if sister_db and not alternative_db:
            super(String, self).__init__(name="String", url="http://stitch.embl.de/")
        if not alternative_db and not sister_db:
            super(String, self).__init__(name="String", url="http://string-db.org/")

    @staticmethod
    def print_doc_requests():
        """
        print doc
        """
        webbrowser.open(url='http://string-db.org/help/index.jsp?topic=/org.string-db.docs/api.html')
        print('''
                database	    Description
                -------------------------------------------------
                string-db.org	Main entry point of STRING
                string.embl.de 	Alternative entry point of STRING
                stitch.embl.de 	The sister database of STRING

                List of requests
                -------------------------------------------------------------------------------------------------------
                resolve	            List of items that match (in name or identifier) the query item
                abstracts	        List of abstracts that contain the query item
                interactors	        List of interaction partners for the query item
                actions	            Action partners for the query item
                interactions	    Interaction network in PSI-MI 2.5 format (xml format)
                network	            The network image for the query item


                List of parameters and values
                -------------------------------------------------------------------------------------------------------
                identifier	                required parameter for single item, e.g. DRD1_HUMAN
                format	                    For resolve requests: only-ids get the list of only the STRING identifiers
                                                (full by default) For abstract requests: use colon pmids for alternative
                                                shapes of the pubmed identifier
                species	                    Taxon identifiers (e.g. Human 9606, see: http://www.uniprot.org/taxonomy)
                limit	                    Maximum number of nodes to return, e.g 10.
                required_score	T           Threshold of significance to include a interaction, a number between 0 & 1000
                additional_network_nodes	Number of additional nodes in network (ordered by score), e.g./ 10
                network_flavor	            The style of edges in the network. evidence for colored multilines.
                                                confidence for singled lines where hue correspond to confidence score.
                                                value = evidence, confidence, actions
                caller_identity	            Your identifier for us.
        ''')

    @staticmethod
    def __get_indentifiers_param(identifier):
        params = {'identifier': str(identifier)}
        return params

    def resolve(self, identifier, **kwargs):
        """
        List of items that match query items
        :param identifier:
        :param kwargs:
        :return: :raise ValueError:
        """
        __valid_param = ['species', 'format']
        __valid_frmt = ['full', 'only_ids']

        query = 'api/json/resolve'

        params = self.__get_indentifiers_param(identifier)
        params['caller_identity'] = self._identity

        for key, value in kwargs.items():
            if key in __valid_param:
                if key is 'format':
                    if value in __valid_frmt:
                        params[key] = value
                    else:
                        raise ValueError('additional_network_nodes error value, must be :', __valid_frmt)
                else:
                    params[key] = value
        res = self.http_get(query, frmt="txt", params=params)

        return res

    def abstracts(self, identifier, **kwargs):
        """
        List of abstract that contain the query items
        :param identifier:
        :param kwargs:
        :return: :raise ValueError:
        """
        __valid_param = ['format', 'limit']
        __valid_frmt = ['colon', 'pmids']

        query = 'api/tsv/abstracts'

        params = self.__get_indentifiers_param(identifier)
        params['caller_identity'] = self._identity

        for key, value in kwargs.items():
            if key in __valid_param:
                if key is 'format':
                    if value in __valid_frmt:
                        params[key] = value
                    else:
                        raise ValueError('additional_network_nodes error value, must be :', __valid_frmt)
                else:
                    params[key] = value
        res = self.http_get(query, frmt="txt", params=params)

        return res

    def actions(self, identifier, **kwargs):
        """
        Actions partners the query items
        :param identifier:
        :param kwargs:
        :return: :raise ValueError:
        """
        __valid_param = ['limit', 'required_score', 'additional_network_nodes']
        __valide_netw_fl = ['evidence', 'confidence', 'actions']

        query = 'api/tsv/actions'

        params = self.__get_indentifiers_param(identifier)
        params['caller_identity'] = self._identity

        for key, value in kwargs.items():
            if key in __valid_param:
                if key is 'additional_network_nodes':
                    if value in __valide_netw_fl:
                        params[key] = value
                    else:
                        raise ValueError('additional_network_nodes error value, must be :', __valide_netw_fl)
                else:
                    params[key] = value
        res = self.http_get(query, frmt="txt", params=params)

        return res

    def interactors(self, identifier, format='psi-mi', **kwargs):
        """
        List of interaction partners for the query items
        :param identifier:
        :param kwargs:
        :param format: psi-mi or psi-mi-tab
        :return: :raise ValueError:
        """
        __valid_param = ['limit', 'required_score', 'additional_network_nodes']
        __valid_netw_fl = ['evidence', 'confidence', 'actions']
        __valid_frmt = ['psi-mi', 'psi-mi-tab']

        query = 'api/'+str(format)+'/interactors'

        params = self.__get_indentifiers_param(identifier)
        params['caller_identity'] = self._identity

        for key, value in kwargs.items():
            if key in __valid_param:
                if key is 'additional_network_nodes':
                    if value in __valid_netw_fl:
                        params[key] = value
                    else:
                        raise ValueError('additional_network_nodes error value, must be :', __valid_netw_fl)
                else:
                    params[key] = value
        res = self.http_get(query, frmt="xml", params=params)

        return res

    def interactions(self, identifier, format='psi-mi', **kwargs):
        """
        Interaction network
        :param identifier:
        :param kwargs:
        :param format: psi-mi or psi-mi-tab
        :return: :raise ValueError:
        """
        __valid_param = ['limit', 'required_score', 'additional_network_nodes']
        __valid_netw_fl = ['evidence', 'confidence', 'actions']
        __valid_frmt = ['psi-mi', 'psi-mi-tab']

        query = 'api/'+str(format)+'/interactions'

        params = self.__get_indentifiers_param(identifier)
        params['caller_identity'] = self._identity

        for key, value in kwargs.items():
            if key in __valid_param:
                if key is 'additional_network_nodes':
                    if value in __valid_netw_fl:
                        params[key] = value
                    else:
                        raise ValueError('additional_network_nodes error value, must be :', __valid_netw_fl)
                else:
                    params[key] = value

        res = self.http_get(query, frmt="xml", params=params)

        return res

    def network(self, identifier, file,  **kwargs):
        """
        Network image for the query items
        :param identifier:
        :param file:
        :param kwargs:
        :raise ValueError:
        """
        __valid_param = ['limit', 'required_score', 'additional_network_nodes']
        __valide_netw_fl = ['evidence', 'confidence', 'actions']

        query = 'api/image/network'

        params = self.__get_indentifiers_param(identifier)
        params['caller_identity'] = self._identity

        for key, value in kwargs.items():
            if key in __valid_param:
                if key is 'additional_network_nodes':
                    if value in __valide_netw_fl:
                        params[key] = value
                    else:
                        raise ValueError('additional_network_nodes error value, must be :', __valide_netw_fl)
                else:
                    params[key] = value

        res = self.http_get(query, frmt="txt", params=params)

        # TODO don't work
        try:
            log.info('Writing image :{}'.format(file))
            f = open(file, "wb")
            f.write(res)
            f.close()
        except:
            pass
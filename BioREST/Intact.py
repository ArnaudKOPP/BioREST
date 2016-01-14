# coding=utf-8
"""
REST class for intact db
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


class Intact(REST):
    """
    Interface to the `Intact <http://www.ebi.ac.uk/intact/>`_ service

        import Intact
        u = Intact()

    """

    _url = "http://www.ebi.ac.uk/intact/complex-ws"

    def __init__(self):
        """
        **Constructor** Intact
        """
        super(Intact, self).__init__(name="Intact", url=Intact._url)

    def search(self, query, frmt='json', facets=None, number=None, filters=None):
        """
        Search for a complex inside intact complex.

        :param query: the query (e.g., ndc80)
        :param frmt: Defaults to json (could be a Pandas data frame if
            Pandas is installed; set frmt to 'pandas')
        :param facets: lists of facets as a string (separated by comma)
        :param number:
        :param filters: list of filters.


            s = Intact()
            # search for ndc80
            s.search('ncd80')

            #  Search for ndc80 and facet with the species field:
            s.search('ncd80', facets='species_f')

            # Search for ndc80 and facet with the species and biological role fields:
            s.search('ndc80', facets='species_f,pbiorole_f')

            # Search for ndc80, facet with the species and biological role
            # fields and filter the species using human:
            s.search('Ndc80', first=0, number=10,
                filters='species_f:("Homo sapiens")',
                facets='species_f,ptype_f,pbiorole_f')

            # Search for ndc80, facet with the species and biological role
            # fields and filter the species using human or mouse:
            s.search('Ndc80, first=0, number=10,
                filters='species_f:("Homo sapiens" "Mus musculus")',
                facets='species_f,ptype_f,pbiorole_f')

            # Search with a wildcard to retrieve all the information:
            s.search('*')

            # Search with a wildcard to retrieve all the information and facet
            # with the species, biological role and interactor type fields:
            s.search('*', facets='species_f,pbiorole_f,ptype_f')

            # Search with a wildcard to retrieve all the information, facet with
            # the species, biological role and interactor type fields and filter
            # the interactor type using small molecule:
            s.search('*', facets='species_f,pbiorole_f,ptype_f',
                filters='ptype_f:("small molecule")'

            # Search with a wildcard to retrieve all the information, facet with
            # the species, biological role and interactor type fields and filter
            # the interactor type using small molecule and the species using human:
            s.search('*', facets='species_f,pbiorole_f,ptype_f',
                filters='ptype_f:("small molecule"),species_f:("Homo sapiens")')

            # Search for GO:0016491 and paginate (first is for the offset and number
            # is how many do you want):
            s.search('GO:0016491', first=10, number=10)
        """
        check_param_in_list(frmt, ['pandas', 'json'])

        # note that code format to be json, which is the only option so
        # we can use pandas as a frmt without addition code.
        params = {'format': 'json', 'facets': facets, 'first': None, 'number': number, 'filters': filters}

        result = self.http_get('search/' + query, frmt="json", params=params)

        # if isinstance(result, int):
        #    raise ValueError("Got a number from Intact request. Check validity of the arguments ")

        if frmt == 'pandas':
            import pandas as pd
            df = pd.DataFrame(result['elements'])
            return df
        else:
            return result

    def details(self, query):
        """Return details about a complex

        :param str query: EBI-1163476

        """
        result = self.http_get('details/' + query, frmt="json")
        return result

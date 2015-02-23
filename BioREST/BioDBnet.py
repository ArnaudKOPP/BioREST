# coding=utf-8
"""
http://biodbnet.abcc.ncifcrf.gov/webServices/RestWebService.php
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
from BioREST.Service import REST

log = logging.getLogger(__name__)


class BioDBnet(REST):
    """
    BioDBnet rest service
    """

    def __init__(self, frmt='json'):
        """
        **Constructor** bioDbnet
        :param frmt: json or xml
        """
        if frmt is 'json':
            __url = "http://biodbnet.abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json"
        else:
            __url = "http://biodbnet.abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi"

        super(BioDBnet, self).__init__(name="BioDBnet", url=__url)

    def getInputs(self):
        """
        Gets all the input nodes in bioDBnet
        :return:
        """
        params = {'method': 'getinputs'}
        res = self.http_get(query='', params=params)
        return res

    def getOutputsForInput(self, input):
        """
        Gets all the possible output nodes for a given input node
        :param input: retrieve output for this input
        :return:
        """
        params = {'method': 'getoutputsforinput', 'input': str(input)}
        res = self.http_get(query='', params=params)
        return res

    def getDirectOutptsForInput(self, input):
        """
        Gets all the direct output nodes for a given input node
        :param input:
        :return:
        """
        params = {'method': 'getdirectoutputsforinput', 'input': str(input), 'directOuput': '1'}
        res = self.http_get(query='', params=params)
        return res

    def getPathways(self, database=None, taxId=9606):
        """
        Call for getting all available pathways in bioDBnet
        :param database: search in specific db
        :param taxId: ncbi taxon if
        :return:
        """
        params = {'method': 'getpathways', 'taxonId': str(taxId)}
        if database is None:
            params['pathways'] = '1'
        else:
            params['pathways'] = str(database)
        res = self.http_get(query='', params=params)
        return res

    def db2db(self, input, inputvalues, outputs, taxonId='9606', format='row'):
        """
        db2db allows for conversions of identifiers from one database to other database identifiers or annotations.
        :param input: input type
        :param inputvalues: input value, str with , as sep
        :param outputs: output type
        :param taxonId: ncbi taxon id
        :param format: row or col
        :return:
        """
        params = {'method': 'db2db',
                  'input': str(input),
                  'inputValues': str(inputvalues),
                  'outputs': str(outputs),
                  'taxonId': str(taxonId),
                  'format': str(format)}
        res = self.http_get(query='', params=params)
        return res

    def dbReport(self, input, inputvalues, taxonId='9606', format='row'):
        """
        dbReport reports all the database identifiers and annotations that it can find for a particular type of input.
        :param input: input type
        :param inputvalues: input value, str with , as sep
        :param taxonId: ncbi taxon id
        :param format: row or col
        :return:
        """
        params = {'method': 'dbreport',
                  'input': str(input),
                  'inputValues': str(inputvalues),
                  'taxonId': str(taxonId),
                  'format': str(format)}
        res = self.http_get(query='', params=params)
        return res

    def dbWalk(self, inputvalues, dbPath, taxonId='9606', format='row'):
        """
        dbWalk is a form of database to database conversion where the user has complete control on the path to follow
        while doing the conversion.
        :param inputvalues: input value, str with , as sep
        :param dbPath:
        :param taxonId: ncbi taxon id
        :param format: row or col
        :return:
        """
        params = {'method': 'dbwalk',
                  'inputValues': str(inputvalues),
                  'dbPath': str(dbPath),
                  'taxonId': str(taxonId),
                  'format': str(format)}
        res = self.http_get(query='', params=params)
        return res

    def dbFind(self, inputvalues, outputs, format='row'):
        """
        dbFind can be used when you do not know the actual type of your identifiers or when you have a mixture of
         different types of identifiers.
        :param inputvalues:
        :param outputs:
        :param format:
        :return:
        """
        params = {'method': 'dbfind',
                  'inputValues': str(inputvalues),
                  'outputs': str(outputs),
                  'format': str(format)}
        res = self.http_get(query='', params=params)
        return res

    def dbOrtho(self, input, inputvalues, intaxon, outtaxon, outputs, format='row'):
        """
        dbOrtho helps users run ortholog conversions where one identifier from one species can be converted to an
        identifier in a different species.
        :param input:
        :param inputvalues:
        :param intaxon:
        :param outtaxon:
        :param outputs:
        :param format:
        :return:
        """
        params = {'method': 'dbortho',
                  'input': str(input),
                  'inputValues': str(inputvalues),
                  'intaxon': str(intaxon),
                  'outtaxon': str(outtaxon),
                  'outputs': str(outputs),
                  'format': str(format)}
        res = self.http_get(query='', params=params)
        return res

    def dbAnnot(self, inputvalues, annotations, taxonId='9060', format='row'):
        """
        dbAnnot allows for easy annotations of biological identifiers. The categories listed are grouped based on
        function.
        :param inputvalues:
        :param annotations:
        :param taxonId:
        :param format:
        :return:
        """
        __valid_annot = ['Genes', 'Drugs', 'Diseases', 'GO Terms', 'Pathways']
        if annotations not in __valid_annot:
            raise ValueError('Choose valid annotations')
        params = {'method': 'dbannot',
                  'inputValues': str(inputvalues),
                  'taxonId': str(taxonId),
                  'format': str(format)}
        res = self.http_get(query='', params=params)
        return res
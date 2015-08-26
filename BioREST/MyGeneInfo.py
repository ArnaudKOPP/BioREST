# coding=utf-8
"""
http://docs.mygene.info/en/latest/index.html
"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import logging
from BioREST.Service import REST, list2string, check_param_in_list

log = logging.getLogger(__name__)

class MyGeneInfo(REST):

    _url = "http://mygene.info/v2"

    def __init__(self):
        super(BioCyc, self).__init__(name="MyGeneInfo", url=MyGeneInfo._url)


    def GeneQuery(self):
        raise NotImplementedError

    def GeneAnnotation(self):
        raise NotImplementedError

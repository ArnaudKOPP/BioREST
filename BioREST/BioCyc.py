# coding=utf-8
"""
http://biocyc.org/web-services.shtml
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import logging
from BioREST.Service import REST

log = logging.getLogger(__name__)


class BioCyc(REST):
    def __init__(self):
        super(BioCyc, self).__init__(name="BioCyc", url="http://websvc.biocyc.org/")

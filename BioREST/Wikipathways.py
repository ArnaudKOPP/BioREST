# coding=utf-8
"""
http://www.wikipathways.org/index.php/Help:WikiPathways_Webservice/API
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

class WikiPathways(REST):

    _url = "http://webservice.wikipathways.org/"

    def __init__(self):
        super(BioCyc, self).__init__(name="WikiPathways", url=WikiPathways._url)

    def listOrganisms(self):
        raise NotImplementedError

    def listPathways(self):
        raise NotImplementedError

    def getPathway(self):
        raise NotImplementedError

    def getPathwayInfo(self):
        raise NotImplementedError

    def getPathwayHistory(self):
        raise NotImplementedError

    def getRecentChanges(self):
        raise NotImplementedError

    def login(self):
        raise NotImplementedError

    def getPathwayAs(self):
        raise NotImplementedError

    def updatePathway(self):
        raise NotImplementedError

    def createPathways(self):
        raise NotImplementedError

    def findPathwaysByText(self):
        raise NotImplementedError

    def findPathwaysByXref(self):
        raise NotImplementedError

    def findInteractions(self):
        raise NotImplementedError

    def saveCurationTag(self):
        raise NotImplementedError

    def removeCurationTag(self):
        raise NotImplementedError

    def getCurationTags(self):
        raise NotImplementedError

    def getCurationTagsByName(self):
        raise NotImplementedError

    def getColoredPathway(self):
        raise NotImplementedError

    def getXrefList(self):
        raise NotImplementedError

    def findPathwaysByLiterature(self):
        raise NotImplementedError

    def saveOntologyTag(self):
        raise NotImplementedError

    def removeOntologyTag(self):
        raise NotImplementedError

    def getPathwayByOntologyTerm(self):
        raise NotImplementedError

    def getPathwayByParentOntologyTerm(self):
        raise NotImplementedError

    def getUserByOrcid(self):
        raise NotImplementedError

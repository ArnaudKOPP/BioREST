# coding=utf-8
"""
This module provides a class :class:`~BioModels` that allows an easy access
to all the BioModel service.


.. topic:: What is BioMart ?

    :URL: http://www.biomart.org/
    :REST: http://www.biomart.org/martservice.html
           http://www.biomart.org/other/biomart_0.9_0_documentation.pdf

    .. highlights::

        The BioMart project provides free software and data services to the
        international scientific community in order to foster scientific collaboration
        and facilitate the scientific discovery process. The project adheres to the open
        source philosophy that promotes collaboration and code reuse.

        -- from BioMart March 2013

# ### Biomart REST TEST
    # from TransCellAssay.IO.Rest.Biomart import BioMart
    # s = BioMart(verbose=True)
    # portal = s.registry()
    # print(json.dumps(portal, indent=4, separators=(',', ':')))
    # res, marts = s.available_marts()
    # marts = json.dumps(marts, indent=4, separators=(',', ':'))
    # print(marts)
    #
    # res, dataset = s.datasets_for_marts('gene_ensembl_config')
    # datasets = json.dumps(dataset, indent=4, separators=(',', ':'))
    # print(datasets)
    #
    # res, attribut = s.attributs_for_datasets(datasets='hsapiens_gene_ensembl', config='gene_ensembl_config')
    # attribut = json.dumps(attribut, indent=4, separators=(',', ':'))
    # print(attribut)
    #
    # res, filter = s.filter_for_datasets(datasets='hsapiens_gene_ensembl', config='gene_ensembl_config')
    # filter = json.dumps(filter, indent=4, separators=(',', ':'))
    # print(filter)

"""
__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import logging
from BioREST.Service import REST

log = logging.getLogger(__name__)


class BioMart(REST):
    """
    Interface to the `BioMart <http://www.biomart.org>`_ service
    V0.9 implemented
    note:: the biomart sevice is slow so please be patient...
    """

    def __init__(self):
        """
        By default, the URL used for the biomart service is::
            http://central.biomart.org
        Server are frequenlty down and slow
        """
        url = "http://central.biomart.org"
        super(BioMart, self).__init__("BioMart", url=url)
        self.marts_lst = None

    def registry(self, frmt='json'):
        """
        Return the root GUI container containing all child Containers and associated marts
        :param frmt: json or xml
        :return:
        """
        query = "martservice/portal"
        res = self.http_get(query, frmt=frmt, headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def available_marts(self, frmt='json'):
        """
        Return available marts
        :param frmt: json or xml
        :return:
        """
        query = "martservice/marts"
        res = self.http_get(query, frmt=frmt, headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            import json
            marts = json.dumps(res, indent=4, separators=(',', ':'))
            marts = json.loads(marts)
            self.marts_lst = [marts[i]['name'] for i in range(len(marts))]
            return res, self.marts_lst

    def datasets_for_marts(self, config, frmt='json'):
        """
        Lists all Datasets for the given Mart
        :param config: name of config as returned by the mart object
        :param frmt: json or xml
        :return:
        """
        query = 'martservice/datasets'
        res = self.http_get(query, frmt=frmt, params={'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            import json
            marts = json.dumps(res, indent=4, separators=(',', ':'))
            marts = json.loads(marts)
            return res, [marts[i]['name'] for i in range(len(marts))]

    def filter_for_datasets(self, datasets, config, frmt='json'):
        """
        Lists all filter for the given dataset(s) of a given marts
        :param datasets: Comma-separated string of datasets
        :param config: name of config as returned bu the mart object
        :param frmt: json or xml
        :return:
        """
        query = 'martservice/filters'
        res = self.http_get(query, frmt=frmt, params={'datasets': str(datasets), 'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            import json
            filter = json.dumps(res, indent=4, separators=(',', ':'))
            filter = json.loads(filter)
            return res, [filter[i]['name'] for i in range(len(filter))]

    def attributs_for_datasets(self, datasets, config, frmt='json'):
        """
        List all attributes for the given dataset(s) of a given marts
        :param datasets: Comma-separated string of datasets
        :param config: name of config as returned bu the mart object
        :param frmt: json or xml
        :return:
        """
        query = 'martservice/attributes'
        res = self.http_get(query, frmt=frmt, params={'datasets': str(datasets), 'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            import json
            attr = json.dumps(res, indent=4, separators=(',', ':'))
            attr = json.loads(attr)
            return res, [attr[i]['name'] for i in range(len(attr))]

    def container_for_marts(self, datasets, config, frmt='json'):
        """
        Lists all containers for the given Mart, starting from the root Container
        :param datasets: Comma-separated string of datasets
        :param config: name of config as returned bu the mart object
        :param frmt: json or xml
        :return:
        """
        query = "martservice/containers"
        res = self.http_get(query, params={'datasets': str(datasets), 'config': str(config)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def linkable_datasets(self, datasets, frmt='json'):
        """
        List all the datasets that can be linked with selected datasets
        :param frmt: json or xml
        :param datasets: comma-separated string of datasets
        :return:
        """
        query = "martservice/linkables"
        res = self.http_get(query, params={'datasets': str(datasets)},
                            headers={'Accept': self.content_types[frmt]})
        if frmt is 'xml':
            return self.easyXML(res)
        else:
            return res

    def querying(self, xmlq):
        """
        Post a query xml
        :param xmlq: the xml query


        Query xml must be formatted like that:

        <Query client="" processor="TSV" limit="1000" header="1">
            <Dataset name="hsapiens_gene_ensembl_hopkinsBreast3" config="hsapiens_gene_ensembl">
                <Filter name="biotype" value="miRNA"/>
                <Attribute name="ensembl_gene_id"/>
                <Attribute name="cancertype"/>
                <Attribute name="description"/>
                <Attribute name="start_position"/>
                <Attribute name="end_position"/>
            </Dataset>
        </Query>

        """
        query = "martservices/results"
        ret = self.http_post(query, frmt=None, data={'query': xmlq.strip()}, headers={})
        return ret


class BioMartQuery(object):
    """
    Class for creating xml query
    client = name of client makin call
    processor = TSV or CSV (format of return type)
    limit = -1 for no limit, number of row returned
    header = if set to 1 then first row of result will be column headers
    """
    def __init__(self, client="", processor='TSV', limit=1000, header=1):
        self.header = '<Query client="{}" processor="{}" limit="{}" header="{}">\n'.format(client, processor, limit,
                                                                                           header)
        self.footer = "    </Dataset>\n</Query>"
        self.dataset = None
        self.attributes = []
        self.filters = []
        self.reset()

    def add_filter(self, name, value):
        """
        Add filter in query xml
        :param name: name of filter
        :param value: value
        """
        self.filters.append('       <Filter name="{}" value="{}"/>\n'.format(name, value))

    def add_attribute(self, attribute):
        """
        Add attribut in query xml
        :param attribute:
        """
        self.attributes.append('        <Attribute name="{}"/>\n'.format(attribute))

    def add_dataset_config(self, dataset, config):
        """
        Set dataset
        :param config:
        :param dataset:
        """
        self.dataset = '        <Dataset name="{}" config="{}">\n'.format(dataset, config)

    def reset(self):
        """
        Reset all value
        """
        self.attributes = []
        self.filters = []
        self.dataset = None

    def get_xml(self):
        """
        Return the xml query
        :return: :raise ValueError:
        """
        if self.dataset is None:
            raise ValueError("data set must be set.")
        xml = self.header
        xml += self.dataset
        for line in self.filters:
            xml += line
        for line in self.attributes:
            xml += line
        xml += self.footer
        return xml
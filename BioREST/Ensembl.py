# coding=utf-8
"""
Interface to Ensembl web service

.. topic:: What is Ensembl ?

    :URL: http://www.ensembl.org/
    :URL: https://github.com/Ensembl/ensembl-rest/wiki/Output-formats

    REST : http://rest.ensemblgenomes.org/

    .. highlights::

        The Ensembl project produces genome databases for vertebrates and
        other eukaryotic species, and makes this information freely available
        online.

        -- From Ensembl web site, Oct 2014

# ### Ensembl REST TEST
    # from BioREST import Ensembl
    # s = Ensembl(verbose=True)
    # print(s.get_info_rest())
    # print(s.get_info_ping())
    # print(s.get_info_software())
    # print(s.get_info_species())
    # print(s.get_archive("AT3G52430"))
    # print(s.post_archive(["AT3G52430", "AT1G01160"]))
    # print(s.get_gene_family_information_by_id('MF_01687'))
    # print(s.get_info_analysis('arabidopsis_thaliana'))
    # print(s.get_info_assembly('arabidopsis_thaliana'))
    # print(s.get_info_assembly_by_region('arabidopsis_thaliana', region=1))
    # print(s.get_info_compara_methods())

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
from BioREST.Service import REST, check_param_in_list, tolist, to_json

log = logging.getLogger(__name__)


class Ensembl(REST):
    """
    Interface to the Ensembl service

    The API was copied from the Ensemble API (http://rest.ensemblgenomes.org/)
    REST API in V4.0 used here

    For post requests, max size is 1000

    """

    def __init__(self, requests_per_sec=15):
        """
        INIT REST object for ensembl

        :param verbose: set to False to prevent informative messages
        :param requests_per_sec: number of requests per sec (max)
        """
        super(Ensembl, self).__init__(name="Ensembl", url='http://rest.ensemblgenomes.org')
        self._request_per_sec = requests_per_sec
        self.callback = None  # use in all methods

    @staticmethod
    def __check_frmt(frmt, values=[]):
        check_param_in_list(frmt, ['json', 'jsonp'] + values)

    @staticmethod
    def __check_id(identifier):
        pass

    @staticmethod
    def __nh_format_to_frmt(value):
        """

        :param value:
        :return:
        """
        if value == 'phylip':
            return 'phyloxml'
        elif value == 'simple':
            return 'nh'
        else:
            return 'json'

    @staticmethod
    def __check_sequence(value):
        """

        :param value:
        """
        check_param_in_list(value, ['none', 'cdna', 'protein'])

    @staticmethod
    def __check_nh_format(value):
        """

        :param value:
        """
        check_param_in_list(value, ['full', 'display_label_composite', 'simple', 'species', 'species_short_name',
                                    'ncbi_taxon', 'ncbi_name', 'njtree', 'phylip'])

    # ARCHIVE
    # ---------------------------------------------------------------------
    def get_archive(self, identifier, frmt='json'):
        """
        Uses the given identifier to return the archived sequence

        :param identifier: An Ensembl stable ID
        :param frmt: output formart(json, xml or jsonp)

            s = Ensembl()
            res = s.get_archive("AT3G52430")

        """
        self.__check_frmt(frmt, ['xml'])
        self.__check_id(identifier)
        res = self.http_get("archive/id/" + identifier, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})

        if frmt == 'xml':
            res = self.easyXML(res)
        return res

    def post_archive(self, identifiers, frmt='json'):
        """
        Retrieve the archived sequence for a set of identifiers

        :param identifiers: An Ensembl stable ID in format ["XXX", "XXXX"]
        :param frmt: output formart(json, xml or jsonp)

        """
        self.__check_frmt(frmt, ['xml'])
        identifiers = tolist(identifiers)
        res = self.http_post("archive/id/", frmt=frmt,
                             headers=self.get_headers(content=frmt),
                             data=to_json({'id': identifiers}),
                             params={'callback': self.callback})
        return res

    # COMPARATIVE GENOMICS
    # ------------------------------------------------------------------
    def get_gene_family_by_id(self, identifier, compara='multi', frmt='json'):
        """
        Retrieve gene family information by ID

        :param identifier: MF_01687
        :param compara: default=bacteria
        :param frmt: json, jsonp, xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("family/id/" + identifier, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'compara': str(compara), 'callback': self.callback})
        if frmt == 'xml':
            res = self.easyXML(res)
        return res

    def get_gene_family_by_member(self, identifier, compara='multi', frmt='json'):
        """
        Retrive gene family to which a gene belongs

        :param identifier: b0344
        :param compara: default=bacteria
        :param frmt: json, jsonp, xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("family/member/id/" + identifier, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'compara': str(compara), 'callback': self.callback})
        if frmt == 'xml':
            res = self.easyXML(res)
        return res

    def get_gene_family_by_symbol(self, species, identifier, compara='multi', frmt='json'):
        """
        Retrive gene family to which a gene belongs

        :param species: species symbol escherichia_coli_str_k_12_substr_mg1655
        :param identifier: lacZ
        :param compara: default=bacteria
        :param frmt: json, jsonp, xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("family/member/symbol"+str(species)+"/" + identifier, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'compara': str(compara), 'callback': self.callback})
        if frmt == 'xml':
            res = self.easyXML(res)
        return res

    def get_genetree_by_id(self, identifier, aligned=False, frmt='json', nh_format='simple', sequence='protein'):
        """
        Retrieves a gene tree dump for a gene tree stable identifier

        :param identifier: An Ensembl genetree ID
        :param frmt: response formats: json, jsonp, nh, phyloxml
        :param bool aligned: if true, return the aligned string otherwise, i
            return the original
            sequence (no insertions). Can be True/1 or False/0 and defaults to 0
        :param nh_format: The format of a NH (New Hampshire) request.
            Valid values are 'full', 'display_label_composite', 'simple',
            'species', 'species_short_name', 'ncbi_taxon', 'ncbi_name',
            'njtree', 'phylip'
        :param sequence: The type of sequence to bring back. Setting it to none
            results in no sequence being returned.
            Valid values are 'none', 'cdna', 'protein'.

            s = Ensembl()
            s.get_genetree('ENSGT00390000003602', frmt='nh', nh_format='simple')
            s.get_genetree('ENSGT00390000003602', frmt='phyloxml')
            s.get_genetree('ENSGT00390000003602', frmt='phyloxml',aligned=True, sequence='cdna')
            s.get_genetree('ENSGT00390000003602', frmt='phyloxml', sequence='none')
        """
        self.__check_frmt(frmt, ['nh', 'phyloxml'])
        self.__check_nh_format(nh_format)
        aligned = int(aligned)
        self.__check_sequence(sequence)
        res = self.http_get("genetree/id/" + identifier, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'nh_format': nh_format, 'sequence': sequence,
                                    'aligned': aligned})
        return res

    def get_genetree_by_member_id(self, species, identifier, frmt='json', aligned=False, db_type='core',
                                  nh_format='simple', sequence='protein', compara='multi'):
        """
        Retrieves a gene tree containing the gene identified by a symbol

        :param identifier: Ensembl stable ID
        :param frmt: format of data default = json
        :param aligned: Return the aligned string if true. Otherwise, return the original sequence (no insertions)
        :param nh_format: The format of a NH (New Hampshire) request.
        :param sequence: type of sequence to bring back
        :param species: species name or alias
        :param compara: Name of the compara database to use. Multiple
            comparas can exist on a server if you are accessing Ensembl
            Genomes data. Defautl to 'multi'
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core. Defaults
            to core

            get_genetree_by_member_id('ENSG00000157764', frmt='phyloxml')

        """
        self.__check_frmt(frmt, ['nh', 'phyloxml'])
        self.__check_frmt(frmt)
        self.__check_nh_format(nh_format)
        frmt = self.__nh_format_to_frmt(nh_format)
        self.__check_sequence(sequence)

        res = self.http_get("genetree/member/id/" + identifier, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'nh_format': nh_format, 'sequence': sequence,
                                    'aligned': int(aligned), 'compara': compara,
                                    'db_type': db_type, 'species': species})
        return res

    def get_genetree_by_member_symbol(self, species, symbol, frmt='json', aligned=False, db_type='core',
                                      nh_format='simple', sequence='protein', compara='multi'):
        """
        Retrieves a gene tree containing the gene identified by a symbol

        :param species: Species name/alias
        :param symbol: symbol o display name of gene
        :param frmt: frmt of data
        :param aligned: Return the aligned string if true. Otherwise, return the original sequence (no insertions)
        :param db_type: Restrict the search to a database other than the default. Useful if you need to use a DB other
                        than core
        :param nh_format: The format of a NH (New Hampshire) request.
        :param sequence: The type of sequence to bring back. Setting it to none results in no sequence being returned
        :param compara: Name of the compara database to use. Multiple comparas can exist on a server if you are
                        accessing Ensembl Genomes data
        """
        self.__check_frmt(frmt, ['nh', 'phyloxml'])
        frmt = self.__nh_format_to_frmt(nh_format)
        self.__check_sequence(sequence)
        self.__check_nh_format(nh_format)

        res = self.http_get("genetree/member/symbol/%s/%s" % (species, symbol),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'nh_format': nh_format, 'sequence': sequence,
                                    'aligned': int(aligned), 'compara': compara,
                                    'db_type': db_type})
        return res

    def get_alignment_by_region(self, region, species, frmt='json', aligned=True, compact=True, compara='multi',
                                display_species_set=None, mask=None, method='EPO', species_set=None,
                                species_set_group='mammals'):
        """
        Retrieves genomic alignments as separate blocks based on a region and
        species

        :param region: Query region. A maximum of 10Mb is allowed to be
            requested at any one time (e.g.,  'X:1000000..1000100:1',
            'X:1000000..1000100:-1',  'X:1000000..1000100')
        :param species: Species name/alias (e.g., human)
        :param frmt: format of return data
        :param bool aligned: Return the aligned string if true. Otherwise,
            return the original sequence (no insertions)
        :param bool compact: Applicable to EPO_LOW_COVERAGE alignments.
            If true, concatenate the low coverage species sequences
            together to create a single sequence. Otherwise, separates
            out all sequences.
        :param compara: Name of the compara database to use. Multiple
            comparas can exist on a server if you are accessing Ensembl
            Genomes data (defaults to multi)
        :param display_species_set: Subset of species in the alignment
            to be displayed (multiple values). All the species in the alignment
            will be displayed if this is not set. Any valid alias may be
            used.. (e.g., human, chimp, gorilla)
        :param mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters.
        :param method:The alignment method amongst Enum(EPO,
            EPO_LOW_COVERAGE, PECAN, LASTZ_NET, BLASTZ_NET, TRANSLATED_BLAT_NET)
        :param species_set: the set of species used to define the pairwise
            alignment (multiple values). Should not be used with the
            species_set_group parameter. Use :meth:`get_info_compara_by_method`
            with one of the methods listed above to obtain a valid list of
            species sets. Any valid alias may be used. (e.g., musc_musculus,
            homo_sapiens)
        :param species_set_group: The species set group name of the multiple
            alignment. Should not be used with the species_set parameter.
            Use /info/compara/species_sets/:method with one of the methods
            listed above to obtain a valid list of group names. (Defaults to
            mammals. e.g. mammals, amniotes, fish, sauropsids)

        """
        check_param_in_list(method, ['EPO', 'EPO_LOW_COVERAGE', 'PECAN', 'LASTZ_NET', 'BLASTZ_NET',
                                     'TRANSLATED_BLAT_NET'])
        check_param_in_list(mask, ['hard', 'soft'])
        self.__check_frmt(frmt, ['xml', 'phyloxml'])
        res = self.http_get("alignment/region/{0}/{1}".format(species, region),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'aligned': int(aligned), 'callback': self.callback,
                                    'compact': compact, 'compara': compara,
                                    'display_species_set': display_species_set,
                                    'mask': mask, 'method': method, 'species_set': species_set,
                                    'species_set_group': species_set_group})
        return res

    def get_homology_by_id(self, identifier, frmt='json', aligned=True, compara='multi', format='full', sequence=None,
                           species=None, target_species=None, target_taxon=None, type='all'):
        """
        Retrieve homology information (orthologs) by Ensembl gene ID

        :param identifier: An Ensembl stable ID
        :param frmt: format of return data
        :param aligned: Return the aligned string if true. Otherwise, return the original sequence (no insertions)
        :param compara: Name of the compara database to use. Multiple comparas can exist on a server if you are
                        accessing Ensembl Genomes data
        :param format: Layout of the response
        :param sequence: The type of sequence to bring back. Setting it to none results in no sequence being returned
        :param species: Species name/alias
        :param target_species: Filter by species. Supports all species aliases
        :param target_taxon:  	Filter by taxon
        :param type: The type of homology to return from this call. Projections are orthology calls defined between
        alternative assemblies and the genes shared between them. Useful if you need only one type of homology back
        from the service

        """
        check_param_in_list(format, ['full', 'condensed'])
        check_param_in_list(type, ['orthologues', 'paralogues', 'projections', 'all'])
        self.__check_sequence(sequence)
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("homology/id/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'aligned': int(aligned), 'callback': self.callback,
                                    'compara': compara, 'format': format, 'sequence': sequence,
                                    'species': species,
                                    'target_species': target_species, 'target_taxon': target_taxon,
                                    'type': type})
        return res

    def get_homology_by_symbol(self, species, symbol, frmt='json', aligned=True, compara=None, format='full',
                               sequence=None, target_species=None, target_taxon=None, type='all'):
        """
        Retrive homology information by symbol

        :param species: Species name/alias
        :param symbol: Symbol or display name of a gene
        :param frmt: format of return data
        :param aligned: Return the aligned string if true. Otherwise, return the original sequence (no insertions)
        :param compara: Name of the compara database to use. Multiple comparas can exist on a server if you are
                        accessing Ensembl Genomes data
        :param format: Layout of the response
        :param sequence: The type of sequence to bring back. Setting it to none results in no sequence being returned
        :param target_species: Filter by species. Supports all species aliases
        :param target_taxon:  	Filter by taxon
        :param type: The type of homology to return from this call. Projections are orthology calls defined between
        alternative assemblies and the genes shared between them. Useful if you need only one type of homology back
        from the service

        """
        check_param_in_list(format, ['full', 'condensed'])
        check_param_in_list(type, ['orthologues', 'paralogues', 'projections', 'all'])
        self.__check_sequence(sequence)
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("homology/{0}/{1}".format(species, symbol),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'aligned': int(aligned), 'callback': self.callback,
                                    'compara': compara, 'format': format, 'sequence': sequence,
                                    'target_species': target_species, 'target_taxon': target_taxon,
                                    'type': type})
        return res

    # CROSS REFERENCES
    # -------------------------------

    def get_xrefs_by_id(self, identifier, frmt='json', all_levels=False, db_type='core', external_db=None,
                        object_type=None, species=None):
        """
        Perform lookups of Ensembl Identifiers and retrieve their external
        references in other databases

        :param identifier: An Ensembl Stable ID (ENSG00000157764)
        :param frmt: response formats: json, jsonp, nh, phyloxml
        :param bool all_levels: Set to find all genetic features linked to
            the stable ID, and fetch all external references for them.
            Specifying this on a gene will also return values from its
            transcripts and translations.
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core
        :param external_db: Filter by external database (e.g., HGNC)
        :param object_type: filter by feature type (e.g., gene, transcript)
        :param species: Species name/alias (human)

        """
        self.__check_frmt(frmt)
        res = self.http_get('xrefs/id/{0}'.format(identifier), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'db_type': db_type, 'callback': self.callback, 'all_levels': int(all_levels),
                                    'external_db': external_db, 'object_type': object_type, 'species': species})
        return res

    def get_xrefs_by_name(self, name, species, frmt='json', db_type='core', external_db=None):
        """
        Performs a lookup based upon the primary accession or display label
        of an external reference and returning the information we hold about the
        entry

        :param name: Symbol or display name of a gene (e.g., BRCA2)
        :param species: Species name/alias (e.g., human)
        :param frmt: response formats: json, jsonp,xml
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core
        :param external_db: Filter by external database (e.g., HGNC)


        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('xrefs/name/{0}/{1}'.format(species, name), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'db_type': db_type, 'callback': self.callback,
                                    'external_db': external_db})
        return res

    def get_xrefs_by_symbol(self, symbol, species, frmt='json', db_type='core', external_db=None, object_type=None):
        """
        Looks up an external symbol and returns all Ensembl objects linked to
        it. This can be a display name for a gene/transcript/translation, a
        synonym or an externally linked reference. If a gene's transcript is
        linked to the supplied symbol the service will return both gene and
        transcript (it supports transient links).

        :param species: Species name/alias (e.g., human)
        :param symbol: Symbol or display name of a gene (BRCA2)
        :param frmt: response formats: json, jsonp,xml
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core
        :param external_db: Filter by external database (e.g., HGNC)
        :param object_type: filter by feature type (e.g., gene, transcript)

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('xrefs/symbol/{0}/{1}'.format(species, symbol), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'db_type': db_type, 'callback': self.callback,
                                    'object_type': object_type, 'external_db': external_db}
                            )
        return res

    # INFORMATION
    # ---------------------------------------------------------------------------

    def get_info_analysis(self, species, frmt='json'):
        """
        List the names of analyses involved in generating Ensembl data.

        :param species: Species name/alias (e.g., homo_sapiens)
        :param frmt: response formats: json, jsonp,xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/analysis/{0}'.format(species), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_assembly(self, species, frmt='json', bands=False):
        """
        List the currently available assemblies for a species.

        :param species: Species name/alias (e.g., homo_sapiens)
        :param frmt: response formats: json, jsonp,xml
        :param bool bands: if set to 1, include karyotype band information.
            Only display if band information is available

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/assembly/{0}'.format(species), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'bands': bands, 'callback': self.callback})
        return res

    def get_info_assembly_by_region(self, species, region, frmt='json', bands=0):
        """
        Returns information about the specified toplevel sequence region for the
        given species.

        :param species: Species name
        :param region: The (top level) sequence region name
        :param frmt: format of return data
        :param bands: If set to 1, include karyotype band information. Only display if band information is available

        """

        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/assembly/{0}/{1}'.format(species, region),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'bands': bands, 'callback': self.callback})
        return res

    def get_info_biotypes(self, species, frmt='json'):
        """
        List the functional classifications of gene models that Ensembl associates
        with a particular species. Useful for restricting the type of genes/transcripts
        retrieved by other endpoints.

        :param species: Species name/alias (e.g., homo_sapiens)
        :param frmt: response formats: json, jsonp,xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/biotypes/{0}'.format(species), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_compara_methods(self, frmt='json'):
        """
        List all compara analyses available (an analysis defines the type of
        comparative data).

        :param frmt: response formats: json, yaml, jsonp, xml
        """
        res = self.http_get('info/compara/methods', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_compara_by_method(self, method, frmt='json', compara='multi'):
        """
        List all collections of species analysed with the specified compara
        method.

        :param method: Filter by compara method. Use one the
            methods returned by /info/compara/methods endpoint.
            e.g., EPO
        :param frmt: response formats: json, jsonp,xml
        :param compara: Name of the compara database to use. Multiple
            comparas may exist on a server when accessing Ensembl Genomes data.
            defaults to 'multi'

        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get('info/compara/species_sets/{0}'.format(method),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'compara': compara, 'callback': self.callback})
        return res

    def get_info_comparas(self, frmt='json'):
        """
        Lists all available comparative genomics databases and their data release.

        :param frmt: response formats: json, jsonp,xml
        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get('info/comparas/', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_data(self, frmt='json'):
        """
        Shows the data releases available on this REST server. May return more than
        one release (unfrequent non-standard Ensembl configuration).

        :param frmt: response formats: json, jsonp,xml


        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/data', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_eg_info(self, frmt='json'):
        """
        Returns the Ensembl Genomes version of the databases backing this service

        :param frmt:

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/eg_version', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_external_db_for_specie(self, species, filter=None, frmt='json'):
        """
        Lists all available external sources for a species.

        :param species: Species name/alias
        :param filter: Restrict external DB serach to a single source or pattern
        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/external_dbs/{0}'.format(species),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'filter': str(filter), 'callback': self.callback})
        return res

    def get_info_divisions(self, frmt='json'):
        """
        Get list of all Ensembl divisions for which information is available

        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/divisions', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_about_genome(self, name, expand=None, frmt='json'):
        """
        Find information about a given genome

        :param name: The production name of the genome
        :param expand: Expands the information to include details of sequence. Can be very large
        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/genomes/{}'.format(name), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'expand': expand, 'callback': self.callback})
        return res

    def get_genomes(self, expand=None, frmt='json'):
        """
        Find information about all genomes. Response may be very large

        :param expand: Expands the information to include details of sequence. Can be very large
        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/genomes', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'expand': expand, 'callback': self.callback})
        return res

    def get_genomes_by_accession(self, division, expand=None, frmt='json'):
        """
        Find information about genomes containing a specified INSDC accession

        :param division: INSDC sequence accession (optionally versioned)
        :param expand: Expands the information to include details of sequences. Can be very large.
        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/genomes/accession/{}'.format(division), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'expand': expand, 'callback': self.callback})
        return res

    def get_genome_by_assembly(self, division, expand=None, frmt='json'):
        """
        Find information about a genome with a specified assembly

        :param division: INSDC assembly ID (optionally versioned)
        :param expand: Expands the information to include details of sequences. Can be very large.
        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/genomes/assembly/{}'.format(division), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'expand': expand, 'callback': self.callback})
        return res

    def get_genome_by_division(self, division, expand=None, frmt='json'):
        """
        Find information about all genomes in a given division. May be large for Ensembl Bacteria

        :param division: INSDC assembly ID (optionally versioned)
        :param expand: Expands the information to include details of sequences. Can be very large.
        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/genomes/division/{}'.format(division), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'expand': expand, 'callback': self.callback})
        return res

    def get_genome_by_taxonomy(self, division, expand=None, frmt='json'):
        """
        Find information about all genomes beneath a given node of the taxonomy

        :param division: INSDC assembly ID (optionally versioned)
        :param expand: Expands the information to include details of sequences. Can be very large.
        :param frmt: data return format

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/genomes/taxonomy/{}'.format(division), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'expand': expand, 'callback': self.callback})
        return res

    def get_info_ping(self, frmt='json'):
        """
        Checks if the service is alive.

        :param frmt:

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/ping', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res['ping']

    def get_info_rest(self, frmt='json'):
        """
        Shows the current version of the Ensembl REST API.

        :param frmt: response formats: json, jsonp,xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/rest', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_software(self, frmt='json'):
        """
        Shows the current version of the Ensembl API used by the REST server.

        :param frmt: response formats: json, jsonp,xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/software', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_info_species(self, filter=None, frmt='json'):
        """
        Lists all available species, their aliases, available adaptor groups and data
        release.

        :param filter: Filter by Ensembl or Ensembl Genomes division
        :param frmt: response formats: json, jsonp,xml

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('info/species', frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'filter': filter, 'callback': self.callback})
        return res

    # LOOKUP
    # -------------------------------------------------------------------
    def get_lookup_by_id(self, identifier, frmt='json', db_type=None, expand=False, format='full', species=None):
        """
        Find the species and database for a single identifier

        :param identifier: An Ensembl stable ID
        :param frmt: response formats in json, xml, jsonp
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core. Defaults
            to core
        :param expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param format: Specify the formats to emit from this endpoint, full or condensed
        :param species: Species name/alias (e.g., human)
            get_lookup_by_id('ENSG00000157764', expand=True)

        """
        check_param_in_list(format, ['full', 'condensed'])
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("lookup/id/" + identifier, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'db_type': db_type, 'expand': int(expand), 'format': format,
                                    'callback': self.callback, 'species': species})
        return res

    def get_lookup_by_genome_name(self, name, frmt='json', biotypes='all', level='gene', xrefs=False):
        """
        Find the species and database for a single identifier

        :param name: An Ensembl stable ID
        :param frmt: response formats in json, xml, jsonp
        :param biotypes: Biotypes of genes to retrieve
        :param level: Level of object to retrieve
        :param xrefs: Include cross-reference

        """
        check_param_in_list(level, ['gene', 'transcript', 'translation', 'protein_feature'])
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("lookup/genome/" + name, frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'biotypes': biotypes, 'level': level, 'xrefs': xrefs})
        return res

    def post_lookup_by_id(self, identifiers, frmt='json', db_type=None, expand=False, format='full', species=None):
        """
        Find the species and database for a single identifier

        :param identifiers: An ontology term identifier (e.g., GO:0005667) or ["AT3G52430", "AT1G01160" ]
        :param frmt: response formats in json, xml, jsonp
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core. Defaults
            to core
        :param expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param format: Specify the formats to emit from this endpoint
        :param species: Species name/alias (e.g., human)
            post_lookup_by_id(["ENSG00000157764", "ENSG00000248378" ])

        """
        self.__check_frmt(frmt)
        identifiers = tolist(identifiers)
        expand = int(expand)
        res = self.http_post("lookup/id/", frmt=frmt,
                             headers=self.get_headers(content=frmt),
                             data=to_json({'ids': identifiers}),
                             params={'db_type': db_type, 'expand': expand, 'format': format,
                                     'callback': self.callback, 'species': species})
        return res

    def get_lookup_by_symbol(self, species, symbol, frmt='json', expand=False, format='full'):
        """
        Find the species and database for a single identifier

        :param species: Species name/alias (e.g., human)
        :param symbol: A name or symbol from an annotation source has been
            linked to a genetic feature. e.g., BRCA2
        :param frmt: response formats in json, xml, jsonp
        :param expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param format: Specify the formats to emit from this endpoint
            get_lookup_by_symbol('homo_sapiens', 'BRCA2', expand=True)

        """
        check_param_in_list(format, ['full', 'condensed'])
        self.__check_frmt(frmt, ['xml'])
        expand = int(expand)
        res = self.http_get("lookup/symbol/{0}/{1}".format(species, symbol),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'format': format,
                                    'callback': self.callback, 'expand': expand})
        return res

    def post_lookup_by_symbol(self, species, symbols, frmt='json', expand=False, format='full'):
        """
        Find the species and database for a set of symbols

        :param species: Species name/alias (e.g., human)
        :param list symbols: A list of names or symbols from an annotation source has been
            linked to a genetic feature. e.g., BRCA2
        :param frmt: response formats in json, xml, jsonp
        :param expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param format: Specify the formats to emit from this endpoint
            post_lookup_by_symbol('homo_sapiens', ['BRCA2', 'BRAF'], expand=True)

        """
        check_param_in_list(format, ['full', 'condensed'])
        self.__check_frmt(frmt, ['xml'])
        symbols = tolist(symbols)
        expand = int(expand)
        res = self.http_post("lookup/symbol/{0}".format(species),
                             frmt=frmt,
                             headers=self.get_headers(content=frmt),
                             data=to_json({'symbols': symbols}),
                             params={'format': format,
                                     'callback': self.callback, 'expand': expand})
        return res

    # MAPPING
    # --------------------------------------------------------------------

    def get_map_cds_to_region(self, identifier, region, frmt='json', species=None):
        """
        Convert from cDNA coordinates to genomic coordinates.

        :param identifier: Ensembl ID e.g. ENST00000288602
        :param region: Query region e.g., 100..300
        :param species: Species Name/alias
        :param frmt: data return format
        Output reflects forward orientation coordinates as returned from the Ensembl API.
            get_map_cds_to_region('ENST00000288602', '1..1000')

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("map/cds/{0}/{1}".format(identifier, region),
                            frmt=frmt, headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'species': species})

        return res

    def get_map_cdna_to_region(self, identifier, region, frmt='json', species=None):
        """
        Convert from cDNA coordinates to genomic coordinates.

        :param frmt: data return format
        :param identifier: An Ensembl stable ID
        :param region:  query region (see example)
        :param species: default to human
        Output reflects forward orientation coordinates as returned from the Ensembl API.

            get_map_cdna_to_region('ENST00000288602', '100..300')

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("map/cdna/{0}/{1}".format(identifier, region),
                            frmt=frmt, headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'species': species})
        return res

    def get_map_assembly_one_to_two(self, first, second, region, species='human', frmt='json'):
        """
        Convert the co-ordinates of one assembly to another

        :param first: version of the input assembly
        :param second: version of the output assembly
        :param region:  query region (see example)
        :param species: default to human
        :param frmt: data return format
            e.get_map_assembly_one_to_two(species='human',
                first='GRCh37', region='X:1000000..1000100:1', second='GRCh38')

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("map/{0}/{1}/{2}/{3}".format(species, first, region, second),
                            frmt=frmt, headers=self.get_headers(content=frmt),
                            params={})
        return res

    def get_map_translation_to_region(self, identifier, region, specie=None, frmt='json'):
        """
        Convert from protein (translation) coordinates to genomic coordinates.
        Output reflects forward orientation coordinates as returned from the
        Ensembl API.

        :type frmt: data return format
        :param region: Query region
        :param identifier: a stable Ensembl ID
        :param specie: Specie name/alias

            get_map_translation_to_region('ENSP00000288602', '100..300')
        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("map/translation/{0}/{1}".format(identifier, region),
                            frmt=frmt, headers=self.get_headers(content=frmt),
                            params={'species': specie, 'callback': self.callback})
        return res

    # ONTOLOGY and Taxonomy
    # -------------------------------------------------------------------------

    def get_ontology_ancestors_by_id(self, identifier, frmt='json', ontology=None):
        """
        Reconstruct the entire ancestry of a term from is_a and part_of
        relationships

        :param identifier: An ontology term identifier (e.g., GO:0005667)
        :param frmt: json, xml, yaml, jsonp
        :param ontology: Filter by ontology. Used to disambiguate
            terms which are shared between ontologies such as GO and EFO (e.g.,
            GO)
        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("ontology/ancestors/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'ontology': ontology})
        return res

    def get_ontology_ancestors_chart_by_id(self, identifier, frmt='json', ontology=None):
        """
        Reconstruct the entire ancestry of a term from is_a and part_of
        relationships.

        :param identifier: an ontology term identifier (GO:0005667)
        :param frmt: json, xml, yaml, jsonp
        :param ontology: Filter by ontology. Used to disambiguate
            terms which are shared between ontologies such as GO and EFO

        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("ontology/ancestors/chart/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'ontology': ontology})
        return res

    def get_ontology_descendants_by_id(self, identifier, frmt='json', closest_term=None, ontology=None, subset=None,
                                       zero_distance=None):
        """
        Find all the terms descended from a given term. By default searches
        are conducted within the namespace of the given identifier

        :param identifier: an ontology term identifier (GO:0005667)
        :param frmt: json, xml, jsonp
        :param bool closest_term: If true return only the closest terms to the
            specified term
        :param ontology: Filter by ontology. Used to disambiguate terms
            which are shared between ontologies such as GO and EFO
        :param subset: Filter terms by the specified subset
        :param bool zero_distance: Return terms with a distance of 0

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("ontology/descendants/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'ontology': ontology,
                                    'closest_term': closest_term, 'subset': subset,
                                    'zero_distance': zero_distance})
        return res

    def get_ontology_by_id(self, identifier, frmt='json', relation=None, simple=False):
        """
        Search for an ontological  term by its namespaced identifier

        :param identifier: An ontology term identifier (e.g., GO:0005667)
        :param bool simple: If set the API will avoid the fetching of parent and child terms
        :param frmt: response formats in json, xml, yaml, jsonp
        :param simple: If set the API will avoid the fetching of parent and child terms
        :param relation: The types of relationships to include in the output. Fetches
            all relations by default (e.g., is_a, part_of)

            e = Ensembl()
            res = e.get_ontology('GO:0005667')

        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        identifier = str(identifier)
        res = self.http_get("ontology/id/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'simple': int(simple), 'relation': relation,
                                    'callback': self.callback})
        return res

    def get_ontology_by_name(self, name, frmt='json', ontology=None, relation=None, simple=False):
        """
        Search for a list of ontological terms by their name

        :param name: An ontology name. SQL wildcards are supported (e.g.,
            transcription factor complex)
        :param frmt: response formats in json, xml, yaml, jsonp
        :param simple: If set the API will avoid the fetching of parent and child terms
        :param relation: The types of relationships to include in the output. Fetches
            all relations by default (e.g., is_a, part_of)
        :param ontology: Filter by ontology. Used to disambiguate terms which are
            shared between ontologies such as GO and EFO (e.g., GO)

            e = Ensembl()
            res = e.get_ontology_by_name('transcription factor')
            400
            res = e.get_ontology_by_name('transcription factor complex')
            res[0]['children']

        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("ontology/name/{0}".format(name), frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'simple': int(simple), 'relation': relation,
                                    'callback': self.callback, 'ontology': ontology})
        return res

    def get_taxonomy_classification_by_id(self, identifier, frmt='json'):
        """
        Return the taxonomic classification of a taxon node

        :param identifier: A taxon identifier. Can be a NCBI taxon id or a name
            (e.g., 9606, Homo sapiens)
        :param frmt: json, xml, yaml, jsonp

            e = Ensembl()
            res = e.get_taxonomy_classification_by_id('9606')

        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("taxonomy/classification/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback})
        return res

    def get_taxonomy_by_id(self, identifier, frmt='json', simple=False):
        """
        Search for a taxonomic term by its identifier or name

        :param identifier: A taxon identifier. Can be a NCBI taxon id or
            a name (e.g., 9606 or Homo sapiens)
        :param bool simple: If set the API will avoid the fetching of parent and child terms
        :param frmt: response formats in json, xml, yaml, jsonp
        """
        self.__check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("taxonomy/id/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'simple': int(simple)})
        return res

    # OVERLAP
    # -----------------------------------------------------
    def get_overlap_by_id(self, identifier, feature='gene', frmt='json', biotype=None, db_type=None, logic_name=None,
                          misc_set=None, object_type=None, so_term=None, species=None, species_set='mammals'):
        """
        Retrieves features (e.g. genes, transcripts, variations etc.)
        that overlap a region defined by the given identifier.

        :param identifier: An Ensemble stable ID
        :param feature: The type of feature to retrieve. Multiple values
            are accepted. Value in Enum(gene, transcript, cds, exon, repeat,
            simple, misc, variation, somatic_variation, structural_variation,
            somatic_structural_variation, constrained, regulatory
        :param frmt: data return format
        :param biotype: The functional classification of the gene or
            transcript to fetch. Cannot be used in conjunction with logic_name
            when querying transcripts. (e.g., protein_coding)
        :param db_type: Restrict the search to a database other than
            the default. Useful if you need to use a DB other than core
        :param logic_name: Limit retrieval of genes, transcripts and
            exons by a given name of an analysis.
        :param misc_set: Miscellaneous set which groups together
            feature entries. Consult the DB or returned data sets to discover
            what is available. (e.g., cloneset_30k
        :param object_type: Filter by feature type (e.g., gene)
        :param so_term: Sequence Ontology term to narrow down the
            possible variations returned. (e.g., SO:0001650)
        :param species: Species name/alias.
        :param species_set: Filter by species set for
            retrieving constrained elements. (e.g. mammals)

        """
        check_param_in_list(feature, ['gene', 'transcript', 'cds', 'exon', 'repeat', 'simple', 'misc', 'variation',
                                      'somatic_variation', 'structural_variation', 'somatic_structural_variation',
                                      'constrained', 'regulatory', 'segmentation', 'motif', 'chipseq', 'array_probe'])
        self.__check_frmt(frmt, ['xml', 'gff3', 'bed'])
        res = self.http_get("overlap/id/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'biotype': biotype,
                                    'db_type': db_type, 'logic_name': logic_name,
                                    'misc_set': misc_set, 'object_type': object_type,
                                    'so_term': so_term, 'species': species, 'feature': feature,
                                    'species_set': species_set})
        return res

    def get_overlap_by_region(self, region, species, feature='gene', frmt='json', biotype=None, cell_type=None,
                              db_type=None, logic_name=None, misc_set=None, so_term=None,
                              species_set='mammals', trim_downstream=False, trim_upstream=False):
        """
        Retrieves multiple types of features for a given region.

        :param region: Query region. A maximum of 5Mb is allowed to
            be requested at any one time. e.g.,  X:1..1000:1, X:1..1000:-1,
            X:1..1000
        :param species: Species name/alias.
        :param feature: The type of feature to retrieve. Multiple
            values are accepted: gene, transcript, cds, exon, repeat,
            simple, misc, variation, somatic_variation, structural_variation,
            somatic_structural_variation, constrained, regulatory
        :param frmt: data return format
        :param biotype: The functional classification of the gene or
            transcript to fetch. Cannot be used in conjunction with logic_name
            when querying transcripts. (e.g., protein_coding)
        :param cell_type: Cell type name in Ensembl's Regulatory Build,
            required for segmentation feature, optional for regulatory elements.
            e.g., K562
        :param db_type: Restrict the search to a database other than
            the default. Useful if you need to use a DB other than core
        :param logic_name: Limit retrieval of genes, transcripts and
            exons by a given name of an analysis.
        :param misc_set: Miscellaneous set which groups together
            feature entries. Consult the DB or returned data sets to discover
            what is available. (e.g., cloneset_30k)
        :param so_term: Sequence Ontology term to narrow down the
            possible variations returned. (e.g., SO:0001650)
        :param species_set: Filter by species set for
            retrieving constrained elements. (e.g. mammals)
        :param bool trim_downstream: Do not return features which overlap
            the downstream end of the region.
        :param bool trim_upstream: Do not return features which overlap
            upstream end of the region.

        """
        check_param_in_list(feature, ['gene', 'transcript', 'cds', 'exon', 'repeat', 'simple', 'misc', 'variation',
                                      'somatic_variation', 'structural_variation', 'somatic_structural_variation',
                                      'constrained', 'regulatory', 'segmentation', 'motif', 'chipseq', 'array_probe'])
        self.__check_frmt(frmt, ['xml', 'gff3', 'bed'])
        res = self.http_get("overlap/region/{0}/{1}".format(species, region),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'biotype': biotype,
                                    'cell_type': cell_type, 'feature': feature,
                                    'db_type': db_type, 'logic_name': logic_name,
                                    'misc_set': misc_set,
                                    'so_term': so_term, 'species_set': species_set,
                                    'trim_downstream': trim_downstream,
                                    'trim_upstream': trim_upstream
                                    })
        return res

    def get_overlap_by_translation(self, identifier, frmt='json', db_type=None, feature='protein_feature', so_term=None,
                                   species=None, type='none'):
        """
        Retrieve features related to a specific Translation as
        described by its stable ID (e.g. domains, variations).

        :param identifier: An Ensembl stable id
        :param frmt: data return format
        :param db_type: Restrict the search to a database other
            than the default. Useful if you need to use a DB other than core
        :param feature: requested feature in: transcript_variation,
            protein_feature, residue_overlap, translation_exon,
            somatic_transcript_variation
        :param so_term: Sequence Ontology term to restrict the variations
            found. Its descendants are also included in the search. (e.g.,
            SO:0001650)
        :param species: species name/alias
        :param type: Type of data to filter by. By default, all
            features are returned. Can specify a domain or consequence
            type. (e.g.,  low_complexity)
        """
        check_param_in_list(feature, ['transcript_variation', 'protein_feature', 'residue_overlap', 'translation_exon',
                                      'somatic_transcript_variation'])
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get("overlap/translation/{0}".format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback,
                                    'db_type': db_type, 'feature': feature,
                                    'so_term': so_term, 'species': species,
                                    'type': type})
        return res

    # SEQUENCE
    # -----------------------------
    def get_sequence_by_id(self, identifier, frmt='fasta', db_type=None, expand_3prime=None, expand_5prime=None,
                           format='fasta', mask=None, mask_feature=False, multiple_sequences=False, object_type=None,
                           species=None, type='genomic'):
        """
        Request multiple types of sequence by stable identifier.
 
        :param identifier: An Ensembl stable ID
        :param frmt: response formats: fasta, json, text, yam, jsonp
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core (e.g.,
            core)
        :param int expand_3prime: Expand the sequence downstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param int expand_5prime: Expand the sequence upstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param format: Format of the data (e.g., fasta)
        :param mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters. Only available when using genomic
            sequence type. (hard/soft)
        :param bool mask_feature: Mask features on the sequence. If sequence
            is genomic, mask introns. If sequence is cDNA, mask UTRs.
            Incompatible with the 'mask' option
        :param bool multiple_sequences: Allow the service to return more
            than 1 sequence per identifier. This is useful when querying
            for a gene but using a type such as protein.
        :param object_type: Filter by feature type (e.g., gene)
        :param species: Species name/alias (e.g., homo_sapiens)
        :param type: could be genomic, cds, cdna, protein (homo_sapiens).
            Requesting a gene and kind not equal to genomic may result in
            multiple sequence, which required the parameter multi_sequences
            to be set to True

        # Default format is fasta, let us use parameter frmt to overwrite it
        sequence = e.get_sequence('ENSG00000157764', frmt='text')
        print(sequence[0:10])
        CGCCTCCCTTCCCCCTCCCC

        # complex request for different database and kind
        res = e.get_sequence('CCDS5863.1', frmt='fasta',
                object_type='transcript', db_type='otherfeatures',
                type='cds', species='human')
        print(res[0:100])
        >CCDS5863.1
        ATGGCGGCGCTGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGGCTCTGTTCAAC
        GGGGACATGGAGCCCGAGGCCGGCGCC

        """
        check_param_in_list(type, ['genomic', 'cds', 'cdna', 'protein'])
        check_param_in_list(mask, ['hard', 'soft'])
        self.__check_frmt(frmt, ['fasta', 'text', 'yaml', 'seqxml'])
        multiple_sequences = int(multiple_sequences)
        res = self.http_get('sequence/id/{0}'.format(identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={
                                'db_type': db_type, 'object_type': object_type,
                                'multiple_sequences': multiple_sequences, 'species': species,
                                'expand_3prime': expand_3prime,
                                'expand_5prime': expand_5prime, 'format': format, 'mask': mask,
                                'mask_feature': mask_feature, 'type': type}
                            )
        return res

    def post_sequence_by_id(self, identifier, frmt='fasta', db_type=None, expand_3prime=None, expand_5prime=None,
                            format='fasta', mask=None, mask_feature=False, multiple_sequences=False, object_type=None,
                            species=None, type='genomic'):
        """
        Request multiple types of sequence by a stable identifier list.

        :param identifier: An Ensembl stable ID
        :param frmt: response formats: fasta, json, text, yam, jsonp
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core (e.g.,
            core)
        :param int expand_3prime: Expand the sequence downstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param int expand_5prime: Expand the sequence upstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param format: Format of the data (e.g., fasta)
        :param mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters. Only available when using genomic
            sequence type. (hard/soft)
        :param bool mask_feature: Mask features on the sequence. If sequence
            is genomic, mask introns. If sequence is cDNA, mask UTRs.
            Incompatible with the 'mask' option
        :param bool multiple_sequences: Allow the service to return more
            than 1 sequence per identifier. This is useful when querying
            for a gene but using a type such as protein.
        :param object_type: Filter by feature type (e.g., gene)
        :param species: Species name/alias (e.g., homo_sapiens)
        :param type: could be genomic, cds, cdna, protein (homo_sapiens).
            Requesting a gene and kind not equal to genomic may result in
            multiple sequence, which required the parameter multi_sequences
            to be set to True
        """
        identifier = tolist(identifier)
        check_param_in_list(type, ['genomic', 'cds', 'cdna', 'protein'])
        check_param_in_list(mask, ['hard', 'soft'])
        self.__check_frmt(frmt, ['fasta', 'text', 'yaml', 'seqxml'])
        multiple_sequences = int(multiple_sequences)
        res = self.http_post('sequence/id',
                             data={"ids": identifier},
                             frmt=frmt,
                             headers=self.get_headers(content=frmt),
                             params={'db_type': db_type, 'object_type': object_type,
                                     'multiple_sequences': multiple_sequences, 'species': species,
                                     'expand_3prime': expand_3prime,
                                     'expand_5prime': expand_5prime, 'format': format, 'mask': mask,
                                     'mask_feature': mask_feature, 'type': type}
                             )
        return res

    def get_sequence_by_region(self, region, species, frmt='json', coord_system=None, coord_system_version=None,
                               expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=False):
        """
        Returns the genomic sequence of the specified region of the given species.

        :param frmt: data return format
        :param region: Query region. A maximum of 10Mb is allowed to be
            requested at any one time. e.g.,  X:1000000..1000100:1
        :param species: Species name/alias
        :param coord_system: Filter by coordinate system name (e.g., contig,
            seqlevel)
        :param  coord_system_version: Filter by coordinate system version
            (e.g., GRCh37)
        :param int expand_3prime: Expand the sequence downstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param int expand_5prime: Expand the sequence upstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param format: Format of the data. (e.g., fasta)
        :param mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters. Only available when using genomic
            sequence type. (hard/soft)
        :param bool mask_feature: Mask features on the sequence. If sequence
            is genomic, mask introns. If sequence is cDNA, mask UTRs.
            Incompatible with the 'mask' option

        """
        check_param_in_list(mask, ['hard', 'soft'])
        self.__check_frmt(frmt, ['fasta', 'text', 'yaml', 'seqxml'])
        res = self.http_get('sequence/region/{0}/{1}'.format(species, region),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={
                                'callback': self.callback, 'coord_system': coord_system,
                                'coord_system_version': coord_system_version,
                                'expand_3prime': expand_3prime,
                                'expand_5prime': expand_5prime, 'format': format, 'mask': mask,
                                'mask_feature': mask_feature}
                            )
        return res

    def pos_sequence_by_region(self, region, species, frmt='json', coord_system=None, coord_system_version=None,
                               expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=False):
        """
        Returns the genomic sequence of the specified region of the given species.

        :param frmt: data return format
        :param region: Query region. A maximum of 10Mb is allowed to be
            requested at any one time. e.g.,  X:1000000..1000100:1
        :param species: Species name/alias
        :param coord_system: Filter by coordinate system name (e.g., contig,
            seqlevel)
        :param  coord_system_version: Filter by coordinate system version
            (e.g., GRCh37)
        :param int expand_3prime: Expand the sequence downstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param int expand_5prime: Expand the sequence upstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param format: Format of the data. (e.g., fasta)
        :param mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters. Only available when using genomic
            sequence type. (hard/soft)
        :param bool mask_feature: Mask features on the sequence. If sequence
            is genomic, mask introns. If sequence is cDNA, mask UTRs.
            Incompatible with the 'mask' option

        """
        region = tolist(region)
        check_param_in_list(mask, ['hard', 'soft'])
        self.__check_frmt(frmt, ['fasta', 'text', 'yaml', 'seqxml'])
        res = self.http_get('sequence/region/{}'.format(species),
                            data={'regions': region},
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={
                                'callback': self.callback, 'coord_system': coord_system,
                                'coord_system_version': coord_system_version,
                                'expand_3prime': expand_3prime,
                                'expand_5prime': expand_5prime, 'format': format, 'mask': mask,
                                'mask_feature': mask_feature}
                            )
        return res

    # VARIATION VEP
    # -----------------------------------------------------
    def get_variation_by_id(self, identifier, species, frmt='json', genotypes=False, phenotypes=False,
                            pops=False, population_genotypes=False):
        """
        Uses a variation identifier (e.g. rsID) to return the variation features

        :param identifier: variation identifier (e.g., rs56116432)
        :param species: Species name/alias (e.g., homo_sapiens)
        :param frmt: response format (json, xml, jsonp)
        :param bool genotypes: Include genotypes
        :param bool phenotypes: Include phenotypes
        :param bool pops: Include populations
        :param population_genotypes:

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('variation/{0}/{1}'.format(species, identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'genotypes': int(genotypes), 'phenotypes': int(phenotypes),
                                    'pops': int(pops), 'population_genotypes': population_genotypes}
                            )
        return res

    def get_vep_by_id(self, identifier, species, frmt='json', canonical=False, ccds=False, domains=False, hgvs=False,
                      numbers=False, protein=False, xref_refseq=False):
        """
        Fetch variant consequences based on a variation identifier

        :param domains: Include names of overlapping protein domains
        :param frmt: data return format
        :param identifier: Query ID. Supports dbSNP, COSMIC and
            HGMD identifiers   (e.g.,    rs116035550, COSM476)
        :param species: Species name/alias
        :param bool canonical: Include a flag indicating the canonical transcript for a gene
        :param bool ccds: Include CCDS transcript identifiers
        :param bool domains:Include names of overlapping protein domains
        :param bool hgvs: Include HGVS nomenclature based on Ensembl stable identifiers
        :param bool numbers: Include affected exon and intron positions within the transcript
        :param bool protein: Include Ensembl protein identifiers
        :param bool xref_refseq: Include aligned RefSeq mRNA identifiers for
            transcript. NB: theRefSeq and Ensembl transcripts aligned in this
            way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence,
            exon structure and protein product

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('vep/{0}/id/{1}'.format(species, identifier),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'canonical': canonical,
                                    'ccds': ccds, 'domains': domains,
                                    'hgvs': hgvs, 'numbers': numbers, 'protein': protein,
                                    'xref_refseq': xref_refseq})
        return res

    def get_vep_by_region(self, region, allele, species, frmt='json', canonical=False, ccds=False, domains=False,
                          hgvs=False, numbers=False, protein=False, xref_refseq=False):
        """
        Fetch variant consequences

        :param region: Query region e.g,  9:22125503-22125502:1
        :param allele: Variation allele (e.g., C, DUP)
        :param species: Species name/alias
        :param domains: Include names of overlapping protein domains
        :param frmt: data return type
        :param bool canonical: Include a flag indicating the canonical transcript for a gene
        :param bool ccds: Include CCDS transcript identifiers
        :param bool domains:Include names of overlapping protein domains
        :param bool hgvs: Include HGVS nomenclature based on Ensembl stable identifiers
        :param bool numbers: Include affected exon and intron positions within the transcript
        :param bool protein: Include Ensembl protein identifiers
        :param bool xref_refseq: Include aligned RefSeq mRNA identifiers for
            transcript. NB: theRefSeq and Ensembl transcripts aligned in this
            way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence,
            exon structure and protein product

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('vep/{0}/region/{1}/{2}'.format(species, region, allele),
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'canonical': canonical,
                                    'ccds': ccds, 'domains': domains,
                                    'hgvs': hgvs, 'numbers': numbers, 'protein': protein,
                                    'xref_refseq': xref_refseq})
        return res

    def post_vep_by_region(self, species, variants, frmt='json', canonical=False, ccds=False, domains=False,
                           hgvs=False, numbers=False, protein=False, xref_refseq=False):
        """
        Fetch variant consequences for multiple regions

        :param species: Species name/alias
        :param variants: 4  16056694 21  ENSVATH00550254  C - . . .
        :param frmt: data return format
        :param canonical: Include a flag indicating the canonical transcript for a gene
        :param ccds: Include CCDS transcript identifiers
        :param domains: Include names of overlapping protein domains
        :param hgvs: Include HGVS nomenclature based on Ensembl stable identifiers
        :param numbers: Include affected exon and intron positions within the transcript
        :param protein: Include Ensembl protein identifiers
        :param xref_refseq: Include aligned RefSeq mRNA identifiers for transcript. NB: theRefSeq and Ensembl
         transcripts aligned in this way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence, exon structure
         and protein product

        """
        self.__check_frmt(frmt, ['xml'])
        res = self.http_get('vep/{0}/region/'.format(species),
                            data={"variants": variants},
                            frmt=frmt,
                            headers=self.get_headers(content=frmt),
                            params={'callback': self.callback, 'canonical': canonical,
                                    'ccds': ccds, 'domains': domains,
                                    'hgvs': hgvs, 'numbers': numbers, 'protein': protein,
                                    'xref_refseq': xref_refseq})
        return res
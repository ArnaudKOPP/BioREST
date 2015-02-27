# coding=utf-8
__author__ = "Arnaud KOPP"
__copyright__ = "© 2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GNU GPL V2.0"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

from collections import OrderedDict
import logging
import pandas as pd

log = logging.getLogger(__name__)


class MultiFASTA(object):
    """
    Class for FASTA files
    """

    def __init__(self):
        # fetch the sequence using this attribute
        self._fasta_fetcher = FASTA()

        # an ordered dictionary to store the fasta contents
        self._fasta = OrderedDict()

    def __len__(self):
        return len(self._fasta)

    def _get_fasta(self):
        return self._fasta

    fasta = property(_get_fasta, doc="Returns all FASTA instances ")

    def _get_ids(self):
        return [f for f in self._fasta.keys()]

    ids = property(_get_ids, doc="returns list of keys/accession identifiers")

    def load_fasta(self, ids):
        """
        Loads a single FASTA file into the dictionary

        :param ids:
        """
        if isinstance(ids, str):
            ids = [ids]

        for id_ in ids:
            self._fasta_fetcher.load(id_)
            # create a new instance of FASTA and save fasta data
            f = FASTA()
            f._fasta = self._fasta_fetcher._fasta[:]

            # append in the ordered dictionary
            self._fasta[id_] = f
            log.info("%s loaded" % id_)

    def save_fasta(self, filename):
        """
        Save all FASTA into a file
        :param filename:
        """
        fh = open(filename, "w")
        for f in self._fasta.values():
            fh.write(f.fasta)
        fh.close()

    def read_fasta(self, filename):
        """
        Load several FASTA from a filename
        :param filename:
        """
        fh = open(filename, "r")
        data = fh.read()
        fh.close()

        # we split according to ">2 character
        for thisfasta in data.split(">")[1:]:
            f = FASTA()
            f._fasta = f._interpret(thisfasta)
            if f.accession is not None and f.accession not in self.ids:
                self._fasta[f.accession] = f
            else:
                log.warning("Accession %s is already in the ids list or could not be interpreted. skipped" %
                            str(f.accession))

    def _get_df(self):
        df = pd.concat([self.fasta[id_].df for id_ in self.fasta.keys()])
        df.reset_index(inplace=True)
        return df

    df = property(_get_df)

    def hist_size(self, **kargs):
        """

        :param kargs:
        """
        try:
            import pylab
            self.df.Size.hist(**kargs)
            pylab.title("Histogram length of the sequences")
            pylab.xlabel("Length")
        except:
            pass


class FASTA(object):
    """
    Fasta class
    """
    known_dbtypes = ["sp", "gi"]

    def __init__(self):
        self._fasta = None

    def _get_fasta(self):
        return self._fasta

    fasta = property(_get_fasta, doc="returns FASTA content")

    # for all types
    def _get_sequence(self):
        if self.fasta:
            return "".join(self.fasta.split("\n")[1:])
        else:
            raise ValueError("You need to load a fasta sequence first using get_fasta or read_fasta")

    sequence = property(_get_sequence, doc="returns the sequence only")

    # for all types
    def _get_header(self):
        if self.fasta:
            return self.fasta.split("\n")[0]
        else:
            raise ValueError("You need to load a fasta sequence first using get_fasta or read_fasta")

    header = property(_get_header, doc="returns header only")

    def _get_dbtype(self):
        dbtype = self.header.split("|")[0].replace(">", "")
        return dbtype

    dbtype = property(_get_dbtype)

    # for all types
    def _get_identifier(self):
        return self.header.split(" ")[0]

    identifier = property(_get_identifier)

    def _get_entry(self):
        return self.header.split("|")[2].split(" ")[0]

    entry = property(_get_entry, doc="returns entry only")

    # swiss prot only
    def _get_accession(self):
        if self.dbtype == "sp":
            # header = self.header
            return self.identifier.split("|")[1]
        elif self.dbtype == "gi":
            return self.identifier.split("|")[1]

    accession = property(_get_accession)

    # swiss prot only
    def _get_name_sp(self):
        if self.dbtype == "sp":
            header = self.header
            return header.split(" ")[0].split("|")[2]

    name = property(_get_name_sp)

    def _get_df(self):
        df = pd.DataFrame({
            "Identifiers": [self.identifier],
            "Accession": [self.accession],
            "Entry": [self.entry],
            "Database": [self.dbtype],
            "Organism": [self.organism],
            "PE": [self.PE],
            "SV": [self.SV],
            "Sequence": [self.sequence],
            "Header": [self.header],
            "Size": [len(self.sequence)]})
        return df

    df = property(_get_df)

    def _get_info_from_header(self, prefix):
        if prefix not in self.header:
            return None
        # finds the prefix
        index = self.header.index(prefix + "=")
        # remove it
        name = self.header[index:][3:]
        # figure out if there is anothe = sign to split the string
        # otherwise, the prefix we looked for is the last one anyway
        if "=" in name:
            name = name.split("=")[0]
            # here each = sign in FASTA is preceded by 2 characters that we must remove
            name = name[0:-2]
            name = name.strip()
        else:
            name = name.strip()
        return name

    def _get_gene_name(self):
        return self._get_info_from_header("GN")

    gene_name = property(_get_gene_name,
                         doc="returns gene name from GN keyword found in the header if any")

    def _get_organism(self):
        return self._get_info_from_header("OS")

    organism = property(_get_organism,
                        doc="returns organism from OS keyword found in the header if any")

    def _get_PE(self):
        pe = self._get_info_from_header("PE")
        if pe is not None:
            return int(pe)

    PE = property(_get_PE,
                  doc="returns PE keyword found in the header if any")

    def _get_SV(self):
        sv = self._get_info_from_header("SV")
        if sv is not None:
            return int(sv)

    SV = property(_get_SV,
                  doc="returns SV keyword found in the header if any")

    def __str__(self):
        str_ = self.fasta
        return str_

    def load(self, id_):
        self.load_fasta(id_)

    def load_fasta(self, id_):
        """

        :param id_:
        :raise Exception:
        """
        from BioREST.Uniprot import Uniprot
        u = Uniprot()
        try:
            res = u.retrieve(id_, frmt="fasta")
            # some entries in uniprot are valid but obsolet and return empty string
            if res == "":
                raise Exception
            self._fasta = res[:]
        except:
            pass

    def save_fasta(self, filename):
        """
        Save FASTA file into a filename

        :param str filename: where to save it
        """
        if self._fasta is None:
            raise ValueError("No fasta was read or downloaded. Nothing to save.")

        fh = open(filename, "w")
        fh.write(self._fasta)
        fh.close()

    def read_fasta(self, filename):
        """

        :param filename:
        :raise ValueError:
        """
        fh = open(filename, "r")
        data = fh.read()
        fh.close()

        # Is there more than one sequence ?
        data = data.split(">")[1:]
        if len(data) > 1 or len(data) == 0:
            raise ValueError(
                """Only one sequence expected to be found. Found %s. Please use MultiFASTA class instead""" % len(data))

        self._data = data
        if data.count(">sp|") > 1:
            raise ValueError("""It looks like your FASTA file contains more than
            one FASTA. You must use MultiFASTA class instead""")
        self._fasta = data[:]
        self._fasta = self._fasta[0]
        if self.dbtype not in self.known_dbtypes:
            log.warning("Only sp and gi header are recognised so far but sequence and header are loaded")

    @staticmethod
    def _interpret(data):
        # cleanup the data in case of empty spaces or \n characters
        return data
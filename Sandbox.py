#!/usr/bin/env python3
# encoding: utf-8
import pandas as pd
import json
import logging
import BioREST
from BioREST.Service import list2string
from io import StringIO
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


# target = ["NXF1", "ALAS2", "GPI", "EIF4A3", "RRM2", "RAD51L3", "KIF26A", "CDC5L", "ABCC3", "ATP1B2"]
# print(list2string(target, sep='%0D', space=False))

# k = BioREST.KEGG()
# target = ["NXF1"]
# for gene in target:
#     try:
#         # res = k.find("hsa", gene)
#         # print(res)
#         des = k.get(":".join(["hsa", gene]))
#         print(des)
#
#         # res = TCA.KEGGParser(des)
#         # print(res['PATHWAY'])
#         # print(json.dumps(res, indent=4))
#
#         # path = k.get(res['PATHWAY'][0].split()[0], "kgml")
#         # print(path)
#
#     except:
#         pass

# psi = BioREST.PSICQUIC()
# psi.TIMEOUT = 10
# psi.RETRIES = 1
# psi.retrieve_all('NXF1')

# hgnc = BioREST.HGNC()
# print(json.dumps(hgnc._info, indent=4))
# res = hgnc.fetch(storedfield='symbol', term='ALAS2')
# print(json.dumps(res, indent=4))
# print(res['response']['docs'][0]['ensembl_gene_id'])

# gene = target

# string = BioREST.String(identity='kopp@igbmc.fr')
# res = string.resolve(gene, species='9606')
# print(json.dumps(res, indent=4))
# id_gene = []
# in case of multiple return, search for
# for i in res:
#     if i['preferredName'] in gene:
#         id_gene.append(i['stringId'])
#
# print(id_gene)
# print(list2string(id_gene, sep='\n', space=False))
# interaction = string.interactions(identifier=id_gene, frmt='psi-mi-tab', species=9606)
# print(interaction)
# file = open('/home/arnaud/Desktop/inter.txt', mode='w')
# file.write(interaction)
# file.close()
# table = pd.read_table(StringIO(interaction), header=None)
# print(table)

# react = BioREST.Reactome()
# print(json.dumps(react.query_hit_pathways(target), indent=4))
#
# biogrid = BioREST.Biogrid(acceskey="dc589cabccb374194e060d3586b31349")
# data = biogrid.interaction(geneList='NXF1', taxId=9606)
#
# df = BioREST.BiogridParser(data_input=data)
# print(df)

# dgidb = BioREST.DGIdb()
# print(dgidb.Search_Interactions(genes=['FLT1', 'MM1', 'FAKE'], drug_types='antineoplastic',
#                                 interaction_sources='TALC'))
# print(dgidb.Interaction_Source())
# print(dgidb.Interaction_Type())
# print(dgidb.Gene_Categories())
# print(dgidb.Source_Trust_Levels())
# print(dgidb.Drug_Types())

pdb = BioREST.PDB()
# print(pdb.describe_pdb('4HHB'))
# print(pdb.describe_pdb_entity('4HHB'))
# print(pdb.describe_chemical_comp('NAG'))
# print(pdb.get_current_PDB_ids())
# print(pdb.get_obsolete_PDB_ids())
# print(pdb.get_unreleased())
# print(pdb.get_unreleased('450D'))
# print(pdb.get_ligand('4HHB'))
# print(pdb.get_gene_ontology('4HHB'))
res = pdb.smiles_query(query='NC(=O)C1=CC=CC=C1', search_type='substructure')
print(res.findAll('p'))

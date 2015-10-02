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


# #### KEGG REST TEST

# from BioREST import KEGG, KEGGParser, KEGGParser2
# k = KEGG()
# print(k.tnumber_to_code("T01001"))
# print(k.databases)
# print(k.code_to_tnumber("hsa"))
# print(k.is_organism("hsa"))
# print(k.info())
# print(k.info("hsa"))
# print(k.info("T01001"))  # same as above
# print(k.info("pathway"))
# k.list('organism')
# print(k.organismIds)
# print(k.pathwayIds)
# print(k.get("hsa:7535"))
# print(k.list("pathway", organism="hsa"))
# print(k.list("pathway"))  # returns the list of reference pathways
# print(k.list("pathway", "hsa"))  # returns the list of human pathways
# print(k.list("organism"))  # returns the list of KEGG organisms with taxonomic classification
# print(k.list("hsa"))  # returns the entire list of human genes
# print(k.list("T01001"))  # same as above
# print(k.list("hsa:10458+ece:Z5100"))  # returns the list of a human gene and an E.coli O157 gene
# print(k.list("cpd:C01290+gl:G00092"))  # returns the list of a compound entry and a glycan entry
# print(k.list("C01290+G00092"))  # same as above
# # search for pathways that contain Viral in the definition
# print(k.find("pathway", "Viral"))
# # for keywords "shiga" and "toxin"
# print(k.find("genes", "shiga+toxin"))
# # for keywords "shiga toxin"
# print(k.find("genes", "shiga toxin"))
# # for chemical formula "C7H10O5"
# print(k.find("compound", "C7H10O5", "formula"))
# # for chemical formula containing "O5" and "C7"
# print(k.find("compound", "O5C7", "formula"))
# # for 174.045 =< exact mass < 174.055
# print(k.find("compound", "174.05", "exact_mass"))
# # for 300 =< molecular weight =< 310
# print(k.find("compound", "300-310", "mol_weight"))
# # retrieves a compound entry and a glycan entry
# print(k.get("cpd:C01290+gl:G00092"))
# # same as above
# print(k.get("C01290+G00092"))
# # retrieves a human gene entry and an E.coli O157 gene entry
# print(k.get("hsa:10458+ece:Z5100"))
# # retrieves amino acid sequences of a human gene and an E.coli O157 gene
# print(k.get("hsa:10458+ece:Z5100/aaseq"))
# res = k.get("hsa05130/image")
# # same as : res = s.get("hsa05130","image")
# f = open("test.png", "wb")
# f.write(res)
# f.close()
# # conversion from NCBI GeneID to KEGG ID for E. coli genes
# print(k.conv("eco", "ncbi-geneid"))
# # inverse of the above example
# print(k.conv("eco", "ncbi-geneid"))
# # conversion from KEGG ID to NCBI GI
# print(k.conv("ncbi-gi", "hsa:10458+ece:Z5100"))
# # KEGG pathways linked from each of the human genes
# print(k.link("pathway", "hsa"))
# # human genes linked from each of the KEGG pathways
# print(k.link("hsa", "pathway"))
# # KEGG pathways linked from a human gene and an E. coli O157 gene.
# print(k.link("pathway", "hsa:10458+ece:Z5100"))
# # show a pathway in the browser
# k.show_pathway("path:hsa05416", scale=50)
# # Same as above but also highlights some KEGG Ids (red for all)
# k.show_pathway("path:hsa05416", dcolor="white", keggid=['1525', '1604', '2534'])
# # You can refine the colors using a dictionary:
# k.show_pathway("path:hsa05416", dcolor="white", keggid={'1525': 'yellow,red', '1604': 'blue,green', '2534': "blue"})
# print(k.get_pathway_by_gene("7535", "hsa"))
# data = k.get("hsa:1203")
# print(data)
# res = KEGGParser2(data)
# print(json.dumps(res, indent=4))
# res2 = KEGGParser(data)
# print(json.dumps(res2, indent=4))
# data = s.get("hsa04660")
# dict_data = s.parse(data)
# print(dict_data['gene'])
# res = s.get("hsa04660", "kgml")
# print(res)
# res = s.parse_kgml_pathway("hsa04660")
# # print(res)
# res['relations']
# print(res['relations'][0])


# pdb = BioREST.PDB()
# res = pdb.describe_pdb('4HHB')
# print(res['pdb'][0]['title'])
# print(res['pdb'][0].attrs)
# print(pdb.describe_pdb_entity('4HHB'))
# print(pdb.describe_chemical_comp('NAG'))
# print(pdb.get_current_PDB_ids())
# print(pdb.get_obsolete_PDB_ids())
# print(pdb.get_unreleased())
# print(pdb.get_unreleased('450D'))
# print(pdb.get_ligand('4HHB'))
# print(pdb.get_gene_ontology('4HHB'))
# res = pdb.smiles_query(query='NC(=O)C1=CC=CC=C1', search_type='substructure')
# print(res.findAll('p'))

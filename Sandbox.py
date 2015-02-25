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


def rest():
    target = ["NXF1", "ALAS2", "GPI", "EIF4A3", "RRM2", "RAD51L3", "KIF26A", "CDC5L", "ABCC3", "ATP1B2"]
    print(list2string(target, sep='%0D', space=False))
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

    gene = 'NXF1'

    string = BioREST.String(identity='kopp@igbmc.fr')
    res = string.resolve(gene, species='9606')
    print(json.dumps(res, indent=4))
    id_gene = ''
    # in case of multiple return, search for
    for i in res:
        if i['preferredName'] == gene:
            id_gene = i['stringId']

    interaction = string.interactions(identifier=id_gene, frmt='psi-mi-tab')
    table = pd.read_table(StringIO(interaction), header=None)
    print(table)


rest()
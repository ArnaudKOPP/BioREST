import os
import json
import logging
import BioREST

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def rest():
    k = BioREST.KEGG()
    # target = ["NXF1", "ALAS2", "GPI", "EIF4A3", "RRM2", "RAD51L3", "KIF26A", "CDC5L", "ABCC3", "ATP1B2"]
    target = ["NXF1"]
    for gene in target:
        try:
            # res = k.find("hsa", gene)
            # print(res)
            des = k.get(":".join(["hsa", gene]))
            print(des)

            # res = TCA.KEGGParser(des)
            # print(res['PATHWAY'])
            # print(json.dumps(res, indent=4))

            # path = k.get(res['PATHWAY'][0].split()[0], "kgml")
            # print(path)

        except:
            pass
    # psi = BioREST.PSICQUIC()
    # psi.TIMEOUT = 10
    # psi.RETRIES = 1
    # psi.retrieve_all('NXF1')

rest()
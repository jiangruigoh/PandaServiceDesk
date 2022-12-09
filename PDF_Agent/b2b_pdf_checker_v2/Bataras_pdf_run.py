"""
Version No: 1
Release Date: 28 September 2021 
KKSC
"""
from yaml_pdf_config import assign_config_values
import os
import time

bataras_cls = assign_config_values()

# Assign values based on customer

bataras_cls.sql_database_name = "compare_bataras"
#ref_list_base_path = "/media/estore/fastAPI/PandaServiceDesk/PDF_Agent/b2b_pdf_checker_v2/File_list_text/"
#bataras_cls.absolute_pth_refno = os.path.join(ref_list_base_path, "ref_list.txt")
#bataras_cls.remove_old_file()

start = time.time()
# Get PDF list from Assign Directory
#bataras_cls.absolute_pth_refno =  os.path.join(ref_list_base_path, "pdf_list.txt")
#bataras_cls.remove_old_file()

print("GET PDF FROM PATH")
bataras_cls.check_path_Store_v4()

# cndn_amt
print("Start Query From Database...")
print("cncdn checkpoint")
bataras_cls.sql_columns = "refno"
bataras_cls.sql_tablename = "cndn_amt"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "PDN"
print(bataras_cls.validate())

# cnnotemain
print("cnnotemain checkpoint")
bataras_cls.sql_columns = "RefNo"
bataras_cls.sql_tablename = "cnnotemain"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "PRCN"
print(bataras_cls.validate())

# dbnotemain
print("dbnotemain checkpoint")
bataras_cls.sql_columns = "RefNo"
bataras_cls.sql_tablename = "dbnotemain"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "PRDN"
print(bataras_cls.validate())

# discheme_taxinv
print("discheme_taxinv checkpoint")
bataras_cls.sql_columns = "refno"
bataras_cls.sql_tablename = "discheme_taxinv"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "DI"
print(bataras_cls.validate())

# grmain
print("grmain checkpoint")
bataras_cls.sql_columns = "RefNo"
bataras_cls.sql_tablename = "grmain"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "GRN"
print(bataras_cls.validate())

# grmain_dncn
print("grmain_dncn checkpoint")
bataras_cls.sql_columns = "RefNo"
bataras_cls.sql_tablename = "grmain_dncn"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "GRDA"
print(bataras_cls.validate())

# pomain
print("pomain checkpoint")
bataras_cls.sql_columns = "RefNo"
bataras_cls.sql_tablename = "pomain"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "PO"
print(bataras_cls.validate())

# promo_taxinv
print("promo_taxinv checkpoint")
bataras_cls.sql_columns = "refno"
bataras_cls.sql_tablename = "promo_taxinv"
bataras_cls.sql_connect()
bataras_cls.query()
bataras_cls.doc_type = "PCI"
print(bataras_cls.validate())


end = time.time()
print("Time Taken: "+ str(end - start))
print("ref_no_counter: " + str(bataras_cls.ref_no_counter))
print("PDF Count: " + str(bataras_cls.pdf_counter))
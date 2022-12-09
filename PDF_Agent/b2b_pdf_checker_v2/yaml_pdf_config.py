"""
Version No: 1
Release Date: 28 September 2021 
KKSC
"""
import yaml
from get_refno import SQL_Q

def assign_config_values():
    get_task_pdf = SQL_Q()
    with open("/media/estore/fastAPI/PandaServiceDesk/PDF_Agent/b2b_pdf_checker_v2/pdf_config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        #print(cfg)

    # Panda Task Agent config
    get_task_pdf.hostname = cfg["mysql"]["hostname"]
    get_task_pdf.sql_username = cfg["mysql"]["username"]
    get_task_pdf.sql_pwd = cfg["mysql"]["pwd"]
    get_task_pdf.sql_port = cfg["mysql"]["port"]
    
    # PDF path
    get_task_pdf.pdf_store_path = cfg["pdf"]["store_path"]

    ymlfile.close()

    return get_task_pdf
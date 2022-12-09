# MYSQL Restore Dump File Agent
"""
Version No: 1
Release Date: 21 February 2022 
KKSC
"""

# param_1: source_path
# param_2: filename
# param_3: database_name # Got USE database_name; in script hence no need to point to database
import os
import mysql.connector
import json
import yaml
from subprocess import check_output,CalledProcessError
from subprocess import Popen, PIPE, STDOUT
import subprocess


def connect():
    """GET Configuration parameters"""
    with open("/media/estore/fastAPI/PandaServiceDesk/panda_task_agent/Task_Agent_Config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        #print(cfg)

    # UVICON Configuration Variables
    #uvicorn_host = cfg["mysql"]["host"]
    #uvicorn_user = cfg["mysql"]["user"]
    #uvicorn_pass = cfg["mysql"]["passwd"]
    #uvicorn_db = cfg["mysql"]["db"]
    #uvicorn_port = cfg["mysql"]["port"]
    
    mydb = mysql.connector.connect(
            host = cfg["sqldump_cfg"]["hostname"],
            user = cfg["sqldump_cfg"]["username"],
            password=cfg["sqldump_cfg"]["passwd"],
            port = cfg["sqldump_cfg"]["port"]
        )

    ymlfile.close() # ALWAYS REMMEBER TO CLOSE FILE AFTER USE

    return mydb

def restore_agent(source_path, filename):
        with open("/media/estore/fastAPI/PandaServiceDesk/panda_task_agent/Task_Agent_Config.yml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            ymlfile.close() # ALWAYS REMMEBER TO CLOSE FILE AFTER USE
        USERNAME = cfg["sqldump_cfg"]["username"]
        PASSWORD=cfg["sqldump_cfg"]["passwd"]
        PORT = cfg["sqldump_cfg"]["port"]
        HOSTNAME = cfg["sqldump_cfg"]["hostname"]
        write_path_file = os.path.join(source_path, filename)
        try:
            command = """/usr/bin/mysql -u %s -p"%s" --host %s --port %s %s """ %(USERNAME, PASSWORD, HOSTNAME, PORT, "")
            with open(write_path_file) as input_file:
                process = Popen(command, stdin = input_file, stderr=PIPE, stdout=PIPE , shell=True)
            output,error = process.communicate()
            process.wait() # Ensures that SQLDUMP process finish before doing anything else
            returnCode = process.poll() 
            input_file.close()
            print("Return Code: ", returnCode)
            return {"status": "success",
                                "data": {
                                    "filename": filename,
                                    "filepath": source_path
                                },
                                #"message": "Affected rows: " + str(affected_rows),
                                "Error": str(error),
                                "message": "Affected rows: " + str('STDOUT:{}'.format(output)),
                                "code": 200
                    }
        except CalledProcessError as e:
            # error_msg = "Error: {}".format(err)
            return {"status": "fail",
                    "data": {
                        "filename": filename,
                        "filepath": source_path
                    },
                    "message": str(e),
                    "code": 422
            }

# restore_agent("/media/estore/PythonScriptAgent/SQLDUMP_files/decompress/", "BATARASHQ_20220222_05_0006.sql")



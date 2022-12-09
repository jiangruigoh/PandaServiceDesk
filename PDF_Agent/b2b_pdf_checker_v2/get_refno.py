"""
Version No: 1
Release Date: 28 September 2021 
KKSC

Get refno from restored database
"""
from os import error
import mysql.connector
import os

from datetime import datetime
import datetime as date_delta
import concurrent.futures

from tqdm import tqdm

def current_date_only():
    now = datetime.now() #Get Datetime input
    current_date = datetime.today().strftime('%Y-%m-%d')
    return current_date

def first_previous_date():
    last_day_of_prev_month = datetime.today().replace(day=1) - date_delta.timedelta(days=1)
    start_day_of_prev_month = datetime.today().replace(day=1) - date_delta.timedelta(days=last_day_of_prev_month.day)
    date_only_opt = start_day_of_prev_month.strftime ('%Y-%m-%d')
    return date_only_opt

def check_path_helper(path, dirs, files):
    for i in range(len(files)):
        abs_path_file = os.path.join(path, files[i])
        time_update = int(os.path.getmtime(abs_path_file))
        timestamp = datetime.fromtimestamp(time_update)
        last_modified = str(timestamp).split(" ")[0] 
        # print(files[i])
        if files[i].endswith(".pdf") and \
            last_modified <= current_date_only() and \
            last_modified >= first_previous_date():
                #self.dir_pdf_list.append(str(files[i]))
                #self.REF_NO = str(files[i])
                #self.append_refno()
                # print(files[i])
                return files[i]

def check_path_helper_v4(path_used, filename):
    abs_path_file = os.path.join(path_used, filename)
    time_update = int(os.path.getmtime(abs_path_file))
    timestamp = datetime.fromtimestamp(time_update)
    last_modified = str(timestamp).split(" ")[0]
    if filename.endswith(".pdf") and \
        last_modified <= current_date_only() and \
        last_modified >= first_previous_date():    
        return filename

class SQL_Q(object):
    def __init__(self):
        self.hostname = ""
        self.sql_username = ""
        self.sql_pwd = ""
        self.sql_port = ""
        self.sql_database_name = ""
        self.sql_tablename = ""
        self.sql_columns = "*"
        self.absolute_pth_refno = ""
        self.REF_NO = ""
        self.query_refno = []
        self.dir_pdf_list = []
        self.pdf_store_path = ""
        self.ref_no_counter = 0
        self.pdf_counter = 0
        self.missing_pdf = []
        self.match_pdf = []
        self.doc_type = ""

    def sql_connect(self):
        try:
            self.__connect = mysql.connector.connect(
                host = self.hostname,
                user = self.sql_username,
                password = self.sql_pwd,
                port = self.sql_port,
                database = self.sql_database_name
            )
            return self.__connect
        except error as e:
            return e
    
    def query(self):
        mycursor = self.__connect.cursor()
        try:
            mycursor.execute(""" SELECT %s FROM  %s """%(self.sql_columns, self.sql_tablename))
            self.__sql_output = mycursor.fetchall()
            for row in self.__sql_output:
                self.REF_NO = row[0]
                # print(self.REF_NO)
                # self.append_refno()
                self.query_refno.append(str(row[0]))
                self.ref_no_counter+=1
            self.__connect.close()
            return self.__sql_output
        except mysql.connector.Error as err:
            error_msg = "Error: {}".format(err)
            return error_msg
    
    def remove_old_file(self):
        try:
            if os.path.isfile(self.absolute_pth_refno):
                os.remove(self.absolute_pth_refno) # Ensures no overide on new Trigger
                return {"status": "SUCCESS",
                        "data": {
                            "path": self.absolute_pth_refno,
                        },
                        "message": "Done Remove OLD FILES",
                        "code": 422
                }
        except error as e:
            return {"status": "fail: " + str(e),
                    "data": {
                        "path": self.absolute_pth_refno,
                    },
                    "message": "FAIL",
                    "code": 422
            }
    
    def check_path_store(self):
        try:
            for path, dirs, files in os.walk(self.pdf_store_path):
                for i in range(len(files)):
                    abs_path_file = os.path.join(path, files[i])
                    time_update = int(os.path.getmtime(abs_path_file))
                    timestamp = datetime.fromtimestamp(time_update)
                    last_modified = str(timestamp).split(" ")[0] 
                    # print(files[i])
                    if files[i].endswith(".pdf") and \
                    last_modified <= current_date_only() and \
                    last_modified >= first_previous_date():
                        #self.dir_pdf_list.append(str(files[i]))
                        #self.REF_NO = str(files[i])
                        #self.append_refno()
                        self.pdf_counter+=1
                        # print(files[i])

        except error as e:
            return {"status": "fail: " + str(e),
                    "data": {
                        "path": self.absolute_pth_refno,
                    },
                    "message": "FAIL",
                    "code": 422
            }
    
    def check_path_store_v2(self):
        try:
            obj = os.scandir(self.pdf_store_path)
            for entry in obj:
                if entry.is_file():
                    filename = entry.name 
                    abs_path_file = os.path.join(self.pdf_store_path, entry.name)
                    time_update = int(os.path.getmtime(abs_path_file))
                    timestamp = datetime.fromtimestamp(time_update)
                    last_modified = str(timestamp).split(" ")[0]
                    # print(last_modified)
                    if  filename.endswith(".pdf") and \
                    last_modified <= current_date_only() and \
                    last_modified >= first_previous_date():
                        self.dir_pdf_list.append(str(filename))
                        #self.REF_NO = str(files[i])
                        #self.append_refno()
                        self.pdf_counter+=1
                        print(filename)

        except error as e:
            return {"status": "fail: " + str(e),
                    "data": {
                        "path": self.absolute_pth_refno,
                    },
                    "message": "FAIL",
                    "code": 422
            }
        
    def check_path_store_v3(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {executor.submit(check_path_helper, path, dirs, files) for path, dirs, files in os.walk(self.pdf_store_path)}
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result != None:
                        self.dir_pdf_list.append(result)
                        print(result)
                except Exception as exc:
                    print("There was an error. {}".format(exc))
        return self.dir_pdf_list
    
    def check_path_Store_v4(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = list(tqdm({executor.submit(check_path_helper_v4, self.pdf_store_path, filename): filename for filename in os.listdir(self.pdf_store_path)}))
            print("Ran Futures")
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result != None:
                        self.dir_pdf_list.append(result)
                except Exception as exc:
                    print("There was an error. {}".format(exc))
            print(self.dir_pdf_list)
            print(len(self.dir_pdf_list))
            return self.dir_pdf_list

    def append_refno(self):
        try:
            res = {"status": "success",
                    "data": {
                        "path": self.absolute_pth_refno,
                    },
                    "message": False,
                    "code": 200
                }
            with open(self.absolute_pth_refno, "a") as new_file:
                new_file.write(self.REF_NO + "\n")
            new_file.close()
            return res

        except error as e:
            return {"status": "fail: " + str(e),
                    "data": {
                        "path": self.absolute_pth_refno,
                    },
                    "message": "FAIL",
                    "code": 422
            }
    
    def validate(self):
        try:
            for ref_i in range(len(self.query_refno)):
                ref = self.query_refno[ref_i]
                if any(ref in s for s in self.dir_pdf_list) and (self.doc_type in self.dir_pdf_list):
                    self.match_pdf.append(ref)
                if any(ref not in s for s in self.dir_pdf_list) and (self.doc_type in self.dir_pdf_list):
                    self.missing_pdf.append(ref)
            return "MATCHED QTY: " + str(len(self.match_pdf)) + " MISSNG QTY: " + str(len(self.missing_pdf))

        except error as e:
            return {"status": "fail: " + str(e),
                    "data": {
                        "path": self.absolute_pth_refno,
                    },
                    "message": "FAIL",
                    "code": 422
            }




"""
Version No: 1
Release Date: 28 September 2021 
KKSC

Checks IF REFNO.pdf exist in given path
"""

import os
from os import error

from datetime import datetime
import datetime as date_delta

def current_date_only():
    now = datetime.now() #Get Datetime input
    current_date = datetime.today().strftime('%Y-%m-%d')
    return current_date

def first_previous_date():
    last_day_of_prev_month = datetime.today().replace(day=1) - date_delta.timedelta(days=1)
    start_day_of_prev_month = datetime.today().replace(day=1) - date_delta.timedelta(days=last_day_of_prev_month.day)
    date_only_opt = start_day_of_prev_month.strftime ('%Y-%m-%d')
    return date_only_opt

def pdf_checker(file_path, file_name):
    try:
        res = {"status": "success",
                "data": {
                    "filename": file_name,
                    "filepath": file_path
                },
                "message": False,
                "code": 200
            }
        for path, dirs, files in os.walk(file_path):
            for i in range(len(files)):
                abs_path_file = os.path.join(path, files[i])
                time_update = int(os.path.getmtime(abs_path_file))
                timestamp = datetime.fromtimestamp(time_update)
                last_modified = str(timestamp).split(" ")[0] 
                # print(files[i])
                if str(file_name) in str(files[i]) and \
                   files[i].endswith(".pdf") and \
                   last_modified <= current_date_only() and \
                   last_modified >= first_previous_date():
                    res = {"status": "success",
                            "data": {
                                "filename": file_name,
                                "filepath": file_path
                            },
                            "message": True,
                            "code": 200
                    }
                    
        return res
        
    except error as e:
        return {"status": "fail: " + str(e),
                "data": {
                    "filename": file_name,
                    "filepath": file_path
                },
                "message": False,
                "code": 422
        }


def pdf_count(file_path):
    """
    Condition of counter:
    1. MUST BE .pdf
    2. Within Date Range
    """
    try:
        pdf_counter = 0
        res = {"status": "success",
                "data": {
                    "pdf_count": pdf_counter
                },
                "message": False,
                "code": 200
            }
        for path, dirs, files in os.walk(file_path):
            for i in range(len(files)):
                # print(files[i])
                abs_path_file = os.path.join(path, files[i])
                time_update = int(os.path.getmtime(abs_path_file))
                timestamp = datetime.fromtimestamp(time_update)
                last_modified = str(timestamp).split(" ")[0]
                if files[i].endswith(".pdf") and \
                   last_modified <= current_date_only() and \
                   last_modified >= first_previous_date():
                    pdf_counter +=1
                    res = {"status": "success",
                        "data": {
                            "pdf_count": pdf_counter
                        },
                        "message": True,
                        "code": 200
                    }
                
                    
        return res
        
    except error as e:
        return {"status": "fail: " + str(e),
                "data": {
                    "pdf_count": pdf_counter
                },
                "message": "FAIL",
                "code": 422
        }

# Test Run
# print(pdf_checker("/media/b2b/rexbridge-b2b.com/uploads/bataras","GMKCN21090001"))
print(pdf_count(""))

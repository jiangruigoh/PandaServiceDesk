import multiprocessing
import os
import yaml
from dotenv import load_dotenv
load_dotenv()

name = "Panda Service Desk"
accesslog = "/media/estore/fastAPI/PandaServiceDesk/gunicorn-access.log"
errorlog = "/media/estore/fastAPI/PandaServiceDesk/gunicorn-error.log"

"""GET Configuration parameters"""
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    #print(cfg)

# UVICON Configuration Variables
uvicorn_host = cfg["uvicorn"]["host"]
uvicorn_port = cfg["uvicorn"]["port"]
uvicorn_reload_status = cfg["uvicorn"]["reload"]

# Closing File
ymlfile.close()

bind = str(uvicorn_host) + ":" + str(uvicorn_port)

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 9999
keepalive = 2

debug = os.environ.get("debug", "false") == "true"
reload = debug
preload_app = False
daemon = False

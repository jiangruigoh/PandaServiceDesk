#!/bin/bash
cd "/media/data/fastAPI/PandaServiceDesk/panda_task_agent"
daily_local_main_run_sqldump.py
echo "Sqldump Task executed!"
exit
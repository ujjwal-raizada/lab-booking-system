import pathlib
import datetime
import os
from shutil import copyfile

# This script will be called by pythonanywhere tasks handler (or any other cron job)
# once a day.

cwd = os.path.abspath(os.path.dirname(__file__))
os.chdir(cwd)

backup_dir = pathlib.Path('backups')
backup_dir.mkdir(parents=True, exist_ok=True)

date = datetime.datetime.now().strftime("%Y-%m-%d")

source = pathlib.Path('server/db.sqlite3')
dest = pathlib.Path('backups/db_backup_' + date)

copyfile(source, dest)
print("database backup created: ", dest)

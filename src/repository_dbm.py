from pathlib import Path
import dbm

DB_FILENAME = "database.dbm"
DB_PATH = Path() / ".." / "db" / DB_FILENAME

db = None


def get_engine():

    db = open(DB_PATH, "c")


def shutdown():
    db.close()

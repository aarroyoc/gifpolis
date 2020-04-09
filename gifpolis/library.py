from gifpolis.file import File
from pathlib import Path
import sqlite3
import shutil
import uuid

class Library:
    def __init__(self):
        self.sql = dict()
        self.sql["init"] = open("gifpolis/init.sql").read()
        self.sql["search"] = open("gifpolis/search.sql").read()
        self.sql["get-all"] = open("gifpolis/get-all.sql").read()
        self.sql["insert-gif"] = open("gifpolis/insert-gif.sql").read()

        self.storage_dir = Path.home() / ".gifpolis"
        if not self.storage_dir.exists():
            self.storage_dir.mkdir()
        self.storage_file = self.storage_dir / "gifpolis.db"
        if not self.storage_file.exists():
            self.init_database()

        self.db = sqlite3.connect(self.storage_file)
       
    def init_database(self):
        db = sqlite3.connect(self.storage_file)
        c = db.cursor()
        c.execute(self.sql["init"])
        db.commit()
        db.close()

    def search(self, query):
        c = self.db.cursor()
        if query:
            final_query = query + "*"
            c.execute(self.sql["search"], final_query)
        else:
            c.execute(self.sql["get-all"])
        
        return list(map(lambda x: File(x[0], x[1]), c.fetchall()))

    def save_file(self, description, filename):
        path_filename = Path(filename)
        gif_id = str(uuid.uuid1())
        new_filename = self.storage_dir / (gif_id + path_filename.suffix)
        shutil.copyfile(path_filename, new_filename)
        c = self.db.cursor()
        c.execute(self.sql["insert-gif"], (gif_id, description, str(new_filename)))
        self.db.commit()


        
import sqlite3

from config import *

conn = sqlite3.connect(ADMIN_DB, check_same_thread=False)
c = conn.cursor()


class User:
    def __init__(self):
        self.l = []

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, action TEXT)")
            conn.commit()
        else:
            pass

    def data_entry(self, n, action):
        c.execute("INSERT INTO admin_log(name, action) VALUES (?, ?)",
            (n, action))
        conn.commit()


    def read_all(self):
        c.execute("SELECT * FROM admin_log")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
            print(row)
        return self.l

# MemoryUnit().read_all()
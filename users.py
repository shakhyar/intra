import sqlite3

from config import *

conn = sqlite3.connect(USER_DB, check_same_thread=False)
c = conn.cursor()

"""
'name'
'std'
'school'
'email'
'ph1'
'ph2'
'prc'
'prp'
'exp'
'fp'
'notes'
'paid'
'secret'
"""
class User:
    def __init__(self):
        self.l = []

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, std TEXT, school TEXT, email TEXT, password TEXT, ph1 INT, ph2 INT, prc TEXT, prp TEXT, exp TEXT, fp TEXT, notes TEXT, paid INT, secret TEXT)")
            conn.commit()
        else:
            pass

    def data_entry(self, n, std, school, email, passw, ph1, ph2, prc, prp, exp, fp, notes, paid, secret):
        c.execute("INSERT INTO users(name, std, school, email, password, ph1, ph2, prc, prp, exp, fp, notes, paid, secret) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (n, std, school, email, passw, ph1, ph2, prc, prp, exp, fp, notes, paid, secret))
        conn.commit()


    def read_all(self):
        c.execute("SELECT * FROM users")
        self.l = []
        for row in c.fetchall():
            self.l.append(row)
            print(row)
        return self.l

    def delete_entry(self, secret):
        self.pid = secret
        c.execute("DELETE from users where secret = ?", (self.pid,))
        conn.commit()

    def update_entry(self, secret):
        self.secret = secret
        c.execute("UPDATE users SET paid = 1 WHERE secret = ?",(self.secret,))
        conn.commit()

    def read(self, name):
        self.name = name
        try:
            c.execute("SELECT * FROM users where name = ?", (self.name,))
            cs = c.fetchone()
            return [cs[0], cs[13]]
        except IndexError:
            return [None, None]

    def validate(self, ph1):
        try:
            self.ph1 = ph1
            c.execute("SELECT * FROM users where ph1 = ?", (self.ph1,))
            cs = c.fetchone()
            return [cs[0], cs[4], cs[13]]
        except IndexError:
            return [None, None]
# MemoryUnit().read_all()
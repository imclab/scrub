import hashlib
import sqlite3

class Scrubber:
    """
    Scrubs a list of todo items
    """
    
    def __init__(self):
        self.__create_db()
    
    def init(self):
        """
        Initializes the todo list.
        """

        self.__init_db()
    
    def scrub(self):
        """
        Scrubs the items in the todo list flagged as 'today' or 'later'.
        """

        con = sqlite3.connect('todo.db')
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('select * from items where flag is not "n"')
            rows = cur.fetchall()
            for row in rows:
                flag = raw_input(row['memo'] + '? (t,l,n) ')
                cur.execute('update items set flag = ? where id = ?', (flag, row['id']))
    
    def add(self, items, flag = 'l'):
        """
        Adds an item to the todo list.
        """

        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            for item in items:
                h = hashlib.md5()
                h.update(item)
                cur.execute('insert into items(hash, flag, memo) values (?, ?, ?)', (h.hexdigest()[0:8], flag, item))
    
    def get(self, flag = None):
        """
        Gets all of the items in the todo list. 
        If 'flag' is set, then only gets items with that flag.
        """

        con = sqlite3.connect('todo.db')
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            if flag is None:
                cur.execute('select * from items')
            else:
                cur.execute('select * from items where flag = ?', [flag])
            rows = cur.fetchall()
            for row in rows:
                print "%s %s" % (row['hash'], row['memo'])

    def remove(self, hashvals):
        """
        Removes a todo item by hash value.
        """

        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            for h in hashvals:
                cur.execute('delete from items where hash = ?', [h])
    
    def __create_db(self):
        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            cur.execute('create table if not exists items(id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, flag TEXT, memo TEXT)')
    
    def __init_db(self):
        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            cur.execute('drop table if exists items')
            cur.execute('create table items(id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, flag TEXT, memo TEXT)')
#! /usr/bin/env python
import sqlite3
import sys

class Scrubber:
    
    """ Scrubs a list of todo items """
    
    def __init__(self):
        self.__create_db()
        pass
    
    def init(self):
        """ Initializes the todo list. """
        self.__init_db()
        pass
    
    def scrub(self):
        """ Scrubs the items in the todo list flagged as 'today' or 'later'. """
        pass
    
    def add(self, item, flag = 't'):
        """ Adds an item to the todo list. """
        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            cur.execute('insert into items(flag, memo) values (?, ?)', (flag, item))
    
    def get(self, flag = None):
        """ 
        Gets all of the items in the todo list. 
        If 'flag' is set, then only gets items with that flag.
        """
        con = sqlite3.connect('todo.db')
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('select * from items')
            rows = cur.fetchall()
            for row in rows:
                print "%s %s %s" % (row['id'], row['flag'], row['memo'])
    
    def __create_db(self):
        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            cur.execute('create table if not exists items(id INTEGER PRIMARY KEY AUTOINCREMENT, flag TEXT, memo TEXT)')
    
    def __init_db(self):
        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            cur.execute('drop table if exists items')
            cur.execute('create table items(id INTEGER PRIMARY KEY AUTOINCREMENT, flag TEXT, memo TEXT)')

if __name__ == "__main__":

    scrubber = Scrubber();

    if len(sys.argv) < 1:
        scrubber.scrub()
    elif sys.argv[1] == '-t':
        scrubber.get('t')
    elif sys.argv[1] == '--init':
        scrubber.init()
    else:
        scrubber.add(sys.argv[1])
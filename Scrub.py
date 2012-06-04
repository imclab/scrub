#! /usr/bin/env python
import argparse
import sqlite3

class Scrubber:
    
    """ Scrubs a list of todo items """
    
    def __init__(self):
        self.__create_db()
    
    def init(self):
        """ Initializes the todo list. """
        self.__init_db()
    
    def scrub(self):
        """ Scrubs the items in the todo list flagged as 'today' or 'later'. """
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
        """ Adds an item to the todo list. """
        con = sqlite3.connect('todo.db')
        with con:
            cur = con.cursor()
            for item in items:
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
            if flag is None:
                cur.execute('select * from items')
            else:
                cur.execute('select * from items where flag = ?', (flag))
            rows = cur.fetchall()
            for row in rows:
                print "%s %s" % (row['flag'], row['memo'])
    
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
    
    parser = argparse.ArgumentParser(description="Scrub is a simple todo list")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', action="store_true")
    group.add_argument('-l', action="store_true")
    parser.add_argument('--init', action="store_true")
    parser.add_argument('memo', action="store", nargs="*")
    
    scrubber = Scrubber()
    args = parser.parse_args()
    
    if args.init: scrubber.init()
    elif args.t: scrubber.get('t')
    elif args.l: scrubber.get('l')
    elif len(args.memo): scrubber.add(args.memo)
    else: scrubber.scrub()
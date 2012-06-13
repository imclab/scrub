#! /usr/bin/env python
from scrub import Scrubber
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="""
        Scrub is a simple todo list
    """)

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-t', action="store_true", help="""
        show todo items flagged 'today'
    """)

    group.add_argument('-l', action="store_true", help="""
        show todo items flagged 'later'
    """)

    group.add_argument('-c', action="store", nargs="*", type=str, metavar="HASH", help="""
        complete a todo item by hash id
    """)

    parser.add_argument('--init', action="store_true", help="""
        initialize the todo list
    """)

    parser.add_argument('memo', action="store", nargs="*", type=str, help="""
        some text to describe a todo item
    """)
    
    scrubber = Scrubber.Scrubber()
    args = parser.parse_args()
    
    if args.init: scrubber.init()
    elif args.t: scrubber.get('t')
    elif args.l: scrubber.get('l')
    elif args.c is not None: scrubber.remove(args.c)
    elif len(args.memo): scrubber.add(args.memo)
    else: scrubber.scrub()
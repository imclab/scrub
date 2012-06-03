#!/bin/sh

echo testing...
clear
./Scrub.py --init
./Scrub.py "Buy Milk"
./Scrub.py "Make Cheese"
./Scrub.py "???"
./Scrub.py "Profit"
./Scrub.py -t
echo done.

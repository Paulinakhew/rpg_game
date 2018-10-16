#!/usr/bin/env python3

import os
def showInstructions():
    #print a main menu and the commands
    print('''
RPG Game
========

Get to the Garden with a key and a potion. 
Avoid the monsters!

Commands:
  go [direction]
  get [item]
''')

def clear_screen():
    os.system('clear')

def riddle():
    print('''
To wield this sword you must prove yourself by answering the following riddle.
    Riddle: I disappear every time you say my name. What am I?''')
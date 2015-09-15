#------------------------------------------------------------------------------
# utils.py -  utilities for simple zero-sum game
#------------------------------------------------------------------------------
import json


def getGameContent():
    with open("parameters.json", 'r') as _file:
        return json.load(_file)

def defaultServerPort():
    return 5556

def defaultHost():
    return "127.0.0.1"
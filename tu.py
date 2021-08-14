#!/usr/bin/env python

from command.Command import Command
from command.Parameters import Parameters
import os
import sys
import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    try:
        Command(Parameters(sys.argv[1:]))
    except BaseException as e:
        print(e)


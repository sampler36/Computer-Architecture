#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# cpu.load('./examples/mult.ls8')  #uncoment for day 2
cpu.load('./examples/call.ls8')  #uncomment for day 4
cpu.run()
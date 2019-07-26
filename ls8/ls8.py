#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# cpu.load('./examples/mult.ls8')  #uncoment for day 2
# cpu.load('./examples/stack.ls8')  #uncoment for day 3
# cpu.load('./examples/call.ls8')  #uncomment for day 4
cpu.load('./examples/sctest.ls8')  #uncomment for day 5
cpu.run()
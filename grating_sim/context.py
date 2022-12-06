"""
Adds the source files to the path for files in any subdirectory
"""
import os
import sys
print("Importing test context manager")

fileLocation = os.path.dirname(os.path.abspath(__file__))
sourceLocation = os.path.abspath(os.path.join(fileLocation, '..', 'source/'))
nkLocation = os.path.abspath(os.path.join(fileLocation, '..', 'nkData/'))
netlistLocation = os.path.abspath(os.path.join(fileLocation, '..', 'netlist/'))
testLocation = os.path.abspath(os.path.join(fileLocation, '..', 'test/'))
baseLocation = os.path.abspath(os.path.join(fileLocation, '../..'))

sys.path.insert(0, sourceLocation)
sys.path.insert(0, baseLocation)
sys.path.insert(0, nkLocation)
sys.path.insert(0, netlistLocation)
sys.path.insert(0, testLocation)

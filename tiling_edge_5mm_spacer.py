#tiling_edge_5mm_spacer.py
from numpy.lib.polynomial import poly
from pandas.core import base
from pandas.io.parsers import read_csv
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 
import math

size = 5  # mm
vertexes = [[0,0],[0,5],[5,5],[5,-5],[-5,-5],[-5,0],[0,0]]
to_print = linear_extrude(15)(polygon(vertexes))

printstring = '$fn=30;\n' + scad_render(to_print)





pyperclip.copy(printstring)

#print("the following has been copied")
#print(scad_render(to_print))
print()

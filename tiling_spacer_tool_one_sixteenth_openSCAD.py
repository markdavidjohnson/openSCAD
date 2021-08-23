#tiling_spacer_tool_one_sixteenth_openSCAD.py
from numpy.lib.polynomial import poly
from pandas.core import base
from pandas.io.parsers import read_csv
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 

thk = 1/16*25.4
width = 20
length = 30
inset = 10
part = resize([20,length,thk])(cube(center=True))
subtract = resize([width-inset,length-inset,thk])(cube(center=True))

to_print = part - subtract

printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

#print("the following has been copied")
#print(scad_render(to_print))
print()

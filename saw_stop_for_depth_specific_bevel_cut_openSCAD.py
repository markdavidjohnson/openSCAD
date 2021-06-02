#saw_stop_for_depth_specific_bevel_cut_openSCAD.py

from solid import *
from solid.utils import *	# Not required, but the utils module is useful
import pyperclip
import math
from shapeFunctions_openSCAD import trapezoidSymmetrical as tzd
import shapeFunctions_openSCAD
import math




part = resize([25,10,20.5])(cube())
to_print = part
#to_print = receiver# + pipe #+ nosebase


printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print() 

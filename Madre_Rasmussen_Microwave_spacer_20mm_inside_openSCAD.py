#Madre_Rasmussen_Microwave_spacer_20mm_inside_openSCAD.py

from solid import *
from solid.utils import *	# Not required, but the utils module is useful
import pyperclip
import math
from shapeFunctions_openSCAD import trapezoidSymmetrical as tzd
import shapeFunctions_openSCAD

negative_space = resize([20,10,10])(cube())
positive_space = left(5)(resize([30,15,10])(cube()))

part = positive_space - negative_space


to_print = part
#to_print = receiver# + pipe #+ nosebase


printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

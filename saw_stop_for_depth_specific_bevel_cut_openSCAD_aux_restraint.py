#saw_stop_for_depth_specific_bevel_cut_openSCAD_aux_restraint.py

from solid import *
from solid.utils import *	# Not required, but the utils module is useful
import pyperclip
import math
from shapeFunctions_openSCAD import trapezoidSymmetrical as tzd
import shapeFunctions_openSCAD
import math

height = 13
thickness = 3
length = 20
cutouth = 3
cutoutl = 10
points = [
    [0,cutouth],
    [0,height],
    [length,height],
    [length,0],
    [length-cutoutl,0],
    [length-cutoutl,cutouth],
    [0,cutouth]
]

part = linear_extrude(thickness)(polygon(points))

to_print = part
#to_print = receiver# + pipe #+ nosebase


printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print() 

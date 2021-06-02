#saw_stop_for_depth_specific_bevel_cut_openSCAD.py

from solid import *
from solid.utils import *	# Not required, but the utils module is useful
import pyperclip
import math
from shapeFunctions_openSCAD import trapezoidSymmetrical as tzd
import shapeFunctions_openSCAD
import math

height = 25
depth = 12
sep = 20.5
#sep =5
part = resize([depth,sep,height])(cube())
thkx = 3
gap =16.2
width = 5

clips = []
clips.append(resize([depth,width,thkx])(cube()))
clips.append(resize([depth,width,thkx])(cube()))
for i in range(len(clips)):
    clips[i] = back(width-1)(clips[i])
    angle_to_eachother = 7
    angle = -angle_to_eachother*i + angle_to_eachother/2
    clips[i] = rotate([-angle,0,0])(clips[i])
    clips[i] = up((thkx + gap)*i)(clips[i])

for i in clips:
    part += i
to_print = part
#to_print = receiver# + pipe #+ nosebase


printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print() 

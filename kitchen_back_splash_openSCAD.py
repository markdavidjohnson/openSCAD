#kitchen_back_splash_openSCAD.py
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 
import random

dims = []

max_height = 85
thk = 1

dims.append([133,max_height])
dims.append([89.5,29.2])
dims.append([6.0,85])
dims.append([106.2,42.8])
dims.append([121.9,42.1])
dims.append([76.3,56.5])
dims.append([60.8,42.5])

parts = []
running_x_pos = 0
for i in dims:
    parts.append([up(random.random()*5)(resize([i[0],i[1],thk])(cube())),running_x_pos])
    running_x_pos += i[0]

to_print=parts[0]
for i,item in enumerate(parts):
    to_print += right(item[1])(item[0])

#INCHES
rolly = 17.7
rollx_small = 118.1  # 196.9, 314.9
#rollx = 196.9  # 196.9, 314.9
#NOW CM
rollx_small, rolly = rollx_small*2.54,rolly*2.54

#piece 1
roll_small = down(5)(back(0)(up(random.random()*5)(resize([rollx_small,rolly,thk])(cube()))))
roll_small = color([0,0,255,255])(roll_small)
to_print += roll_small

#piece 2
roll_small = right(rollx_small)(down(5)(back(0)(up(random.random()*5)(resize([rollx_small,rolly,thk])(cube())))))
roll_small = color([random.random()*255,random.random()*255,random.random()*255,255])(roll_small)
to_print += roll_small

#piece 3
roll_small = right(0)(down(5)(forward(rolly)(up(random.random()*5)(resize([rollx_small,rolly,thk])(cube())))))
roll_small = color([random.random()*255,random.random()*255,random.random()*255,255])(roll_small)
to_print += roll_small

to_print += color([255,0,0,255])(right(329)(resize([2,100,thk])(cube())))

printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

#Madre_Rasmussen_Microwave_Hinge_Part_v2_openSCAD.py

from solid import *
from solid.utils import *	# Not required, but the utils module is useful
import pyperclip
import math
from shapeFunctions_openSCAD import trapezoidSymmetrical as tzd
import shapeFunctions_openSCAD

import pandas as pd
Cutout = 'Madre_Rasmussen_Microwave_Hinge_Part_Cutout.csv'
Hole = 'Madre_Rasmussen_Microwave_Hinge_Part_Hole.csv'
Main = 'Madre_Rasmussen_Microwave_Hinge_Part_Main.csv'
Base = 'Madre_Rasmussen_Microwave_Hinge_Part_Base.csv'
Step = 'Madre_Rasmussen_Microwave_Hinge_Part_Step.csv'

dfc = pd.read_csv(Cutout)[['X','Y']]
dfh = pd.read_csv(Hole)[['X','Y']]
dfm = pd.read_csv(Main)[['X','Y']]
dfb = pd.read_csv(Base)[['X','Y']]
dfs = pd.read_csv(Step)[['X','Y']]

print(dfc)


list_cutout = dfc.values.tolist()
list_cutout.append(list_cutout[0])
list_hole = dfh.values.tolist()
list_hole.append(list_hole[0])
list_main = dfm.values.tolist()
list_main.append(list_main[0])
list_base = dfb.values.tolist()
list_base.append(list_base[0])
list_step = dfs.values.tolist()
list_step.append(list_step[0])

total_rotate_angle = -47
total_forward_dist = 11.5


main = down(1)(linear_extrude(1.5)(polygon(list_main)))
main = mirror([0,0,1])(main)
main = rotate([0,0,total_rotate_angle])(main)
main = forward(total_forward_dist)(main)

cutout = up(0)(linear_extrude(4)(polygon(list_cutout)))
cutout = mirror([0,0,1])(cutout)
cutout = rotate([0,0,total_rotate_angle])(cutout)
cutout = forward(total_forward_dist)(cutout)
angle = 13
cutout = rotate([0,angle,0])(cutout)
cutout = up(math.tan(angle * pi / 180)*45+1-.8)(cutout)


hole = down(3)(linear_extrude(10)(polygon(list_hole)))
hole = mirror([0,0,1])(hole)
hole = rotate([0,0,total_rotate_angle])(hole)
hole = forward(total_forward_dist)(hole)
shift_distance = 1.5
hole = back(shift_distance)(hole)
cutout = back(shift_distance)(cutout)


step = down(1)(linear_extrude(4)(polygon(list_step)))
step = rotate([0,0,total_rotate_angle])(step)
step = forward(total_forward_dist)(step)

base = left(6.25)(forward(7.25)(down(1)(linear_extrude(10)(polygon(list_base)))))
base = rotate([0,0,total_rotate_angle])(base)
base = forward(total_forward_dist)(base)
angle = -4  #was +8
base = up(math.tan(angle * pi / 180)*57-.2)(base)
base = rotate([0,angle,0])(base)
part = base

part += step

main = back(12)(rotate([180,0,0])(main))
part += main

#hole = right(8.19-(3.6-1.4))(hole)
hole_shift_distance = 1
hole = right(hole_shift_distance)(hole)
cutout = right(hole_shift_distance)(cutout)

part -= cutout + hole
part -= back(50)(down(3)(resize([100,100,2])(cube())))

to_print = part
#to_print = receiver# + pipe #+ nosebase


printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

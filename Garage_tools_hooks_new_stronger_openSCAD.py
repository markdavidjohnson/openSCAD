#Garage_tools_hooks_new_stronger_openSCAD
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip

#Garage_tools_hooks_new.stl
#the triangles
boxInnerYmax = 27
boxInnerXmax = 27
boxInnerXmin = 0
boxInnerYmin = 0
thk = 0
wall_thickness = 3
zzz = polygon(points=[
    [boxInnerXmin-thk,boxInnerYmin-thk],
    [boxInnerXmax+thk,boxInnerYmin-thk],
    [boxInnerXmin+thk,boxInnerYmax+thk],
    [boxInnerXmin-thk,boxInnerYmin-thk]
    ])
zzz = linear_extrude(wall_thickness)(zzz)

#now cut out the hollow space
hollow_thk = 3
hollow_space = polygon(points=[
    [boxInnerXmin + hollow_thk,boxInnerYmin + hollow_thk],
    [boxInnerXmax-hollow_thk*2*2**.5,boxInnerYmin + hollow_thk],
    [boxInnerXmin + hollow_thk,boxInnerYmax-hollow_thk*2*2**.5],
    [boxInnerXmin + hollow_thk,boxInnerYmin + hollow_thk],
    ])
hollow_space = linear_extrude(wall_thickness)(hollow_space)
zzz -= hollow_space


spacing = 10
zzz = up(spacing/2)(zzz)

#add the part that rests on the wall, interfacing with the screw
thk_off_wall = hollow_thk
box_x_min = 0
box_x_inner_min = box_x_min + hollow_thk
box_x_max = boxInnerXmax
box_x_inner_max = box_x_max - hollow_thk
box_z_min = 0
box_z_max = spacing/2
box_z_inner_max = box_z_max - hollow_thk
screw_interface = polygon(points=[
    [box_x_min,box_z_min],
    [box_x_inner_min,box_z_min],
    [box_x_inner_min,box_z_inner_max],
    [box_x_inner_max,box_z_inner_max],
    [box_x_inner_max,box_z_min],
    [box_x_max,box_z_min],
    [box_x_max,box_z_max],
    [box_x_min,box_z_max],
    [box_x_min,box_z_min]
    ])
screw_interface = linear_extrude(thk_off_wall)(screw_interface)
screw_interface = forward(thk_off_wall)(rotate([90,0,0])(screw_interface))
zzz += screw_interface

#Reinforcement piece
zzz += forward(7)(resize([1,2,spacing/2])(cube()))
zzz += mirror([0,0,1])(zzz)


to_print = zzz

printstring = '$fn=100;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

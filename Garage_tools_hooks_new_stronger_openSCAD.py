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
overhang = boxInnerXmax/8  # to make it an obtuse angle
thk = 0
wall_thickness = 5
main_triangle_points = [
    [boxInnerXmin-thk,boxInnerYmin-thk],
    [boxInnerXmax+thk,boxInnerYmin-thk],
    [boxInnerXmin+thk-overhang,boxInnerYmax+thk],
    [boxInnerXmin-thk,boxInnerYmin-thk]
    ]
zzz = polygon(points=main_triangle_points)
zzz = linear_extrude(wall_thickness)(zzz)


#now cut out the hollow space
hollow_thk = 3
'''
hollow_space = polygon(points=[
    [boxInnerXmin + hollow_thk,boxInnerYmin + hollow_thk],
    [boxInnerXmax-hollow_thk*2*2**.5,boxInnerYmin + hollow_thk],
    [boxInnerXmin + hollow_thk - overhang*.7,boxInnerYmax-hollow_thk*2*2**.5],
    [boxInnerXmin + hollow_thk,boxInnerYmin + hollow_thk],
    ])
hollow_space = linear_extrude(wall_thickness)(hollow_space)
zzz -= hollow_space
'''

spacing = 10
zzz = up(spacing/2)(zzz)

#add the part that rests on the wall, interfacing with the screw
thk_off_wall = hollow_thk
box_x_min = -1
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
zzz += left(3)(forward(7)(resize([5,2,spacing/2])(cube())))

#flattening cutting peice
fcp = polygon(points=[
    [boxInnerXmin,boxInnerYmin],
    [-boxInnerXmax,boxInnerYmin],
    [boxInnerXmin-overhang,boxInnerYmax],
    [boxInnerXmin,boxInnerYmin]
    ])
fcp = linear_extrude(20)(fcp)
zzz -= fcp

#round the tip a bit
tipx, tipy = main_triangle_points[2][0],main_triangle_points[2][1]
print(tipx, tipy)
tip_rounding_feature = polygon(points=[
    [tipx,tipy],
    [tipx-2,tipy],
    [tipx-2.5,tipy-.5],
    [tipx-2.5,tipy-2],
    [tipx+1,tipy-5],
    [tipx,tipy]
    ])
tip_rounding_feature = up(spacing/2)(linear_extrude(wall_thickness)(tip_rounding_feature))
zzz += tip_rounding_feature


#mirror symmetry
zzz += mirror([0,0,1])(zzz)

zzz = rotate([90,0,0])(zzz)

to_print = zzz

printstring = '$fn=100;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

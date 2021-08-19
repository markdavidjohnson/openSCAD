#disc_golf_contact_lens_disc_holder_openSCAD.py
from numpy.lib.polynomial import poly
from pandas.core import base
from pandas.io.parsers import read_csv
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 

#https://mvpdiscsports.com/discs/deflector/
Deflector_D = 21.5*10
Deflector_H = 14.5
#https://www.dynamicdiscs.com/collections/dynamic-discs-felon
Felon_D = 21.2*10
Felon_H = 1.8*10

basethk=10
height=25+basethk
inner_radius = 8.5/2*25.4+8
inner_radius = max(Felon_D/2,Deflector_D/2)+4
outer_radius = inner_radius + 4
cap_bottomer_height = basethk
cap_bottomer_r = outer_radius+3
part = cylinder(r=outer_radius,h=height) - cylinder(r=inner_radius,h=height)
part += cylinder(r=outer_radius,h=basethk)
part += cylinder(r=cap_bottomer_r,h=cap_bottomer_height) 

chamfer_size =3
cap_bottomer_r = cap_bottomer_r+.1
chamfer_circle = polygon([[cap_bottomer_r,0],[cap_bottomer_r,chamfer_size],[cap_bottomer_r-chamfer_size,0],[cap_bottomer_r,0]])
chamfer_circle = rotate_extrude()(chamfer_circle)
part -= chamfer_circle

rightward_distance = outer_radius + 15
part = right(rightward_distance)(part)


#now let's get that arc that connects the two halves

connector_radius = 500
connector = cylinder(r=connector_radius,h=basethk)
connector_back = connector_radius-outer_radius-20+10
connector = back(connector_back)(connector)

chamfer_size =3
chamfer_large = polygon([[connector_radius,0],[connector_radius,chamfer_size],[connector_radius-chamfer_size,0],[connector_radius,0]])
chamfer_large = rotate_extrude()(chamfer_large)
chamfer_large = back(connector_back)(chamfer_large)
connector -= chamfer_large

connector_neg_r = connector_radius*.4
connector_neg = cylinder(r=connector_neg_r,h=basethk)
connector_neg_back = connector_neg_r-outer_radius-10+outer_radius*2-25
connector_neg = back(connector_neg_back)(connector_neg)

chamfer_size =3
chamfer_small = polygon([[connector_neg_r,0],[connector_neg_r+chamfer_size,0],[connector_neg_r,chamfer_size],[connector_neg_r,0]])
chamfer_small = rotate_extrude()(chamfer_small)
chamfer_small = back(connector_neg_back)(chamfer_small)
connector_neg += chamfer_small

connector = connector - connector_neg

connector_cutter = linear_extrude(basethk)(polygon([[0,0],[500,1000],[500,-3000],[-3000,-3000],[-3000,3000],[0,3000],[0,0]]))
connector_cutter = back(connector_neg_back)(connector_cutter)
connector -= connector_cutter

part += connector


#so far we've only been creating the right side, mirroring gives us an identical left side
part += mirror([1,0,0])(part)

# this whole section here is for creating the subtraction objects to subset down the part
# so that it will fit on my printer's bed, 200x200mm
dim = 1000
sectioner1 = resize([dim,dim,dim])(cube())
sL__s = back(200)(left(rightward_distance)(sectioner1))        # shows only the extreme left
sR__s = back(200)(left(dim - rightward_distance)(sectioner1))  # shows the extreme right
s_L_s = back(200)(left(0)(sectioner1))                         # shows the left half
s_R_s = back(200)(left(dim)(sectioner1))                       # shows the right half
s__Ts = back(0)(left(dim/2)(sectioner1))                       # shows the top
s__Bs = back(dim)(left(dim/2)(sectioner1))                     # shows the bottom
sLL__s = back(200)(left(rightward_distance+dim)(sectioner1))   # useful for hiding the extreme left
sRR__s = back(200)(right(rightward_distance)(sectioner1))      # useful for hiding the extreme right

llb = sL__s + s__Ts                                            # left left bottom
llt = sL__s + s__Bs                                            # left left top
lrb = s_L_s + s__Ts + sLL__s                                   # left right bottom
lrt = s_L_s + s__Bs + sLL__s                                   # left right top
rrb = sR__s + s__Ts                                            # right right bottom
rrt = sR__s + s__Bs                                            # right right top
rlb = s_R_s + s__Ts + sRR__s                                   # right left bottom
rlt = s_R_s + s__Bs + sRR__s                                   # right left top

part = part - rlt  # use this line to select the section of the whole part to show eg: part = part - lrt



# now we finish it off by converting the above code into openSCAD code 
# and copying it to the clipboard

to_print = part

printstring = '$fn=300;\n' + scad_render(to_print)
pyperclip.copy(printstring)

#print("the following has been copied")
#print(scad_render(to_print))
print()

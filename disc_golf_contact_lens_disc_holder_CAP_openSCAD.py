#disc_golf_contact_lens_disc_holder_CAP_openSCAD.py
from numpy.lib.polynomial import poly
from pandas.core import base
from pandas.io.parsers import read_csv
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 
import math

def dprint(listy):
    ostr = ''
    for i in listy:
        #print(i)
        out = str(i)
        out += ' '*(10-len(out)) + '|'
        ostr += out
    print(ostr)

#this next import will copy to the clipboard the SCAD code for the base
import disc_golf_contact_lens_disc_holder_BASE_openSCAD
base_code = pyperclip.paste()

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

cap_height = height-basethk
cap_inner_radius = outer_radius+1
cap_outer_radius = cap_inner_radius+5

cap_thk=3
part = cylinder(r=cap_outer_radius,h=cap_height) - cylinder(r=cap_inner_radius,h=cap_height)
brim = cylinder(r=cap_outer_radius,h=cap_thk) - cylinder(r=cap_outer_radius-10,h=cap_thk)
brim = up(cap_height)(brim)
part += brim


texture_half_width = 8/2
texture_depth = (cap_outer_radius-cap_inner_radius)*.4

polygon_list = []
#model_texture = [[cap_outer_radius,texture_half_width],[cap_outer_radius-texture_depth,0],[cap_outer_radius,-texture_half_width],[cap_outer_radius,texture_half_width]]
model_texture = [
                    
                    
                    [cap_outer_radius,texture_half_width],
                    [cap_outer_radius-texture_depth,0],
                    [cap_outer_radius,-texture_half_width]
                ]

angle = 15
texture_polygon = []
for i in range(int(360/angle)):
    rad_angle = i*math.radians(angle)
    deg_angle = i*angle
    #add post
    p1x = model_texture[0][0]*math.cos(rad_angle)*2
    p1y = model_texture[0][1]*math.sin(rad_angle)*2
    x = model_texture[0][0]
    y = model_texture[0][1]
    p1x = x * math.cos(rad_angle) + y * math.sin(rad_angle)
    p1y = -x * math.sin(rad_angle) + y * math.cos(rad_angle)
    texture_polygon.append([p1x,p1y])

    for index in range(len(model_texture)):
        x = model_texture[index][0]
        y = model_texture[index][1]
        p1x = x * math.cos(rad_angle) + y * math.sin(rad_angle)
        p1y = -x * math.sin(rad_angle) + y * math.cos(rad_angle)
        texture_polygon.append([p1x,p1y])

        dprint(['dprint',
            deg_angle,
            round(p1x,3),
            round(p1y,3),
            i,
            index,
            model_texture[index][0],
            model_texture[index][1]
            ])
    
    x = model_texture[-1][0]
    y = model_texture[-1][1]
    p1x = x * math.cos(rad_angle) + y * math.sin(rad_angle)
    p1y = -x * math.sin(rad_angle) + y * math.cos(rad_angle)
    texture_polygon.append([p1x,p1y])



texture_polygon.append([model_texture[0][0],model_texture[0][1]])
texture_height = height*3
texture = linear_extrude(texture_height)(polygon(texture_polygon))
texture = cylinder(r=cap_outer_radius*2,h=texture_height) - texture
part -= texture





def indicator_text(letter):
    global cap_outer_radius
    global cap_height
    text_size = 170
    lid = cylinder(r=cap_outer_radius-4,h=3)
    if letter == "R":
        lid -= back(text_size/2*.95)(left(text_size/3*1.5)(up(2)(linear_extrude(5)(text(letter,text_size)))))
    elif letter == "L":
        lid -= back(text_size/2*.95)(left(text_size/3*1.2)(up(2)(linear_extrude(5)(text(letter,text_size)))))
    lid = up(cap_height+4)(lid)
    return lid

Llid = indicator_text("L")
Rlid = indicator_text("R")

Rpart = part + Rlid
Lpart = part + Llid







#move it into position relateive to the base
Rpart = up(13)(right(outer_radius + 15)(Rpart))

Lpart = up(13)(left(outer_radius + 15)(Lpart))
#Lpart += Llid

to_print = Rpart + Lpart


printstring = '$fn=30;\n' + scad_render(to_print) + base_code
pyperclip.copy(printstring)

#print("the following has been copied")
#print(scad_render(to_print))
print()

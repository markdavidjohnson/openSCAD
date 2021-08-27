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

display_goal = 'display_all'  # 'print_sections' or 'display_all'

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
    cap_thickness = .7
    lid = cylinder(r=cap_outer_radius-4,h=cap_thickness)
    if letter == "R":
        lid += back(text_size/2*.95)(left(text_size/3*1.5)(up(cap_thickness)(linear_extrude(.3)(text(letter,text_size)))))
    elif letter == "L":
        lid += back(text_size/2*.95)(left(text_size/3*1.2)(up(cap_thickness)(linear_extrude(.3)(text(letter,text_size)))))
    lid = up(cap_height+4)(lid)
    return lid

Llid = indicator_text("L")
Rlid = indicator_text("R")
#Rlid, Llid = up(cap_height+20)(Rlid), up(cap_height+20)(Llid)


upward_move = 13
outward_move_additional = 15

if display_goal == 'display_all':
    Rpart = part + Rlid
    Lpart = part + Llid


    #move it into position relateive to the base
    
    Rpart += Rlid
    Lpart += Llid
    
    Rpart = up(upward_move)(right(outer_radius + outward_move_additional)(Rpart))
    Lpart = up(upward_move)(left(outer_radius + outward_move_additional)(Lpart))
    

    Rpart = color([1,1,1])(Rpart)
    Lpart = color([(224/255),(89/255),(186/255)])(Lpart)

    to_print = Rpart + Lpart
    

    printstring = '$fn=30;\n' + scad_render(to_print) + base_code

elif display_goal == 'print_sections':

    rightward_distance = outer_radius + outward_move_additional

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

    all_occluders = [llb,llt,lrb,lrt,rrb,rrt,rlb,rlt]
    all_occluders_dict = { "llb": llb, "llt": llt, "lrb": lrb, "lrt": lrt, "rrb": rrb, "rrt": rrt, "rlb": rlb, "rlt": rlt}
    
    
    Rpart = part# + Rlid
    Lpart = part# + Llid

    Rpart = Rlid
    Lpart = Llid


    #move it into position relateive to the base
    Rpart = up(upward_move)(right(outer_radius + outward_move_additional)(Rpart))

    Lpart = up(upward_move)(left(outer_radius + outward_move_additional)(Lpart))
    #Lpart += Llid

    bulk_export = True
    if bulk_export:
        for occluder_iterator in all_occluders_dict.keys():
            to_print = Rpart + Lpart - all_occluders_dict[occluder_iterator]

            printstring = '$fn=300;\n' + scad_render(to_print)
            fname = '/Users/MarkJohnson/Downloads/my_cap_' + occluder_iterator + '_colter_ironing_thin'
            with open(fname + '.scad', 'w') as f:
                f.write(printstring)
            #sadly, openscad doesnt seem to work with terminal for Mac, just command line for Windows
            #https://apple.stackexchange.com/questions/175855/is-there-a-way-to-make-open-a-pass-command-line-arguments-to-the-app-it-launc
            #import os
            #os.system('/Applications/OpenSCAD.app -o ' + fname + '.stl ' + fname + '.scad')
            #open -a openscad --o "/Users/MarkJohnson/Downloads/my_cap_rrt_colter_ironing_2mm.scad" "/Users/MarkJohnson/Downloads/my_cap_rrt_colter_ironing_2mm.stl"


    else:
    
        to_print = Rpart + Lpart - lrb

        printstring = '$fn=30;\n' + scad_render(to_print)





pyperclip.copy(printstring)

#print("the following has been copied")
#print(scad_render(to_print))
print()

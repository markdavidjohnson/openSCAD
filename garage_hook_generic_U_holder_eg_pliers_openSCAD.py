#garage_hook_generic_U_holder_eg_pliers_openSCAD.py
from numpy.lib.polynomial import poly
from pandas.io.parsers import read_csv
from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 

'''
I use this script to create batches of parametrically defined tool hooks. It 
outputs the hooks as openSCAD code in a compact arrangement fit for a 200x200mm 
printer.

see an example of the file in this github titled garage_hook_generator_settings
for an example on how to build your own csv settings file.
'''

path = '/Users/MarkJohnson/Downloads/garage_hook_generator_settings - Sheet1.csv'
path = '/Users/MarkJohnson/Downloads/garage_hook_generator_settings - Sheet1 (1).csv'
path = '/Users/MarkJohnson/Downloads/garage_hook_generator_settings - Sheet1 (5).csv'
#df = read_csv(path).loc[3,14]
df = pd.read_csv(path)
output_shapes = []
for i,row in df.iterrows():
    #if i > 2:  # use this line to test and debug the first few clips before going big
    #    continue
    if row['1_for_print'] != 1:  # only print rows with 1 here
        print('skipping row ', i, 'due to not having a 1, instead it has', row['1_for_print'])
        continue
    blank_values = False
    blank_cols = []
    for coly in df.columns:
        if pd.isna(row[coly]):
            blank_values = True
            blank_cols.append(coly)
    if blank_values:
        print('skipping row index', i, 'due to blank values in:', str(blank_cols))
        continue
    halft_width = row.full_width/2 #53.5/2  #59.5/2 #35/2 #38/2 #31.5/2
    thk = max(1.6,halft_width / ((31.5/2) / 1.2))  # i like this ratio to the overall size, but feel free to modify
    gripper_type = row.gripper_type# 'straight'  # 'curved' or 'straight'
    #only used for gripper_type = 'straight'
    gripper_length = row.gripper_length_without_screw_space + 3
    gripper_center_wall_offset = row.gripper_center_wall_offset
    gripper_tip_radius = thk
    base_height = row.base_height
    gripper_height = row.gripper_height

    backplate = resize([halft_width,thk,base_height])(cube())

    if gripper_type == 'curved':
        radius = halft_width*2
        forward_dist = halft_width*.6
        gripper = cylinder(r=halft_width+thk,h=gripper_height) - cylinder(r=halft_width,h=gripper_height)
        gripper_cutter = resize([100,100,100])(cube())
        gripper_cutter = forward(forward_dist)(down(50)(left(50)(gripper_cutter)))
        gripper_cutter += mirror([0,1,0])(gripper_cutter) + rotate([0,0,90])(gripper_cutter)
        gripper -= gripper_cutter
        gripper = forward(forward_dist+gripper_center_wall_offset)(gripper)
        gripper = scale([1,.7,1])(gripper)
        gripper_leg = right(halft_width)(resize([thk,gripper_center_wall_offset,gripper_height])(cube()))
        gripper += gripper_leg
    elif gripper_type == 'straight':
        gripper = resize([thk,gripper_length+gripper_tip_radius,gripper_height])(cube())
        forward_dist = 0 # halft_width*.6
        gripper_tip = cylinder(r=gripper_tip_radius,h=gripper_height)
        gripper_tip = forward(gripper_length+gripper_tip_radius)(gripper_tip)
        rounding_feature = linear_extrude(gripper_height)(polygon([[halft_width,gripper_length+gripper_tip_radius],[halft_width,gripper_length+gripper_tip_radius*2],[halft_width+thk,gripper_length+gripper_tip_radius]]))
        gripper += gripper_tip
        gripper = right(halft_width)(gripper) + rounding_feature
    else:
        print('no gripper_type recognized, please edit the variable assignment')

    screw_hole_radius = 1.5
    screw_hole = cylinder(r=screw_hole_radius,h=base_height)
    screw_hole = rotate([90,0,0])(screw_hole)
    screw_hole = up(base_height/2)(screw_hole)
    screw_hole = forward(base_height/2)(screw_hole)
    backplate -= screw_hole

    mypart = backplate + gripper
    mypart += mirror([1,0,0])(mypart)

    output_shapes.append([mypart,halft_width,gripper_length])

xloc = 0
yloc = 0
max_gripper_length = 0
for i,item in enumerate(output_shapes):
    if i == 0:
        print('added first')
        to_print = item[0]
    else:
        old_half_width = output_shapes[i-1][1]
        new_half_width = output_shapes[i][1]
        max_gripper_length = max(max_gripper_length,output_shapes[i][2])
        new_offset = old_half_width + new_half_width
        xloc += new_offset + 6
        print(i,'new_offset',xloc)
        if xloc + new_half_width + 4 > 200:
            print('we over 200',xloc,yloc)
            xloc = 0
            yloc += max_gripper_length+10
            max_gripper_length = 0
        to_print += forward(yloc)(right(xloc)(item[0]))

printstring = '$fn=30;\n' + scad_render(to_print)
pyperclip.copy(printstring)

#print("the following has been copied")
#print(scad_render(to_print))
print()

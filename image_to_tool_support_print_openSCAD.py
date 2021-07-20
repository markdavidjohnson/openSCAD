#image_to_tool_support_print_openSCAD.py

'''
How to use this:
Take a picture of a tool with a white background, and a standard cheap plastic ruler with it. 
Try to minimize distortion, and put the camera 1 meter above the subject, cropping down to 
have only the tool, ruler, and white background.

Then update the paths and run. It will ask you which outlines is the ruler for scaling purposes
and which one is the tool you want to create a shadow for.

The best method by far, if you can, is to put a computer screen on a table, protect it with 
parchment paper or some other translucent material (also important for eliminating pixel lines)
and putting the tools (gently) on the screen. In a dark room, this eliminates the shadows that
otherwise could mess up your outline.

you also need to have a csv file with settings if you want to use this new bulk version, you can 
see an example of the file in this github
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt
from solid.objects import linear_extrude, polygon

from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 

import webbrowser
import random



#general settings
image_path = '/Users/MarkJohnson/Downloads/IMG_6639.jpg'
use_last_identified_contours = True  # True or False
last_identified_contour_path = "image_to_tool_support_print_openSCAD_last_identified_contour.csv"
tool_outline_extrude_distance = .5
#subtraction object settings
use_subtraction_objects = False
expected_ruler_area = 9300  # units: mm^2
#setting for light color slow mode
use_light_color_mode = True


#creating the path to save out identified contours for faster processing in light color slow mode
updated_path = image_path.replace(image_path[-4:],'_contoured'+image_path[-4:])

if not use_last_identified_contours:
    img = cv2.imread(image_path)
elif use_last_identified_contours:
    img = cv2.imread(updated_path)
    '''
    # optional cropping step
    x=400
    w=2300
    y=1400
    h=1000
    img = img[y:y+h, x:x+w]
    '''

# converting image into grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

if not use_last_identified_contours:
    if use_light_color_mode:
        #finding yellows and other light colors and making them look dark by setting the gray value to the darkest rgb value
        rows,cols,depth = img.shape
        i=0
        while i < rows:
            if i % 20 ==0:
                print('non-grays, row:',i,'of',rows,'if your image has great contrast, you can turn off low this slower mode by changing use_light_color_mode to False')
            j = 0
            row_had_color = False
            while j < cols:
                k = img[i,j]
                min = np.amin(k)
                max = np.amax(k)
                if min < max*.7:
                    gray[i,j] = 0  #min  # darkening the pixels that are not gray
                    row_has_color = True
                    #j += 1
                else:
                    j += 10
                j += 1
            i += 1
            if not row_had_color:
                i += 0

# setting threshold of gray image
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#_, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)



scale_percent = 30 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
#cv2.imshow('shapes gray', gray)
#cv2.waitKey(0)
#cv2.destroyAllWindows()





# using a findContours() function
contours, _ = cv2.findContours(
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i = -1
areas = []
rulermsg = ''
filled_contours = np.zeros(img.shape, np.uint8)
# list for storing names of shapes
for contour in contours:
    i += 1
    # here we are ignoring first counter because
    # findcontour function detects whole image as shape
    if i == 0:
        continue

    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)
    
    #PRINT AREA
    area = cv2.contourArea(contour)
    if area>100000:
        print("area of detected large shapes:",area)
    if area > 12*10**5 or area < .1*10**5:  # caution, this will cause a max and min regonized size
        continue
    else:
        # using drawContours() function
        rand_color_flavor1 = int(random.random()*180)
        rand_color_flavor2 = int(random.random()*180)
        cv2.drawContours(img, [contour], 0, (rand_color_flavor1, rand_color_flavor2, 255), 5)
        cv2.drawContours(filled_contours, [contour], 0, (255, 255, 255), cv2.FILLED)


        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

        # putting shape name at center of each shape
        cv2.putText(img, str(i), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (rand_color_flavor1, rand_color_flavor2, 255), 2)

if not use_last_identified_contours:
    print('saving',updated_path)
    cv2.imwrite(updated_path,filled_contours)  
    
    


scale_percent = 30 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
# displaying the image after drawing contours
#cv2.imshow('shapes contours, which is ruler and tool?', resized)
intermediate_out_path = 'which_contour.png'
cv2.imwrite(intermediate_out_path,img)  
webbrowser.get('macosx').open(intermediate_out_path)


print('check ' + intermediate_out_path)
index_of_ruler = int(input('which number was the ruler?'))
index_of_tool = int(input('which number was the tool?'))

tool_contour = contours[index_of_tool]

ruler_contour = contours[index_of_ruler]
ruler_area = cv2.contourArea(ruler_contour)
linear_calibration_factor = (ruler_area/expected_ruler_area)**.5

areas.append(tool_contour)
#areas.append(ruler_contour)

print()
print('areas')
calibrated_areas = [] # 30mm x 310mm = 9300mm^2 expected
ruler_recognition_size_tolerance = .3

if len(areas)==1:
    print('tool area og',areas[0],'calibrated',areas[0]**.5/linear_calibration_factor,'mm^2')
    print(rulermsg)
else:
    print('error: detected the wrong number of tools, len(areas)',len(areas),'areas:',areas)
    exit()


def turn_contour_into_accurate_outline(contour_of_interest):

    #scale points to real size
    output_points = []
    minx = 9999999999999999
    miny = 9999999999999999
    for i in contour_of_interest:
        x = i[0][0]/linear_calibration_factor
        y = i[0][1]/linear_calibration_factor
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        output_points.append([x,y])
    if use_subtraction_objects == False:
        #translate points toward origin, this doesnt work if there are multiple parts, small inconvenience
        for i, item in enumerate(output_points):
            newx = item[0]-minx
            newy = item[1]-miny
            output_points[i] = [newx,newy]
    #clean up points (trying to eliminate self-intersecting meshes that won't render in openscad https://github.com/openscad/openscad/issues/791)
    for i, item in enumerate(output_points):
        if use_subtraction_objects:
            round_digits = 0
        else:
            round_digits = 8
        newx = round(item[0],round_digits)
        newy = round(item[1],round_digits)
        output_points[i] = [newx,newy]
    return output_points

#mask = np.ones(img.shape, dtype=np.uint8) * 255
#cv2.drawContours(mask, [tool_contour], -1, (0,0,0), thickness=10)
#cv2.imshow('shapes', mask)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

fixed_main_tool_points = turn_contour_into_accurate_outline(tool_contour)
dfo = pd.DataFrame(fixed_main_tool_points,columns=["X","Y"])
dfo.to_csv(last_identified_contour_path,index=False)
    


main_tool_outline = linear_extrude(tool_outline_extrude_distance)(polygon(fixed_main_tool_points))




if use_subtraction_objects:
    csv_contour_ids = input('please input all subtraction contour ids with comma separation eg 1,2,3 here: ')
    csv_contour_ids.replace(' ','')
    csv_contour_ids += ','
    subtraction_contour_ids = csv_contour_ids.split(',')

    for sid in subtraction_contour_ids:
        if sid == None or sid == '':
            continue
        else:
            sidint = int(sid)
            fixed_cut_part_points = turn_contour_into_accurate_outline(contours[sidint])
            if sid == subtraction_contour_ids[0]:
                cut_part = linear_extrude(tool_outline_extrude_distance+20)(polygon(fixed_cut_part_points))
            else:
                cut_part += linear_extrude(tool_outline_extrude_distance+20)(polygon(fixed_cut_part_points))


    '''
    #THIS SECTION CAN BE USED IF YOU HAVE A CSV CONTAINING THE MANUALLY IDENTIFIED SUBTRACTION AREA USING SOMETHING LIKE FIJI
    #add my FIJI trace of the screen for cutting out of the tool contour
    df = pd.read_csv(use_subtraction_object_path, sep=',')

    df['Xn'] = df['X']-df['X'].min()
    df['Yn'] = df['Y']-df['Y'].min()

    scale = 1
    df['Xnl'] = df['Xn']*scale
    df['Ynl'] = df['Yn']*scale

    ll = df[['Xnl','Ynl']].values.tolist()

    length = 5

    cut_part = polygon(ll)
    cut_part = linear_extrude(length)(cut_part)
    cut_part = rotate([0,0,-2])(cut_part)
    cut_part = down(1)(cut_part)
    cut_part = right(10)(forward(70)(cut_part))
    '''
    
    to_print = main_tool_outline - cut_part
    

else:
    to_print = main_tool_outline

to_print = mirror([0,1,0])(to_print)

printstring = '$fn=100;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

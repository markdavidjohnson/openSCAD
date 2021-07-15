#image_to_tool_support_print_openSCAD.py

'''
How to use this:
Take a picture of a tool with a white background, and a standard cheap plastic ruler with it. 
Try to minimize distortion, and put the camera 1 meter above the subject, cropping down to 
have only the tool, ruler, and white background.

Then update the paths and run. It will scale using the ruler, automatically identifying it if
you've taken the picture from the correct distance (and your phone's resolution matches my iphone 8)
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

#general settings
image_path = '/Users/MarkJohnson/Downloads/IMG_6596.jpg'
use_last_identified_contour = False  # True or False
last_identified_contour_path = "image_to_tool_support_print_openSCAD_last_identified_contour.csv"
tool_outline_extrude_distance = .5
#subtraction object settings
use_subtraction_object = False
use_subtraction_object_path = "/Users/MarkJohnson/Downloads/screen.csv"

if not use_last_identified_contour:
    img = cv2.imread(image_path)
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

    #finding yellows and other light colors and making them look dark by setting the gray value to the darkest rgb value
    rows,cols,depth = img.shape
    i=0
    while i < rows:
        if i % 20 ==0:
            print('non-grays, row:',i,'of',rows)
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



    scale_percent = 30 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('shapes', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





    # using a findContours() function
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    areas = []
    rulermsg = ''
    # list for storing names of shapes
    for contour in contours:

        # here we are ignoring first counter because
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        #PRINT AREA
        area = cv2.contourArea(contour)
        if area > 9*10**5 or area < 1*10**5:  # caution, this will cause a max and min regonized size
            continue
        else:
            ruler_recognition_size_tolerance = .3
            if area > 500000* (1-ruler_recognition_size_tolerance) and area < 500000* (1+ruler_recognition_size_tolerance):  # IS RULER
                linear_calibration_factor = (area/9300)**.5
                if rulermsg == '':
                    rulermsg = 'ruler area og ' + str(area) + '\linear_calibration_factor ' + str(linear_calibration_factor)
                else:
                    print('error, multiple ruler messages')
                    exit()
            else:
                areas.append(area)
                tool_contour = contour

            # using drawContours() function
            cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)



            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])

            # putting shape name at center of each shape
            if len(approx) == 3:
                cv2.putText(img, 'Triangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 4:
                cv2.putText(img, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 5:
                cv2.putText(img, 'Pentagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 6:
                cv2.putText(img, 'Hexagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            else:
                cv2.putText(img, 'circle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    scale_percent = 30 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # displaying the image after drawing contours
    cv2.imshow('shapes', resized)

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

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #print(tool_contour)

    #scale points to real size
    output_points = []
    minx = 9999999999999999
    miny = 9999999999999999
    for i in tool_contour:
        x = i[0][0]/linear_calibration_factor
        y = i[0][1]/linear_calibration_factor
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        output_points.append([x,y])
    #translate points toward origin
    for i, item in enumerate(output_points):
        newx = item[0]-minx
        newy = item[1]-miny
        output_points[i] = [newx,newy]
    #clean up points (trying to eliminate self-intersecting meshes that won't render in openscad https://github.com/openscad/openscad/issues/791)
    for i, item in enumerate(output_points):
        newx = round(item[0],0)
        newy = round(item[1],0)
        output_points[i] = [newx,newy]

    mask = np.ones(img.shape, dtype=np.uint8) * 255
    cv2.drawContours(mask, [tool_contour], -1, (0,0,0), thickness=10)
    cv2.imshow('shapes', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    dfo = pd.DataFrame(output_points,columns=["X","Y"])
    dfo.to_csv(last_identified_contour_path,index=False)
    

else:  # if not using a new image to determine the points
    output_points = pd.read_csv(last_identified_contour_path).values.tolist()


main_tool_outline = linear_extrude(tool_outline_extrude_distance)(polygon(output_points))



if use_subtraction_object:

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


    to_print = main_tool_outline - cut_part

else:
    to_print = main_tool_outline



printstring = '$fn=100;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

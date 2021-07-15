#image_to_tool_support_print_openSCAD.py
import cv2
import numpy as np
from matplotlib import pyplot as plt
from solid.objects import linear_extrude, polygon

from solid import *
from solid.utils import *  # Not required, but the utils module is useful
import pyperclip
from io import StringIO
import pandas as pd 

# reading image
path = 'IMG_6592.jpg'
img = cv2.imread(path)
x=400
w=2300
y=1400
h=1000

img = img[y:y+h, x:x+w]

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

output_points = []
for i in tool_contour:
    output_points.append([i[0][0]/linear_calibration_factor,i[0][1]/linear_calibration_factor])

to_print = linear_extrude(.5)(polygon(output_points))

mask = np.ones(img.shape, dtype=np.uint8) * 255
cv2.drawContours(mask, [tool_contour], -1, (0,0,0), thickness=10)
cv2.imshow('shapes', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

printstring = '$fn=100;\n' + scad_render(to_print)
pyperclip.copy(printstring)

print("the following has been copied")
print(scad_render(to_print))
print()

import cv2
import numpy as np
from skimage.measure import regionprops
from skimage import color



maxx = 0
minx = 0
maxy = 0
miny = 0

def houghTransformtion(frame,grayImg):
    edges = cv2.Canny(grayImg,50,150,apertureSize = 3)
    cv2.imwrite('lineDetected13.jpg',frame)
    return findPoints(frame,edges)

def findPoints(frame,edges):
    #trazenje linija 
    minLineLength = 700
    maxLineGap = 8
    lines = cv2.HoughLinesP (edges, 1, np.pi / 180, 50, minLineLength, maxLineGap)

    #trazenje krajnjih tacaka
    minx = lines[0][0][0]
    miny = lines[0][0][1]
    maxx = lines[0][0][2]
    maxy = lines[0][0][3]

    temp = len(lines)
    
    print "start"
    
    for i in  range(temp):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]
        if  x1 < minx :
            miny = y1
            minx = x1
        if  x2 > maxx:
            maxx = x2
            maxy = y2
     #cv2.line(frame, (minx,miny), (maxx, maxy), (0, 255, 0), 2)
    return minx,miny,maxx,maxy


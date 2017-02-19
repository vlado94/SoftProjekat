#STUDENT
#RA 40/2013

#Ime
#Vladimir

#Prezime
#Stanojevic

#Predmet
#SOFT Computing


import cv2
import numpy as np
from scipy import ndimage
from vector import *
from skimage import color
from lineDetection  import *
from skimage.morphology import *
from sklearn.datasets import fetch_mldata


video = "videos2/video-1.avi"
vid = cv2.VideoCapture(video)
distOk = 20
mnist_numbers = []
mnist = fetch_mldata('MNIST original')
zbir = 0

def startHough() :
    vid = cv2.VideoCapture(video)
    ret, frame = vid.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        kernel = np.ones((2,2),np.uint8)
        gray = cv2.dilate(gray,kernel)
        frame1=frame
    vid.release()
    cv2.destroyAllWindows()
    return houghTransformtion(frame1,gray)
    
    
x1,y1,x2,y2=startHough()
edges = [(x1, y1), (x2, y2)]
id = -1        
    
def nextId():
    global id
    id += 1
    return id


#nalazenje objekata u zadatom okruzenju
def inRange(number,numbers) :
    result = []
    #iteriranje kroz listu svih dosadasnjim nadjenih 
    #elemenata u svim dosadasnjim frejmovima    
    #u pokrenutom klipu
    for nu in numbers:
          #provera da li je rastojanje objekata ispod dozvoljenog  
          if (distance(number['center'],nu['center']) < distOk) :

            result.append(nu)

    return result
        
        
    
def putPictureInLeftCorner(img_BW) :
    #print "stavljanje slike u gornji levi ugao"
    counter = 0
    maxx  = -1
    minx  = 1000
    maxy  = -1
    miny  = 1000
    heightOfNumber = 0
    widthOfNumber = 0
    newImg = np.zeros((28,28),np.uint8)
    try :
        label_img  = label(img_BW)
        regions = regionprops(label_img)
        
        while (counter < len(regions)) :
            bbox = regions[counter].bbox
            if bbox[0] < minx:
                minx = bbox[0]
            if bbox[1] < miny:
                miny = bbox[1]
            if bbox[2] > maxx:
                maxx = bbox[2]
            if bbox[3] > maxy:
                maxy = bbox[3]


            counter += 1
            
        #definisanje velicine objekta
        heightOfNumber = maxy - miny
        #print "sirina objekta:"
        #print widthOfNumber
        widthOfNumber = maxx - minx
        #print "visina objekta:"
        #print heightOfNumber
        newImg [0 : widthOfNumber, 0 : heightOfNumber] = newImg [0 : widthOfNumber,0 : heightOfNumber] + img_BW[ minx : maxx, miny : maxy]
        return  newImg
    except  ValueError:
        print "uhvaceno"
        pass
    
    
    
#detekcija o kom broju se radi
def detectNumber(img) :
    minSum  =  9999
    rez  =  -1
    for i in range(70000) : 
        mnist_img  =  mnist_numbers[i]
        sum  =  0
        sum  =  np.sum(mnist_img != img)
        if sum  <  minSum :
            minSum  =  sum
            rez  =  mnist.target[i]
        i  +=  1
    return  rez

        
#pronalazenje najblizeg elementa u listi od zadatog elementa
def findClosest (list,elem):
    #iteriranje kroz listu okolnih elemenata u jednom frejmu u pokrenutom klipu
    min = list[0]
    for obj in list:
        dist1 = distance (min['center'],elem['center'])
        dist2 = distance(obj['center'],elem['center'])
        if  dist1 > dist2:
            min = obj
    return min


def modifyPicture(img) :
    
    img_BW=color.rgb2gray(img) >= 0.88
    img_BW = (img_BW).astype('uint8')
    new_img  =  putPictureInLeftCorner(img_BW)
    new_img =  checkPicture(new_img,video)
    rez = detectNumber(new_img)
    
    return rez    
    
def translateMnist(mnist) :
    for i in range(70000)  :
        img  =  mnist.data[i].reshape(28,28)
        bin_img  =  ((color.rgb2gray(img)/255.0)>0.88).astype('uint8')
        bin_img  =  putPictureInLeftCorner(bin_img)
        mnist_numbers.append(bin_img)
        
def main():
    kernel = np.ones((2,2),np.uint8)
    translateMnist(mnist)
    numbers = []
    frame = 0
    while  (1) :
        ret, currentFrame = vid.read()
        if not ret: break
        #start_time  = time.time()
        
        #cv2.circle(currentFrame, (edges[0]), 4, (25, 25, 255), 1)
        #cv2.circle(currentFrame, (edges[1]), 4, (25, 25, 255), 1)
        
        
        lower = np.array([220 , 220 , 220],dtype = "uint8")
        upper = np.array([255 , 255 , 255],dtype = "uint8")
        
        trasholdImage = cv2.inRange(currentFrame, lower, upper)
        bw_img = trasholdImage * 1.0
        bw_imgCopy = trasholdImage * 1.0
        
        bw_img = cv2.dilate(bw_img,kernel)
        bw_img = cv2.dilate(bw_img,kernel)
        bw_img = update2(bw_img,video)
        
        
        labeled, _ = ndimage.label(bw_img)
        pictureElements = ndimage.find_objects(labeled)
               
        for i in range(len(pictureElements)) : 
            #print "analiza objekta" + format(i)
            location = pictureElements[i]
            #info o centru
            center = []
            center.append((location[1].stop + location[1].start) /2)
            center.append((location[0].stop + location[0].start) /2)
            
            #info o dimenzijama
            dimension = []
            dimension.append(location[1].stop - location[1].start)
            dimension.append(location[0].stop - location[0].start)
            
            if dimension[0] > 11 or dimension[1] > 11 : 
                number = {'center' : center, 'dimension' : dimension, 'frame' : frame}
                
                result = inRange(number,numbers)
                if len(result) == 0 :
                    number['id'] = nextId()
                    number['pass'] = False
                    x1 = center[0] - 14
                    y1 = center[1] - 14
                    x2 = center[0] + 14
                    y2 = center[1] + 14
                    number['value'] = modifyPicture(bw_imgCopy[y1:y2,x1:x2])
                    number['image'] = bw_imgCopy[y1:y2,x1:x2]
                    #cv2.imshow("primljen",number['image'])
                    #cv2.waitKey()
                    #print "registrovano::::: " + format(number['value'])
                    numbers.append(number)
                else:
                    num = findClosest(result,number)
                    num['center'] = number['center']
                    num['frame'] = number['frame']
                    
        for num in numbers :
            tt  =  frame - num['frame']
            if ( tt < 3 ):
                dist, pnt,r  =  pnt2line2(num['center'],edges[0],edges[1])
                if r  >  0 :
                    if dist < 9 :
                        if num['pass'] == False:
                            num['pass'] = True
                            (x,y) = num['center']
                            print "prosaaaooooo::::" + format(num['value'])
                            cv2.imshow('imagee',num['image'])
                            cv2.waitKey()
                            global zbir
                            zbir += num['value']
        cv2.imshow('frame',currentFrame)
        frame += 1
        k  = cv2.waitKey(30) & 0xff
        if  k == 27:
            break
    print "Zbir je: " + format(zbir)
    vid.release()
    cv2.destroyAllWindows()
main()
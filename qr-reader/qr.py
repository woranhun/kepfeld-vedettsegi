import cv2
import imutils
import numpy as np
#import qrReservedMask
from numpy.lib.function_base import append
from scipy import stats

img = cv2.imread('c:\\FCKONEDRIVE\\QR READER\\test.jpg')

scale_percent = 15 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)



#print(qrReservedMask.qrReserved)
  
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

grayImage = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

dst = cv2.Laplacian(blackAndWhiteImage, cv2.CV_8U, ksize=1)

cnts = cv2.findContours(dst.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

corners = []

for c in cnts:
	# compute the center of the contour
    M = cv2.moments(c)

    area = cv2.contourArea(c)         
    if area < 1000 or area > 2500:                   
         continue
    
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        corners.append([cx,cy])
        cv2.drawContours(dst, [c], -1, (0, 255, 0), 2)
        cv2.circle(dst, (cx, cy), 7, (0, 0, 255), -1)
        cv2.putText(dst, "center", (cx - 20, cy - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)


print(corners)

dst = cv2.line(dst, corners[0], corners[2], (255, 255, 0), 1)
dst = cv2.line(dst, corners[2], corners[1], (255, 255, 0), 1)

QRWidth = corners[0][1] - corners[2][1]

nodeWidth = QRWidth/53

xCrop = [int(corners[0][0]-nodeWidth*5),int(corners[1][0]+nodeWidth*4)]
yCrop = [int(corners[1][1]-nodeWidth*2),int(corners[0][1]+nodeWidth*4)]
print(xCrop)
print(yCrop)
cropped_image = blackAndWhiteImage[xCrop[0]:xCrop[1], yCrop[0]:yCrop[1]] 
 
kernel = np.ones((1,1),np.uint8)
closing = cv2.morphologyEx(cropped_image, cv2.MORPH_CLOSE, kernel)
resized = cv2.resize(closing, [456, 456], interpolation = cv2.INTER_NEAREST   )

rawData = np.zeros((57, 57))
for i in range(57):
    for j in range(57):
        yCrop = [j * 8 +1,j*8+7]
        xCrop = [i * 8 +1,i*8+7]
        node = resized[xCrop[0]:xCrop[1], yCrop[0]:yCrop[1]]

        #if (i%3  + j%2)%2 == 0: 
        #if (j)%3 == 0: 
        #if (i+j)%2 == 0: 
        #if (i)%2 == 0:
        #if (i+j)%3 == 0: 
        #if (i/2+j/3)%2 == 0: 
        #if (i*j)%2 + (i*j)%3 == 0: 
        #if ((i*j)%2 + (i*j)%3)%2 == 0:
        row = j
        column = i
        rawData[i][j] = 1 - (int(stats.mode(node, axis=None)[0]/255))
        #if (((column*row)%3) + ((column*row)%2)) == 0:
        #    rawData[i][j] = (int(stats.mode(node, axis=None)[0]/255))
        #else: rawData[i][j] = 1 - (int(stats.mode(node, axis=None)[0]/255))


#a format data nincs rendesen maszkolva
print(rawData)
uint_img = np.array(rawData*255).astype('uint8')
threshed = cv2.cvtColor(uint_img, cv2.COLOR_GRAY2BGR)
#cv2.imshow("asd",threshed)
#cv2.imwrite("detected.png", threshed)
#print([rawData[56][56], rawData[55][56], rawData[56][55], rawData[55][55]])
#print([rawData[56][54], rawData[55][54], rawData[56][53], rawData[55][53]])
column = 56
row = 56
isGoingUp = True
outData = []
for i in range(57):
    outData.append(int(rawData[row][column]))
    if(column%2 == 1):
        if(isGoingUp):
            row-=1
        else: row+=1
        column+=1
    else: column-=1

    #cv2.line(dst, corners[2], corners[1], (255, 255, 0), 1)

dataType = ""
for i in range(4):
    dataType += str(outData[i])
print("Data Type: " + dataType)
bytesOut = ""
for i in range(4,15):
    bytesOut += str(outData[i])
print(bytesOut)
print("Data Length: " + str(int(bytesOut, 2)))

dataOut = ""
for i in range(15, 57):
    dataOut += str(outData[i])
    if(len(dataOut) == 8):
        print(chr(int(dataOut, 2)))
        dataOut = ""

print(outData)

print(16%7)
#cv2.imshow('Black white image', closing)
cv2.imshow('Cropped', resized)

cv2.waitKey(0)
cv2.destroyAllWindows()
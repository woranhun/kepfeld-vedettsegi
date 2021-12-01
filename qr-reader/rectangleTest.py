import cv2
from numpy import inf

image = cv2.imread('test_photo.png')
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(
    gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow(" asd", thresh)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

minX = inf
maxX = 0
maxY = 0
minY = inf

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        if max(w, h)/min(w, h) < 1.05:
            minX = min(minX, x)
            maxX = max(maxX, x+w)
            maxY = max(maxY, y+h)
            minY = min(maxY, y)
            #cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh2 = cv2.threshold(
    gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
cropped_image = thresh2[minX:maxX, minY:maxY]

resized = cv2.resize(cropped_image, [57, 57], interpolation=cv2.INTER_NEAREST)
cv2.imwrite("cropim.png", cropped_image)



cv2.imshow('thresh', cropped_image)
cv2.imshow('image', image)
cv2.waitKey()

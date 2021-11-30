import os

import cv2
import imutils
import numpy as np
# import qrReservedMask
from scipy import stats


class QR:
    

    img = None
    corners = []

    def __init__(self):
        path = "c:\\FCKONEDRIVE\\kepfeld-vedettsegi\\qr-reader\\1234.png"
        self.img = cv2.imread(path)

    def main(self):
        QR_SIZE = 21
        ENABLE_MASKING = True
        qrMask21 = np.array([1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0])
        qrMask25 = np.array([1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

        # scale_percent = 100  # percent of original size
        # width = int(self.img.shape[1] * scale_percent / 100)
        # height = int(self.img.shape[0] * scale_percent / 100)
        # dim = (width, height)

        # resize image
        # resized = cv2.resize(self.img, dim, interpolation=cv2.INTER_AREA)

        grayImage = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

        dst = cv2.Laplacian(blackAndWhiteImage, cv2.CV_8U, ksize=1)

        contours = cv2.findContours(dst.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for contour in contours:
            # compute the center of the contour
            M = cv2.moments(contour)

            area = cv2.contourArea(contour)
            
            #depends on the image a lot
            #corners has to have 3 items in it (the alignment patterns)
            if area < 2000 or area > 4000:
                continue
            #print(area)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                self.corners.append([cx, cy])
                cv2.drawContours(dst, [contour], -1, (0, 255, 0), 2)
                cv2.circle(dst, (cx, cy), 7, (0, 0, 255), -1)
                cv2.putText(dst, "center", (cx - 20, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        #print(self.corners)
        cv2.line(dst, self.corners[0], self.corners[2], (255, 255, 0), 1)
        cv2.line(dst, self.corners[2], self.corners[1], (255, 255, 0), 1)

        #see if corners are detected correctly
        #cv2.imshow("asd", dst)

        QRWidth = self.corners[0][1] - self.corners[2][1]
        QRWidth2 = self.corners[2][0] - self.corners[1][0]
        #print(QRWidth, " " ,QRWidth2)

        nodeWidth = QRWidth / (QR_SIZE-9)

        ratioTo9 = (9/nodeWidth)

        #ratioTo8 *= ratioTo8*1.001
        #print(nodeWidth)
        scale_percent = 100 * ratioTo9  # percent of original size
        width = int(blackAndWhiteImage.shape[1] * scale_percent / 100)
        height = int(blackAndWhiteImage.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized2 = cv2.resize(blackAndWhiteImage, dim, interpolation=cv2.INTER_NEAREST)

        #cv2.imshow("res2",resized2)

        dst = cv2.Laplacian(resized2, cv2.CV_8U, ksize=1)

        contours = cv2.findContours(dst.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        self.corners = []
        for contour in contours:
            # compute the center of the contour
            M = cv2.moments(contour)

            area = cv2.contourArea(contour)
            
            #depends on the image a lot
            #corners has to have 3 items in it (the alignment patterns)
            if area < 2000 or area > 4000:
                continue
            #print(area)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                self.corners.append([cx, cy])
                cv2.drawContours(dst, [contour], -1, (0, 255, 0), 2)
                cv2.circle(dst, (cx, cy), 7, (0, 0, 255), -1)
                cv2.putText(dst, "center", (cx - 20, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        #print(self.corners)
        cv2.line(dst, self.corners[0], self.corners[2], (255, 255, 0), 1)
        cv2.line(dst, self.corners[2], self.corners[1], (255, 255, 0), 1)

        #see if corners are detected correctly
        #cv2.imshow("asd2", dst)

        ratioTo9 = 1
        xCrop = [int(self.corners[0][0] * ratioTo9 - 9 * 3 + 0), int(self.corners[1][0] * ratioTo9 + 9 * 3 + 0)]
        yCrop = [int(self.corners[1][1] * ratioTo9 - 9 * 3 + 3), int(self.corners[0][1] * ratioTo9 + 9 * 3 + 0)]
        #print(xCrop)
        #print(yCrop)
        cropped_image = resized2[xCrop[0]:xCrop[1], yCrop[0]:yCrop[1]]
        #cv2.imshow("cropped", cropped_image)
        #print("Cropped image resolution> ", cropped_image.shape[0])

        kernel = np.ones((1, 1), np.uint8)
        closing = cv2.morphologyEx(cropped_image, cv2.MORPH_CLOSE, kernel)
        resized = cv2.resize(closing, [QR_SIZE*9, QR_SIZE*9], interpolation=cv2.INTER_NEAREST)

        rawData = np.zeros((QR_SIZE, QR_SIZE))
        #resized = np.zeros((456, 456))
        mask = np.zeros((QR_SIZE, QR_SIZE))

        formatInfo = ""
        for i in range(0,5):
            j = 8
            yCrop = [j * 9 + 2, j * 9 + 6]
            xCrop = [i * 9 + 2, i * 9 + 6]
            node = resized[xCrop[0]:xCrop[1], yCrop[0]:yCrop[1]]
            if i == 2 or i == 4: 
                formatInfo+=str((1-(int(stats.mode(node, axis=None)[0] / 255))))
            else: formatInfo+=str(((int(stats.mode(node, axis=None)[0] / 255))))

        ecNumber = int(formatInfo[::2], 2)
        if(ecNumber == 3): print("EC Level: Low")
        if(ecNumber == 2): print("EC Level: Medium")
        if(ecNumber == 1): print("EC Level: Q")
        if(ecNumber == 0): print("EC Level: High")
        maskIndex = int(formatInfo[2::], 2)
        print("Mask pattern: ", maskIndex)
        masks = [lambda i,j : (i+j)%2 == 0, 
                lambda i,j : (i)%2 == 0,
                lambda i,j : (j)%3 == 0,
                lambda i,j : (i+j)%3 == 0,
                lambda i,j : (i // 2 + j // 3) % 2 == 0,
                lambda i,j : (i*j)%2 + (i*j)%3 == 0,
                lambda i,j : ((i*j)%2 + (i*j)%3)%2 == 0,
                lambda i,j : (((i * j) % 3) + ((i + j) % 2)) % 2 == 0]


        for i in range(QR_SIZE):
            for j in range(QR_SIZE):
                yCrop = [j * 9 + 2, j * 9 + 6]
                xCrop = [i * 9 + 2, i * 9 + 6]
                node = resized[xCrop[0]:xCrop[1], yCrop[0]:yCrop[1]]

                # See pixel centers
                #cv2.rectangle(resized, (xCrop[0], yCrop[0]), (xCrop[1], yCrop[1]), (int(stats.mode(node, axis=None)[0]),0,0), 1)
                cv2.rectangle(resized, (xCrop[0], yCrop[0]), (xCrop[1], yCrop[1]), (255,0,0), 1)

                if(ENABLE_MASKING):

                    #    if (j)%3 == 0:
                    #      if (i+j)%2 == 0:
                    #     if (i)%2 == 0:
                    #      if (i+j)%3 == 0:
                    #      if (i // 2 + j // 3) % 2 == 0:
                    #          if (i*j)%2 + (i*j)%3 == 0:
                    # if ((i*j)%2 + (i*j)%3)%2 == 0:


                    if masks[maskIndex](i,j):
                        rawData[i][j] = (int(stats.mode(node, axis=None)[0] / 255))
                        mask[i][j] = 1
                    else:
                        rawData[i][j] = 1-(int(stats.mode(node, axis=None)[0] / 255))
                        mask[i][j] = 0

                else:
                    rawData[i][j] = 1 - (int(stats.mode(node, axis=None)[0] / 255))

        #cv2.imshow("res",resized)
        # a format data nincs rendesen maszkolva
        #print(rawData)
        if(ENABLE_MASKING):
            masked = np.array(rawData * 255).astype('uint8')
            maskedImg =  255 - cv2.cvtColor(masked, cv2.COLOR_GRAY2BGR)
            #cv2.imshow("Masked", maskedImg)
            cv2.imwrite("detected1.png", maskedImg)

            maskDebug = np.array(mask * 255).astype('uint8')
            maskImg =  255 - cv2.cvtColor(maskDebug, cv2.COLOR_GRAY2BGR)
            #cv2.imshow("Mask", maskImg)
            cv2.imwrite("mask.png", maskImg)
        else: 
            orig = np.array(rawData * 255).astype('uint8')
            origImg =  255 - cv2.cvtColor(orig, cv2.COLOR_GRAY2BGR)
            #cv2.imshow("Original", origImg)
            cv2.imwrite("readOriginal.png", origImg)

        #Timing pattern bezavarna ehelyett
        #np.delete(rawData, 6, 1)


        column = QR_SIZE-1
        row = QR_SIZE-1
        isGoingUp = True
        outData = []
        afterTiming = False

        for i in range(QR_SIZE*(QR_SIZE-1)):

            if(column == 6):
                column-=1
                afterTiming = True
            #print("col " + str(column) + " row " + str(row))

            if(qrMask21[column*QR_SIZE + row] == 0):
                outData.append(int(rawData[row][column]))

            if afterTiming:
                if column % 2 == 0:
                    if (isGoingUp == True):
                        row -= 1
                    else:
                        row += 1
                    column += 1
                else:
                    column -= 1
            else: 
                if column % 2 == 1:
                    if (isGoingUp == True):
                        row -= 1
                    else:
                        row += 1
                    column += 1
                else:
                    column -= 1

            #this wont work after timing pattern
            if(isGoingUp and row == -1 and column%2 == 0):
                column-=2
                row = 0
                isGoingUp = False

            if(not isGoingUp and row == QR_SIZE and column%2 == 0):
                column-=2
                row= QR_SIZE-1
                isGoingUp = True

            

            # cv2.line(dst, corners[2], corners[1], (255, 255, 0), 1)


        

        dataOut = ""
        stringOut = ""
        #itt kell 0-tól menni és úgy megy az RS decode
        for i in range(0, len(outData)):
            
            dataOut += str(outData[i])
            
            if len(dataOut) == 8:
                stringOut += chr(int(dataOut, 2))
                dataOut = ""

        #print(outData[128::])
        s = list(stringOut)
        s[0] = "a"
        stringOut = "".join(s)
        original = stringOut.encode('iso-8859-1')

        from reedsolo import RSCodec
        rsc = RSCodec(7)  # 10 ecc symbols
        decodedData = rsc.decode( bytearray(original))[0]

        dec = decodedData

        bytes_as_bits = ''.join(format(byte, '08b') for byte in dec)
        

        integer_map = map(int, bytes_as_bits)
        bytes_as_bits_lst = list(integer_map)

        dataOut = ""
        stringOut = ""
        for i in range(12, len(bytes_as_bits_lst)):
            dataOut += str(bytes_as_bits_lst[i])
            if len(dataOut) == 8:
                stringOut += chr(int(dataOut, 2))
                dataOut = ""

        original = stringOut.encode('iso-8859-1')
                
        print("Data Length (bits): ", len(bytes_as_bits_lst))
        dataType = "".join([str(i) for i in bytes_as_bits_lst[0:4]])
        print("Data Type: " + dataType)

        bytesOut = "".join([str(i) for i in bytes_as_bits_lst[4:12]])
        numCharacters = int(bytesOut, 2)
        print("Number of characters : " + str(numCharacters))


        print(original[:numCharacters])

        
   

        # cv2.imshow('Black white image', closing)
        cv2.imshow('Cropped', resized)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':

    



    qr = QR()
    qr.main()

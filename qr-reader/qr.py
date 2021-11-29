import os

import cv2
import imutils
import numpy as np
# import qrReservedMask
from PIL import Image
from pyzbar.pyzbar import decode
from scipy import stats


class QR:
    img = None
    corners = []

    def __init__(self, path: os.path = os.path.join("qr-reader", "img.png")):
        self.img = cv2.imread(path)

    def main(self):
        # scale_percent = 15  # percent of original size
        scale_percent = 100  # percent of original size
        width = int(self.img.shape[1] * scale_percent / 100)
        height = int(self.img.shape[0] * scale_percent / 100)
        dim = (width, height)

        # print(qrReservedMask.qrReserved)

        # resize image
        resized = cv2.resize(self.img, dim, interpolation=cv2.INTER_AREA)

        grayImage = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

        dst = cv2.Laplacian(blackAndWhiteImage, cv2.CV_8U, ksize=1)

        contours = cv2.findContours(dst.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for contour in contours:
            # compute the center of the contour
            M = cv2.moments(contour)

            area = cv2.contourArea(contour)
            # if area < 1000 or area > 2500:
            if area < 100 or area > 700:
                continue

            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                self.corners.append([cx, cy])
                cv2.drawContours(dst, [contour], -1, (0, 255, 0), 2)
                cv2.circle(dst, (cx, cy), 7, (0, 0, 255), -1)
                cv2.putText(dst, "center", (cx - 20, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        print(self.corners)

        cv2.waitKey(0)
        cv2.line(dst, self.corners[0], self.corners[2], (255, 255, 0), 1)
        cv2.line(dst, self.corners[2], self.corners[1], (255, 255, 0), 1)

        QRWidth = self.corners[0][1] - self.corners[2][1]

        nodeWidth = QRWidth / 53

        xCrop = [int(self.corners[0][0] - nodeWidth * 5), int(self.corners[1][0] + nodeWidth * 4)]
        yCrop = [int(self.corners[1][1] - nodeWidth * 2), int(self.corners[0][1] + nodeWidth * 4)]
        print(xCrop)
        print(yCrop)
        cropped_image = blackAndWhiteImage[xCrop[0]:xCrop[1], yCrop[0]:yCrop[1]]

        kernel = np.ones((1, 1), np.uint8)
        closing = cv2.morphologyEx(cropped_image, cv2.MORPH_CLOSE, kernel)
        resized = cv2.resize(closing, [456, 456], interpolation=cv2.INTER_NEAREST)

        rawData = np.zeros((57, 57))
        # resized = np.zeros((456, 456))
        for i in range(57):
            for j in range(57):
                yCrop = [j * 8 + 1, j * 8 + 7]
                xCrop = [i * 8 + 1, i * 8 + 7]
                node = resized[xCrop[0]:xCrop[1], yCrop[0]:yCrop[1]]

                # if (j)%3 == 0:
                # if (i+j)%2 == 0:
                # if (i)%2 == 0:
                # if (i+j)%3 == 0:
                # if (i // 2 + j // 3) % 2 == 0:
                # if (i*j)%2 + (i*j)%3 == 0:
                # if ((i*j)%2 + (i*j)%3)%2 == 0:
                row = j
                column = i
                # rawData[i][j] = 1 - (int(stats.mode(node, axis=None)[0] / 255))

                # # if (int(stats.mode(node, axis=None)[0] / 255)) == (((column * row) % 3) + ((column + row) % 2)) % 2:
                if (int(stats.mode(node, axis=None)[0] / 255)) == ((i * j) % 2 + (i * j) % 3) % 2:
                    rawData[i][j] = 0
                else:
                    rawData[i][j] = 1

                # rawData[i][j] ^= (((i * j) % 3) + ((i + j) % 2)) % 2

        # a format data nincs rendesen maszkolva
        print(rawData)
        self.img = np.array(rawData * 255).astype('uint8')
        threshed = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        # cv2.imshow("asd",threshed)
        cv2.imwrite(os.path.join("qr-reader", "detected.png"), threshed)
        tmp = threshed
        # print([rawData[56][56], rawData[55][56], rawData[56][55], rawData[55][55]])
        # print([rawData[56][54], rawData[55][54], rawData[56][53], rawData[55][53]])
        column = 56
        row = 56
        isGoingUp = True
        rawread = []
        for i in range(57):
            rawread.append(int(rawData[row][column]))
            if column % 2 == 1:
                if isGoingUp:
                    row -= 1
                else:
                    row += 1
                column += 1
            else:
                column -= 1

            # cv2.line(dst, corners[2], corners[1], (255, 255, 0), 1)

        dataType = "".join([str(i) for i in rawread[0:4]])
        print("Data Type: " + dataType)

        bytesOut = "".join([str(i) for i in rawread[4:20]])
        print("Data Length: " + str(int(bytesOut, 2)))

        dataOut = ""
        for i in range(20, 57):
            dataOut += str(rawread[i])
            if len(dataOut) == 8:
                print(chr(int(dataOut, 2)))
                dataOut = ""

        ou = "".join([str(i) for i in rawread[20:]])
        ou = "0b" + ou
        ou = int(ou, 2)
        print(rawread[20:])
        print((rawread[:8]))
        print(bin(bytearray("h", "ISO-8859-1")[0]))
        print(bin(bytearray("a", "ISO-8859-1")[0]))
        print(ou.to_bytes((ou.bit_length() + 7) // 8, 'big').decode('ISO-8859-1'))

        print(decode(Image.open("./qr-reader/img.png")))
        # cv2.imshow('Black white image', closing)
        cv2.imshow('Cropped', resized)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    qr = QR()
    qr.main()

# import the opencv library
import cv2


def callback(x):
    pass


def findID(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, l, u)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        hull = cv2.convexHull(c)
        cv2.drawContours(img, [hull], 0, (0, 255, 0), 2)
    return img


if __name__ == "__main__":
    cv2.namedWindow('bars')
    cv2.createTrackbar('L', 'bars', 0, 255, callback)  # lower threshold trackbar for window 'image
    cv2.createTrackbar('U', 'bars', 0, 255, callback)  # upper threshold trackbar for window 'image
    cv2.createTrackbar('sigma', 'bars', 0, 255, callback)  # upper threshold trackbar for window 'image
    while True:
        l = cv2.getTrackbarPos('L', 'bars')
        u = cv2.getTrackbarPos('U', 'bars')
        sigma = cv2.getTrackbarPos('sigma', 'bars')
        pic = cv2.imread("./img/20211006_184640/1.png")
        pic = cv2.GaussianBlur(pic, (3, 3), sigma/10)

        idcard = findID(pic)
        cv2.imshow('frame', idcard)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Destroy all the windows
    cv2.destroyAllWindows()

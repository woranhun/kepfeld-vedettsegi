# import the opencv library
import os
from datetime import datetime

import cv2


def createFolderFromTime(basePath: os.path) -> os.path:
    workingPath = os.path.join(basePath, datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.makedirs(workingPath)
    return workingPath


workdir = createFolderFromTime("./img")
os.chdir(workdir)
# define a video capture object
vid = cv2.VideoCapture(0)
i = 0
while (True):

    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    key = cv2.waitKey(1)
    if key & 0xFF == ord(' '):
        cv2.imwrite(str(i) + ".png", frame)
        i += 1
    elif key & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

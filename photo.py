
#import the Raspberry Pi camera modules.
from picamera.array import PiRGBArray
from picamera import PiCamera
import time, cv2

#import the matplotlib pyplot module. Refer to it as plt.
#import matplotlib.pyplot as plt
#import the Ipython display module clear_output methods
from IPython.display import clear_output


def takePlaque():
    # sanity check, to be sure that no other processes are using the camera
    try:
        camera.close()
        del camera
    except:
        print('ok')

    camera = cv2.VideoCapture(0)
    ret, image = camera.read()
    cv2.imwrite('plaque.jpg', image)
    camera.release()

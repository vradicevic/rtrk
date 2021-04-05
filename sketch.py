from cv2 import cv2
import numpy as np
import os
import pathlib
import copy
import random
import io
from PIL import Image



def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T

def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float)

    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result

WIDTH,HEIGHT = 1280,720
folderPath = "C:\\Videosekvence\\Dummy sekvence"
offsets=[15,25,35,45]

shapeSize = (128,72)
array = get_gradient_3d(16, 9, (0, 0, 192), (255, 255, 64), (True, False, False))
movingObject = np.uint8(array)
movingObject = cv2.resize(movingObject,shapeSize,interpolation=cv2.INTER_CUBIC)
acx,acy = 640,360
for step in offsets:
    p1 = (acx, acy)
    p2 = (acx+step, acy)
    p3 = (acx, acy+step)
    p4 = (acx+step, acy+step)
    p5 = (acx-step, acy)
    p6 = (acx, acy-step)
    p7 = (acx-step, acy-step)
    p8 = (acx+step, acy-step)
    p9 = (acx-step, acy+step)
    pointList = [p1,p2,p3,p4,p5,p6,p7,p8,p9]

    for p in range(len(pointList)):
        
        newFrame = np.ones((HEIGHT,WIDTH,3),dtype=np.uint8)
        newFrame[pointList[p][1]:(pointList[p][1]+72),pointList[p][0]:(pointList[p][0]+128)] = movingObject
        cv2.imshow("Shape",newFrame)
        cv2.waitKey()
        filePath = folderPath+ "\\Offset" +str(step)+"Frame" + str(p) + ".yuv"
        yuv = cv2.cvtColor(newFrame,cv2.COLOR_BGR2YUV)
        f= io.BytesIO()
        f.write(yuv.tobytes())
        with open(filePath,'wb') as file:
            file.write(f.getbuffer())



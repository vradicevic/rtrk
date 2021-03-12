from cv2 import cv2
import numpy as np
import os
import pathlib
import copy
import random
import io
from PIL import Image

blockSize = 42
WIDTH,HEIGHT = 1280,720
folderPath = "images\\evaluation42BlockSize"
steps = [10,20,30,50,100,200,300]
acx, acy = (360,360)   #središte bloka randomnoisea
subBlockSize = 6



blockOfRandomNoise = np.ones((blockSize,blockSize,3),dtype=np.uint8)
for i in range(0,blockSize,subBlockSize):
    for j in range(0,blockSize,subBlockSize):
        temp = np.ones((subBlockSize,subBlockSize,3),dtype=np.uint8)
        temp[:,:] = [( random.randint(0,255)),( random.randint(0,255) ),( random.randint(0,255) )]
        blockOfRandomNoise[i:i+subBlockSize,j:j+subBlockSize] = temp
        
for step in steps:
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
        pointList[p] = (pointList[p][0]-int(blockSize/2),pointList[p][1]-int(blockSize/2))
        newFrame = np.ones((HEIGHT,WIDTH,3),dtype=np.uint8)
        newFrame[pointList[p][1]:(pointList[p][1]+blockSize),pointList[p][0]:(pointList[p][0]+blockSize)] = blockOfRandomNoise
        
        filePath = folderPath+ "\\Step" +str(step)+"Block"+str(blockSize) +"Frame" + str(p) + ".yuv"
        yuv = cv2.cvtColor(newFrame,cv2.COLOR_BGR2YUV)
        f= io.BytesIO()
        f.write(yuv.tobytes())
        with open(filePath,'wb') as file:
            file.write(f.getbuffer())
    





# for pos in range(0,numsOfFrames,1):
#     fileName = "images\\FrameShapeBlock16\\FrameShapeNum"+str(pos)+".png"
#     newFrame = np.ones((HEIGHT,WIDTH,3))
#     x = startPosition[1] + pos*step
#     y = startPosition[0] + pos*step
#     newFrame[x:(x+blockSize),y:(y+blockSize),0:3] = blockOfRandomNoise
#     newFrame[x+blockSize:x+2*blockSize,y:y+blockSize] = scndblockOfRandomNoise
#     newFrame[x+blockSize:x+2*blockSize,y-blockSize:y] = thrdblockOfRandomNoise
#     cv2.imshow("Frame",newFrame)
#     cv2.waitKey()
#     cv2.imwrite(fileName,newFrame)

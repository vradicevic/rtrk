from cv2 import cv2
import numpy as np
import os
import pathlib
import new_tss
from paths import *

width,height = 1280,720


blockSize = 32


vectorsFile = open(vectorsPath,"r+")
buffer = np.fromfile(vectorsFile,dtype=np.int16)
vectors = []
numOfVs = int(len(buffer)/6)


for i in range(0,len(buffer),6):
    vectors.append((buffer[i:i+6])) 
    #svaki vektor je složen od 5 integera na sljedeći način u bin-u
    # ::from-[0]=x i [1]=y   2 integera jedan x drugi y 
    # ::to- [2]=x i  [3]=y  2 integera jedan x drugi y 
    # ::length- [4] 1 integer udaljenosti from i to točke
    # ::angle- [5] 1 integer kut vektora
vectorsFile.close()



videoPath = videoMovingDashboard30FPS

print(len(buffer)/6)
framenum = 45
file = open(videoPath,'rb')
file.seek(framenum*width*height*2)
yuv = np.frombuffer(file.read(width*height*2), dtype=np.uint8).reshape(height,width,2)
file.close()
png = cv2.cvtColor(yuv,cv2.COLOR_YUV2BGR_YUYV)



 
numofVectors = 0
for bcount in range(0, numOfVs, 1):
    if vectors[bcount][4]>2:
        numofVectors+=1
        pointFrom = vectors[bcount][0:2]
        pointTo = vectors[bcount][2:4]
        print("Angle: "+ str(vectors[bcount][5]))
        cv2.arrowedLine(png,(pointFrom[0],pointFrom[1]), (pointTo[0],pointTo[1]),(0,0,255), 1)
print(numofVectors)
cv2.imshow("Framnjo",png)

#cv2.imwrite("F:\\Slike\\hibridtestMoving.png",png)
cv2.waitKey()


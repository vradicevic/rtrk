from cv2 import cv2
import numpy as np
import os
import pathlib
import xlwt 
from xlwt import Workbook
from math import sqrt,pow,atan2
offsets = [15,25,35,45]
width,height = 1280,720
imgPath = "D:\\Videosekvence\\Dummy sekvence\\Offset15Frame0.yuv"
file = open(imgPath,'rb')
yuv = np.frombuffer(file.read(width*height*3), dtype=np.uint8).reshape(height,width,3)
png = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
file.close()
for offset in offsets:
    for frame in range(1,9,1):
        png = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
        vectorsPath = "D:\\vektori\\evaluation_dummy\\vectorsOffset"+str(offset)+"Frame"+str(frame)+".bin"
        
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
        for bcount in range(0, numOfVs, 1):
            if vectors[bcount][4]>2:
                pointFrom = vectors[bcount][0:2]
                pointTo = vectors[bcount][2:4]
                
                cv2.arrowedLine(png,(pointFrom[0],pointFrom[1]), (pointTo[0],pointTo[1]),(0,0,255), 1)
        cv2.imshow("Png",png)
        cv2.waitKey()
        


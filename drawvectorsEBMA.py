from cv2 import cv2
import numpy as np
import os
import pathlib


width,height = 1280,720
step = 15
offset= 10
frame= 3

pathVectors = "D:\\ProgramskiDokumenti\\VS Code\\Pythonprojects\\rtrk\\vectors\\vectorsEBMA\\vectorsFrame" +str(frame)+"StepSize"+ str(step)+"Offset"+str(offset)+".bin"
vectorsFile = open(pathVectors,"r+")
buffer = np.fromfile(vectorsFile,dtype=np.int_)
vectors = []

for i in range(0,len(buffer),6):
    vectors.append((buffer[i:i+6])) 
    #svaki vektor je složen od 5 integera na sljedeći način u bin-u
    # ::from-[0]=x i [1]=y   2 integera jedan x drugi y 
    # ::to- [2]=x i  [3]=y  2 integera jedan x drugi y 
    # ::length- [4] 1 integer udaljenosti from i to točke
    # ::angle- [5] 1 integer kut vektora
vectorsFile.close()
pathImage = "D:\\ProgramskiDokumenti\\VS Code\\Pythonprojects\\rtrk\\images\\evaluation\\Step"+str(offset)+"Block16Frame"+str(frame)+".yuv"
file = open(pathImage,'rb')
yuv = np.frombuffer(file.read(width*height*3), dtype=np.uint8).reshape(height,width,3)
file.close()
png = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
blockSize = 8
w_segments = int(width/blockSize)
h_segments = int(height/blockSize)
vectorsCount = w_segments*h_segments
for bcount in range(0, vectorsCount, 1):
        
        if (vectors[bcount][0],vectors[bcount][1]) != (vectors[bcount][2],vectors[bcount][3]) :
            
                    
            pointFrom = vectors[bcount][0:2]
            pointTo = vectors[bcount][2:4]
           
            cv2.arrowedLine(png,(pointFrom[0],pointFrom[1]), (pointTo[0],pointTo[1]),(255,255,255), 1)

cv2.imshow("Frame",png)
cv2.waitKey()
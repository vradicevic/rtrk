from cv2 import cv2
import numpy as np
import os
import pathlib
import new_tss
path ="D:\\Visual Studio Code\\rtrk\\vectors\\vectorsFrame3StepSize10Offset10.bin"
yuvVideoSequence = "D:\\Visual Studio\\YUV\\captureYUV422P.yuv"

vectorsFile = open(path,"r+")
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

#flow=[]



width,height= 1280, 720
blockSize = 8
w_segments = int(width/blockSize)
h_segments = int(height/blockSize)
vectorsCount = w_segments*h_segments
frameNumber = 12

frame = cv2.imread("D:\\Visual Studio Code\\rtrk\\images\\Block43Step10\\Block43Step10Frame1.png")
color =(255,0,255)
colorFlag = False

for bcount in range(0, vectorsCount, 1):
        
        if (vectors[bcount][0],vectors[bcount][1]) != (vectors[bcount][2],vectors[bcount][3]) :
            if(colorFlag):
                color= (255,0,0)
                colorFlag= False
            else:
                color = (0,0,255)
                colorFlag=True
                    
            pointFrom = vectors[bcount][0:2]
            pointTo = vectors[bcount][2:4]
           
            cv2.arrowedLine(frame,(pointFrom[0],pointFrom[1]), (pointTo[0],pointTo[1]),(255,255,255), 1)
            
            #cv2.putText(frame,str(vectors[bcount][5]),(pointTo[0],pointTo[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25,color,1,cv2.LINE_AA,False)
            

cv2.imshow("Frame",frame)
cv2.waitKey()
from cv2 import cv2
import numpy as np
import os
import pathlib
import xlwt 
from xlwt import Workbook
from math import sqrt,pow,atan2
pi = 3.14159265

wb = Workbook() 
offsets = [10, 20 ,30, 50, 100,200,300]
steps = [10,15,20,25, 30,35,40,45,50, 100,150,200,250]
angles = [0,0,90,45,180,-90,-135,-45,135]

width,height= 1280, 720
blockSize = 8
w_segments = int(width/blockSize)
h_segments = int(height/blockSize)
vectorsCount = w_segments*h_segments
sheet1 = wb.add_sheet('Validation')

row,column = 0,0
sheet1.write(0,1, "Broj pronađenih vektora")
sheet1.write(0,2, "Broj valjanih vektora")
vectorsNum = 0
vectorsPassed = 0

for offset in offsets:
    for step in steps:
        lengths = [(0,0),(offset,0),(0,offset),(offset,offset),(-offset,0),(0,-offset),(-offset,-offset),(offset,-offset),(-offset,offset)]
        sheet1.write(row,0, ("Offset: "+str(offset)+" Step: "+str(step)))
        row+=1
        for frame in range(0,9,1):
            
            path = "D:\\ProgramskiDokumenti\\VS Code\\Pythonprojects\\rtrk\\vectors\\vectorsEBMA\\vectorsFrame" +str(frame)+"StepSize"+ str(step)+"Offset"+str(offset)+".bin"
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
            
            for bcount in range(0, vectorsCount, 1):
                length = int(sqrt(pow(lengths[frame][0],2)+pow(lengths[frame][1],2)))
                
            
                if (vectors[bcount][0],vectors[bcount][1]) != (vectors[bcount][2],vectors[bcount][3]):
                    
                    print("Frame: "+str(frame)+"Step: "+str(step)+" Offset:"+str(offset))
                    print("Lengths: " +str(length)+":"+str(vectors[bcount][4]))
                    vectorsNum+=1
                    if( vectors[bcount][5] == angles[frame] and vectors[bcount][4]== length):
                        vectorsPassed+=1
                   
            sheet1.write(row+frame, 0,("Frame"+str(frame)))
            sheet1.write(row+frame, 1,str(vectorsNum))
            sheet1.write(row+frame, 2,str(vectorsPassed))

            vectorsNum = 0
            vectorsPassed = 0

        row += 13 

wb.save('validationEBMA.xls')
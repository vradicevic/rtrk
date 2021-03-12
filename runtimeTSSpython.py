import sys
import numpy as np
from cv2 import cv2 
import new_tss
import copy
import ebma
import xlwt 
from xlwt import Workbook
from math import sqrt,pow,atan2
pi = 3.14159265
blockSize=8
wb = Workbook()
offsets = [10, 20 ,30, 50, 100,200,300]
steps = [10,15,20,25, 30,35,40,45,50, 100,150,200,250]
angles = [0,0,90,45,180,-90,-135,-45,135]
width,height = 1280,720

hSegments, wSegments = int(height/blockSize),int(width/blockSize)
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
            
            pathRef = "D:\\ProgramskiDokumenti\\VS Code\\Pythonprojects\\rtrk\\images\\evaluation\\Step"+str(offset)+"Block16Frame0.yuv"
            pathCurrent = "D:\\ProgramskiDokumenti\\VS Code\\Pythonprojects\\rtrk\\images\\evaluation\\Step"+str(offset)+"Block16Frame"+str(frame)+".yuv"
            refImg = new_tss.getPngFromYUV444(pathRef,width,height)
            currImg = new_tss.getPngFromYUV444(pathCurrent,width,height)
            vectors = new_tss.main(refImg,currImg,blockSize=8,step= step)
            bcount = 0
            for y in range(0, int(hSegments*blockSize), blockSize):
                for x in range(0, int(wSegments*blockSize), blockSize):
                    if (x,y) != vectors[bcount] :
                        #print("x:"+str(x)+" Y:"+str(y)+"\n"+"Px:"+str(vectors[bcount][0])+" Py:"+str(vectors[bcount][1]))
                        vectorsNum+=1
                        p= vectors[bcount]
                        lengthExpected = int(sqrt(pow(lengths[frame][0],2)+pow(lengths[frame][1],2)))
                        lenghtReal = int(sqrt(pow((p[0]-x),2)+pow((p[1]-y),2)))
                        if( lenghtReal== lengthExpected):
                            vectorsPassed+=1
                    bcount = bcount + 1
            
            
                   
            sheet1.write(row+frame, 0,("Frame"+str(frame)))
            sheet1.write(row+frame, 1,str(vectorsNum))
            sheet1.write(row+frame, 2,str(vectorsPassed))

            vectorsNum = 0
            vectorsPassed = 0

        row += 13 

wb.save('validationResultPython.xls')
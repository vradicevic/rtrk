from cv2 import cv2
import numpy as np
import os
import pathlib
import xlwt 
from xlwt import Workbook
from math import ceil, sqrt,pow,atan2
from utils import *
pathVectors = "C:\\Dummy evaluacija\\640x360\\Block=16\\Vektori\\"
saveXlsPath = "C:\\Dummy evaluacija\\640x360\\Block=16\\MYBMA.xls"
pi = 3.14159265
directions = ["Right","Down","DownRight","Left","Up","UpLeft","UpRight","DownLeft"]
lengthRule = [True,True,False,True,True,False,False,False]
angles = [0,90,45,180,270,225,315,135]
objects = ["128x72","256x144","512x288"]
steps = [15,25,35]
width,height = 1280,720

row,col =0,0
iter=0

wb = Workbook()
sheet = wb.add_sheet('MYBMA',cell_overwrite_ok=True)
startRow=0
for object in objects:
    sheet.write(row,0, object)
    startRow=row
    row+=2
    for direction in directions:
        sheet.write(row,0, direction)
        col=1
        for step in steps:
            sheet.write(startRow,col, ("Step:"+str(step)))
            sheet.write(startRow+1,col, "Total")
            sheet.write(startRow+1,col+1, "Good")
            path = pathVectors + "MYBMA_"+str(object)+"_"+str(direction)+"_Step="+str(step)+".bin"
            numOfVs,vectors = ReadVectors(path)
            
            good = EvaluateVectors(vectors,numOfVs,[(not lengthRule[iter])*ceil(sqrt(pow(step/2,2)*2))+(lengthRule[iter])*ceil(step/2),angles[iter]])
            sheet.write(row,col, numOfVs)
            sheet.write(row,col+1, good)
            col+=2 
        row+=1
        iter+=1
    iter=0
    row+=2

wb.save(saveXlsPath)
            
            




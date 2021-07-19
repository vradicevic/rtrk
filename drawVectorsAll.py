
from utils import *
from cv2 import cv2
import numpy as np
pathVectors = "C:\\Dummy evaluacija\\640x360\\Block=16\\Vektori\\"
pathSaveImages ="C:\\Dummy evaluacija\\640x360\\Block=16\\Slike\\TSS\\"
pathVideo = "C:\\Videosekvence\\dummy_sekvenca_640x360.yuv"
directions = ["Right","Down","DownRight","Left","Up","UpLeft","UpRight","DownLeft"]
objects = ["128x72","256x144","512x288"]
steps = [15,25,35]
width,height = 640,360
file = open(pathVideo,'rb')
for object in objects:
    
    for step in steps:
        
        for direction in directions:
            file.seek(width*height*2,1)
            path = pathVectors + "TSS_"+str(object)+"_"+str(direction)+"_Step="+str(step)+".bin"
            numOfVs,vectors = ReadVectors(path)
            yuv = np.frombuffer(file.read(width*height*2), dtype=np.uint8).reshape(height,width,2)
            png = cv2.cvtColor(yuv,cv2.COLOR_YUV2BGR_YUYV)
            for vector in vectors:
                pointFrom = vector[0:2]
                pointTo = vector[2:4]
                cv2.arrowedLine(png,(pointFrom[0],pointFrom[1]), (pointTo[0],pointTo[1]),(255,0,0), 2)
            fileName = pathSaveImages+str(object) + "_"+str(direction)+"_"+str(step)+".png"
            cv2.imwrite(fileName,png)

file.close()
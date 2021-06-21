from cv2 import cv2
import random
import io
import os
import numpy

pathWrite = "F:\\Videosekvence\\dummy_sekvenca.yuv"
mypath = "F:\\Videosekvence\\Dummy sekvence\\YUYV"
files = os.listdir(mypath)
print(files)

fileAppend = open(pathWrite,"ab")
for videoFile in files:
    fileRead = open(mypath+"\\"+ videoFile,"rb")
    video = fileRead.read()
    fileAppend.write(video)
    fileRead.close()

fileAppend.close()
print("Done")

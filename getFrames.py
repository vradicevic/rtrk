from cv2 import cv2
import random
import io
import os

videoPath = "F:\\Videosekvence\\yuv\\odabrani_mirna_rightYUYVFPS30.yuv"
savePath = "F:\\Videosekvence\\odabrani_mirna.yuv"


selectors = random.sample(range(1,65,2),18)
selectors.sort()
print(selectors)
frameSize = 1280*720*2
fileRead = open(videoPath, "rb+")
fileWrite = open(savePath,"ab+")
for i in range(0,18,1):
    fileRead.seek((selectors[i]-1)*frameSize,os.SEEK_SET)
    yuyv = fileRead.read(frameSize)
    fileWrite.write(yuyv)
    fileRead.seek(selectors[i]*frameSize,os.SEEK_SET)
    yuyv = fileRead.read(frameSize)
    fileWrite.write(yuyv)
fileRead.close()
fileWrite.close()
print("End")


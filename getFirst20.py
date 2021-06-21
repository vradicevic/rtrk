
from cv2 import cv2
import io

videopath = "D:\\Videosekvence\\yuv\\odabrani final\\slijedniKamionOdabraniMovingDashboard.yuv"
savepath = "D:\\Videosekvence\\yuv\\odabrani final\\slijedniKamion.yuv"

fileRead = open(videopath,"rb")
fileWrite = open(savepath,'wb')
frameSize = int(1280*720*2)



fileRead.seek(30*frameSize,1)
for i in range(0,20):
    binary = fileRead.read(frameSize)
    fileWrite.write(binary)
    binary = fileRead.read(frameSize)
    fileWrite.write(binary)
    
    
    

fileRead.close()
fileWrite.close()

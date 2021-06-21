
from cv2 import cv2
import io

videopath = "F:\\Videosekvence\\odabrani_movingDashboard.yuv"
savepath = "F:\\Videosekvence\\objectFollowSequence.yuv"

fileRead = open(videopath,"rb")
fileWrite = open(savepath,'ab')
frameSize = 1280*720*2
ok = True

cnt=0
pairs = [22,34]
for pair in pairs:
    fileRead.seek(pair*frameSize,0)
    binary = fileRead.read(frameSize)
    fileWrite.write(binary)
    fileRead.seek((pair+1)*frameSize,0)
    binary = fileRead.read(frameSize)
    fileWrite.write(binary)
    

fileRead.close()
fileWrite.close()

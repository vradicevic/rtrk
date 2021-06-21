
from cv2 import cv2
import io

videopath =  "D:\\Videosekvence\\yuv\\odabrani final\\odabrani_mirna.yuv"
savepath = "D:\\Videosekvence\\yuv\\odabrani final\\mirna.yuv"

fileRead = open(videopath,"rb")
fileWrite = open(savepath,'ab')
frameSize = 1280*720*2
ok = True

cnt=0


fileRead.seek(-4*frameSize,2)
binary = fileRead.read(frameSize)
fileWrite.write(binary)

binary = fileRead.read(frameSize)
fileWrite.write(binary)
binary = fileRead.read(frameSize)
fileWrite.write(binary)
binary = fileRead.read(frameSize)
fileWrite.write(binary)
    

fileRead.close()
fileWrite.close()

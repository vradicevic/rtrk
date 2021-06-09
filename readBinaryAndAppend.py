
from cv2 import cv2
import io

videopath = "D:\\Videosekvence\\yuv\\mirna_leftFullSequenceYUV444FPS30.yuv"
savepath = "D:\\Videosekvence\\yuv\\mirna_leftSELECTEDDD.yuv"

fileRead = open(videopath,"rb")
fileWrite = open(savepath,'wb')
frameSize = 1280*720*3
ok = True

cnt=0
pairs = [541,621,698,958,995]
for pair in pairs:
    fileRead.seek(pair*frameSize,0)
    binary = fileRead.read(frameSize)
    fileWrite.write(binary)
    fileRead.seek((pair+1)*frameSize,0)
    binary = fileRead.read(frameSize)
    fileWrite.write(binary)
    

fileRead.close()
fileWrite.close()

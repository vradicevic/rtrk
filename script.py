
from cv2 import cv2
import io
videopath = "D:\\VISION_SDK_02_12_01_00\\vision_sdk\\tools\\network_tools\\bin\\Videosekvence\\dummyNV12.yuv"
imagespath = "D:\\VISION_SDK_02_12_01_00\\vision_sdk\\tools\\network_tools\\bin\\Videosekvence\\singledummyNV12.yuv"


fileRead = open(videopath,"rb")
fileWrite = open(imagespath,'ab')
frameSize = int(1280*720*3/2)
ok = True

cnt=0
fileRead.seek(0*frameSize,0)
binary = fileRead.read(frameSize)
fileWrite.write(binary)
fileRead.seek((1)*frameSize,0)
binary = fileRead.read(frameSize)
fileWrite.write(binary)

    

fileRead.close()
fileWrite.close()

    

import framecollect as fc
import new_tss as tss
from cv2 import cv2
import io
videopath = "D:\\carPass.mp4"
imagespath = "D:\\car"

frame = cv2.imread(imagespath+"\\car150.png") 
filePath = imagespath+ "\\car150.yuv"
yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
f= io.BytesIO()
f.write(yuv.tobytes())
with open(filePath,'wb') as file:
    file.write(f.getbuffer())


frame = cv2.imread(imagespath+"\\car151.png") 
filePath = imagespath+ "\\car151.yuv"
yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
f= io.BytesIO()
f.write(yuv.tobytes())
with open(filePath,'wb') as file:
    file.write(f.getbuffer())
    
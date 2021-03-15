import framecollect as fc
import new_tss as tss
from cv2 import cv2
import io
videopath = "D:\\auticClosing.mp4"
imagespath = "D:\\auticClosing"


#fc.getFrames(videopath,0,500,imagespath,name="autic")



filePath = imagespath+ "\\auticALL.yuv"
f= io.BytesIO()
file = open(filePath,'wb')

for num in range(1,15,1):
    frame = cv2.imread(imagespath+"\\autic"+str(num)+".png") 
    yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
    f.write(yuv.tobytes())
    
file.write(f.getbuffer())
    

import framecollect as fc
import new_tss as tss
from cv2 import cv2
import io
videopath = "D:\\auticClosing.mp4"
imagespath = "D:\\auticClosing"


fc.getFrames(videopath,0,500,imagespath,name="autic")




for num in range(1,500,1):
    frame = cv2.imread(imagespath+"\\autic"+str(num)+".png") 
    filePath = imagespath+ "\\autic" +str(num)+".yuv"
    yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
    f= io.BytesIO()
    f.write(yuv.tobytes())
    with open(filePath,'wb') as file:
        file.write(f.getbuffer())
    

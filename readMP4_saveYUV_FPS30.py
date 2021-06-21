import framecollect as fc
from cv2 import cv2
import io

videopath = "F:\\izlaz.mp4"
savepath = "F:\\slijedniAutoOdabraniMovingDashboard.yuv"


file = open(savepath,'ab')

ok = True
f= io.BytesIO()
cnt=0
start =13500
video = cv2.VideoCapture(videopath)

fc.read_frame(video,start)
for i in range(0,100,1):
    ok,frame = fc.read_frame(video,1)
    if ok:
        yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
        file.write(yuv.tobytes())
    else :
        break
    

file.close()

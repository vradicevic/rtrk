import framecollect as fc
from cv2 import cv2
import io

videopath = "F:\\Videosekvence\\moving_dashboard720.mp4"
savepath = "F:\\Videosekvence\\moving_dashboardYUV444.yuv"


file = open(savepath,'ab')

ok = True
f= io.BytesIO()
cnt=0
video = cv2.VideoCapture(videopath)
for i in range(0,24120,60):
    ok,frame = fc.read_frame(video,59)
    if ok:
        yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
        file.write(yuv.tobytes())
        ok,frame = fc.read_frame(video,1)
        if ok:
            yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
            file.write(yuv.tobytes())
        else:
            break
    else :
        break
    

file.close()

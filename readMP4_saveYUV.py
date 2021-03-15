import framecollect as fc
from cv2 import cv2
import io

videopath = "D:\\Videosekvence\\uno.mp4"
savepath = "D:\\Videosekvence\\calm_centerYUV444.yuv"
video = cv2.VideoCapture(videopath)
file = open(savepath,'wb')
ok = True
f= io.BytesIO()
cnt=0
ok,frame = fc.read_frame(video,0)
while cnt<60:
    if ok:
        cnt+=1
        yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
        f.write(yuv.tobytes())
        ok,frame = fc.read_frame(video,0)

file.write(f.getbuffer())

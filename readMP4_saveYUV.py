import framecollect as fc
from cv2 import cv2
import io

videopath = "D:\\Videosekvence\\mirna_right720.mp4"
savepath = "D:\\Videosekvence\\YUV\\test.yuv"
video = cv2.VideoCapture(videopath)
file = open(savepath,'wb')

ok = True
f= io.BytesIO()
cnt=0
ok,frame = fc.read_frame(video,int(94.5*60))

while cnt<120:
    if ok:
        cnt+=1
        yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
        f.write(yuv.tobytes())
        ok,frame = fc.read_frame(video,0)
    else:
        break

file.write(f.getbuffer())

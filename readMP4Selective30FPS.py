import framecollect as fc
from cv2 import cv2
import io

videopath = "D:\\Videosekvence\\mirna_left720.mp4"
savepath = "D:\\Videosekvence\\yuv\\mirna_leftFullSequenceYUV444FPS30.yuv"


file = open(savepath,'wb')

ok = True
f= io.BytesIO()
cnt=0
video = cv2.VideoCapture(videopath)
ok,frame = fc.read_frame(video,1080)
for i in range(1080,6720,1):
    ok,frame = fc.read_frame(video,0)
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

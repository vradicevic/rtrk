from paths import *
from cv2 import cv2
import io
import framecollect as fc

videoPath = "D:\\Videosekvence\\moving_dashboard720.mp4"

video = cv2.VideoCapture(videoPath)
ok = True
while ok:
    ok,frame = fc.read_frame(video,50)
    cv2.imshow("video", frame)
    cv2.waitKey(delay=10)

import sys
import numpy as np
from cv2 import cv2 
import new_tss

import copy
import ebma
import framecollect as fc

videopath = "casa_360.mp4"
prevFrame= "C:/Users/Valentin/Pictures/frame1.png"
frame = "C:/Users/Valentin/Pictures/frame2.png"
yuvVideoSequence = "D:\\ProgramskiDokumenti\\VisualStudio\\YUV\\captureYUV422P.yuv"
width,height= 1280, 720
#framecollect.getFrames(videopath)
#cv2.arrowedLine(image, start_point, end_point, color, thickness)
"""
cv2.imread(prevFrame)
editedFrame = new_tss.main(cv2.imread(prevFrame),cv2.imread(frame))
cv2.imshow(videopath,editedFrame)
cv2.waitKey()

"""

def run_TSS2FramesFromYUV():
    yuvPrevFrame = new_tss.frameFromYUV422(yuvVideoSequence,5, width,height)
    yuvPrevFrame = cv2.cvtColor(yuvPrevFrame, cv2.COLOR_YUV2BGR_YUYV)
    yuvCurrentFrame = new_tss.frameFromYUV422(yuvVideoSequence,6,width,height)
    yuvCurrentFrame = cv2.cvtColor(yuvCurrentFrame, cv2.COLOR_YUV2BGR_YUYV)
    editedFrame = new_tss.main(yuvPrevFrame,yuvCurrentFrame)
    cv2.imshow("Python TSS",editedFrame)
    cv2.waitKey()


def run_TSSvideo(videopath):
    video = cv2.VideoCapture(videopath)
    
    
    prevFrame = None
    
    count=True
    while video.isOpened():
        
        ret, frame = video.read()
        
        if count:
            prevFrame = frame
            count = False
        
        editedFrame = new_tss.main(prevFrame,frame,blockSize=8)
        prevFrame = frame
        

        cv2.imshow(videopath,editedFrame)
        if cv2.waitKey(1) == ord('q'):
            break
        
  
    video.release()
    
    cv2.destroyAllWindows()

def run_EBMAvideo(videopath):
    video = cv2.VideoCapture(videopath)
    
    prevFrame = None
    count=True
    while video.isOpened():
        
        ret, frame = video.read()
        
        if count:
            prevFrame = frame
            count = False
        
        editedFrame = ebma.main(prevFrame,frame, blockSize=8)
        prevFrame = frame
       
        cv2.imshow(videopath,editedFrame)
        if cv2.waitKey(1) == ord('q'):
            break
        
    
    video.release()
    
    cv2.destroyAllWindows()
def run_TSS2frames(frame, prevFrame):
    
    editedFrame = new_tss.main(cv2.imread(prevFrame),cv2.imread(frame))
    cv2.imshow(videopath,editedFrame)
    cv2.waitKey()
def run_EBMA2frames(frame, prevFrame):
    
    editedFrame = ebma.main(cv2.imread(prevFrame),cv2.imread(frame))
    cv2.imshow(videopath,editedFrame)
    cv2.waitKey()


#run_TSS2FramesFromYUV()
#run_TSSvideo(videopath)
#run_EBMAvideo(videopath)
#run_EBMA2frames(frame,prevFrame)
run_TSS2frames(frame,prevFrame)
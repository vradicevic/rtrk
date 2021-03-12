import numpy as np
from cv2 import cv2
import random
import time
import os
import copy

debug = True


def getPngFromYUV444(path,width,height):
    file = open(path,'rb')
    yuv = np.frombuffer(file.read(width*height*3), dtype=np.uint8).reshape(height,width,3)
    file.close()
    png = cv2.cvtColor(yuv,cv2.COLOR_YUV2RGB)
    return png


def frameFromYUV422(videosequenceName, frameNumber,width,height):
    frameSize = width*height*2
    file_size = os.stat(videosequenceName).st_size
    n_frames = file_size // frameSize
    file = open(videosequenceName,'rb')
    file.seek(frameSize*(frameNumber))
    yuv = np.frombuffer(file.read(frameSize), dtype=np.uint8).reshape(height,width,2)
    file.close()
    return yuv


def YCrCb2BGR(image):
    """
    Converts numpy image into from YCrCb to BGR color space
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

def BGR2YCrCb(image):
    """
    Converts numpy image into from BGR to YCrCb color space
    """
    return cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)

def segmentImage(anchor, blockSize=8):
    """
    Determines how many macroblocks an image is composed of
    :param anchor: I-Frame
    :param blockSize: Size of macroblocks in pixels
    :return: number of rows and columns of macroblocks within
    """
    h, w = anchor.shape
    hSegments = int(h / blockSize)
    wSegments = int(w / blockSize)
    totBlocks = int(hSegments * wSegments)

    #if debug:
    #    print(f"Height: {h}, Width: {w}")
    #    print(f"Segments: Height: {hSegments}, Width: {wSegments}")
    #    print(f"Total Blocks: {totBlocks}")

    return hSegments, wSegments

def getCenter(x, y, blockSize):
    """
    Determines center of a block with x, y as top left corner coordinates and blockSize as blockSize
    :return: x, y coordinates of center of a block
    """
    return (int(x + blockSize/2), int(y + blockSize/2))

def getAnchorSearchArea(x, y, blockSize, searchArea = 7):
    """
    Returns image of anchor search area
    :param x, y: top left coordinate of macroblock in Current Frame
    :param anchor: I-Frame
    :param blockSize: size of block in pixels
    :param searchArea: size of search area in pixels
    :return: Image of anchor search area
    """
    #h, w = anchor.shape
    cx, cy = getCenter(x, y, blockSize)

    sx = max(0, cx-int(blockSize/2)-searchArea) # ensure search area is in bounds
    sy = max(0, cy-int(blockSize/2)-searchArea) # and get top left corner of search area

    # slice anchor frame within bounds to produce anchor search area
    #anchorSearch = anchor[sy:min(sy+searchArea*2+blockSize, h), sx:min(sx+searchArea*2+blockSize, w)]

    return sx,sy

def getBlockZone(p, anchor, tBlock, blockSize):
    """
    Retrieves the block searched in the anchor search area to be compared with the macroblock tBlock in the current frame
    :param p: x,y coordinates of macroblock center from current frame
    :param aSearch: anchor search area image
    :param tBlock: macroblock from current frame
    :param blockSize: size of macroblock in pixels
    :return: macroblock from anchor
    """
    h,w = anchor.shape
    px, py = p # coordinates of macroblock center
    px, py = max(0,int(px-blockSize/2)),max(0, int(py-blockSize/2)) # get top left corner of macroblock
    #px, py = max(0,px), max(0,py) # ensure macroblock is within bounds
    px,py = min(px,w-blockSize),min(py, h-blockSize)

    aBlock = anchor[py:py+blockSize, px:px+blockSize] # retrive macroblock from anchor search area


    try:
        assert aBlock.shape == tBlock.shape # must be same shape

    except Exception as e:
        print(e)
        print(f"ERROR - ABLOCK SHAPE: {aBlock.shape} != TBLOCK SHAPE: {tBlock.shape}")

    return aBlock,px,py
def mannualMAD(tBlock, aBlock):
    sumMAD = 0
    for y in range(0,8,1):
        for x in range(0,8,1):
            sumMAD += np.abs(tBlock[x][y] - aBlock[x][y])
            
    return sumMAD/(8*8)

def getMAD(tBlock, aBlock):
    """
    Returns Mean Absolute Difference between current frame macroblock (tBlock) and anchor frame macroblock (aBlock)
    """
    return np.sum(np.abs(np.subtract(tBlock, aBlock)))/(tBlock.shape[0]*tBlock.shape[1])

def getBestMatch(tBlock,anchor,sx,sy,blockSize,x,y,step=11): #3 Step Search
    
    
    #ah, aw = aSearch.shape
    acy, acx = int(y+blockSize/2), int(x + blockSize/2) # get center of anchor search area

    minMAD = float("+inf")
    minP = None

    while step >= 1:
        p1 = (acx, acy)
        p2 = (acx+step, acy)
        p3 = (acx, acy+step)
        p4 = (acx+step, acy+step)
        p5 = (acx-step, acy)
        p6 = (acx, acy-step)
        p7 = (acx-step, acy-step)
        p8 = (acx+step, acy-step)
        p9 = (acx-step, acy+step)
        pointList = [p1,p2,p3,p4,p5,p6,p7,p8,p9] # retrieve 9 search points

        for p in range(len(pointList)):
            aBlock,px1,py1 = getBlockZone(pointList[p], anchor, tBlock, blockSize) # get anchor macroblock
            MAD = getMAD(tBlock, aBlock) # determine MAD
            if MAD < minMAD: # store point with minimum MAD
                minMAD = MAD
                minP = (px1,py1)
                acx, acy = int(px1 + blockSize/2), int(py1+blockSize/2)
            else:
                minP = (acx- int(blockSize/2), acy- int(blockSize/2))

        step = int(step/2)
    
    px, py = minP # center of anchor block with minimum MAD
    #px, py = px - int(blockSize / 2), py - int(blockSize / 2) # get top left corner of minP
    #px, py = max(0, px), max(0, py) # ensure minP is within bounds
    #matchBlock = aSearch[py:py + blockSize, px:px + blockSize] # retrieve best macroblock from anchor search area

    return px,py

def blockValueDeviation(block,blockSize):
    sum= 0
    for y in range(0,8,1):
        for x in range(0,8,1):
            sum += block[x][y]
    mean= sum/(blockSize*blockSize)
    deviationSum=0
    for y in range(0,8,1):
        for x in range(0,8,1):
            deviationSum += abs(mean-block[x][y])
    return deviationSum




def blockSearchBody(anchor, target, blockSize, searchArea=400,step=11):
    """
    Facilitates the creation of a predicted frame based on the anchor and target frame
    :param anchor: I-Frame
    :param target: Current Frame to create a P-Frame from
    :param blockSize: size of macroBlock in pixels
    :param searchArea: size of searchArea extended from blockSize
    :return: predicted frame
    """
    h, w = anchor.shape
    hSegments, wSegments = segmentImage(anchor, blockSize)


    #predicted = np.ones((h, w))*255
    bcount = 0
    vectors=[]
    for y in range(0, int(hSegments*blockSize), blockSize):
        for x in range(0, int(wSegments*blockSize), blockSize):
            
            targetBlock = target[y:y+blockSize, x:x+blockSize] #get current macroblock
            sumDev = blockValueDeviation(targetBlock,blockSize)
    
            if sumDev>500:
                print(sumDev)
                sx, sy = getAnchorSearchArea(x, y, blockSize, searchArea) #get anchor search area
                
                #print("AnchorSearchArea: ", anchorSearchArea.shape)
                
                px,py = getBestMatch(targetBlock,anchor,sx,sy, blockSize,x,y,step) #get best anchor macroblock
            
                #predicted[y:y+blockSize, x:x+blockSize] = anchorBlock #add anchor block to predicted frame
                
                vectors.append((px,py))
            else:
                
                vectors.append((x,y))
            
            
            bcount+=1
            
            #cv2.imwrite("OUTPUT/predictedtestFrame.png", predicted)
            #print(f"ITERATION {bcount}")

    #cv2.imwrite("OUTPUT/predictedtestFrame.png", predicted)

    #time.sleep(10)

    assert bcount == int(hSegments*wSegments) #check all macroblocks are accounted for

    return vectors


def preprocess(anchor, target, blockSize):

    if isinstance(anchor, str) and isinstance(target, str):
        anchorFrame = BGR2YCrCb(cv2.imread(anchor))[:, :, 0] # get luma component
        targetFrame = BGR2YCrCb(cv2.imread(target))[:, :, 0] # get luma component

    elif isinstance(anchor, np.ndarray) and isinstance(target, np.ndarray):
        anchorFrame = BGR2YCrCb(anchor)[:, :, 0] # get luma component
        targetFrame = BGR2YCrCb(target)[:, :, 0] # get luma component

    else:
        raise ValueError

    #resize frame to fit segmentation
    hSegments, wSegments = segmentImage(anchorFrame, blockSize)
    anchorFrame = cv2.resize(anchorFrame, (int(wSegments*blockSize), int(hSegments*blockSize)))
    targetFrame = cv2.resize(targetFrame, (int(wSegments*blockSize), int(hSegments*blockSize)))

    #if debug:
        #print(f"A SIZE: {anchorFrame.shape}")
        #print(f"T SIZE: {targetFrame.shape}")


    return (anchorFrame, targetFrame)

def main(anchorFrame, targetFrame, outfile="OUTPUT", saveOutput=False, blockSize = 8,step=11):
    """
    
    :param anchor: file path of I-Frame or I-Frame
    :param target: file path of Current Frame or Current Frame
    :return: image with vectors
    """
    editedFrame = copy.copy(targetFrame)
    anchorFrame, targetFrame = preprocess(anchorFrame, targetFrame, blockSize) #processes frame or filepath to frame
    
    hSegments, wSegments = segmentImage(anchorFrame, blockSize)
    vectors = blockSearchBody(anchorFrame, targetFrame, blockSize)
    #print(str(step)+str(blockSize))
    bcount = 0
    
    

    
    

    return vectors


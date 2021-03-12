import numpy as np
import cv2
import random
import time
import os
import copy

debug = True

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

def getAnchorSearchArea(x, y,anchor, blockSize, searchArea = 3):
    """
    Returns image of anchor search area
    :param x, y: top left coordinate of macroblock in Current Frame
    :param anchor: I-Frame
    :param blockSize: size of block in pixels
    :param searchArea: size of search area in pixels
    :return: Image of anchor search area
    """
    h, w = anchor.shape
    cx, cy = getCenter(x, y, blockSize)

    sx = max(0, cx-int(blockSize/2)-searchArea) # ensure search area is in bounds
    sy = max(0, cy-int(blockSize/2)-searchArea) # and get top left corner of search area

    # slice anchor frame within bounds to produce anchor search area
    anchorSearch = anchor[sy:min(sy+searchArea*2+blockSize, h), sx:min(sx+searchArea*2+blockSize, w)]
    h,w = anchorSearch.shape
    return sx,sy,w,h

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

def getBestMatch(tBlock,anchor,sx,sy,h,w,blockSize,x,y): #3 Step Search
    """
    Implemented 3 Step Search. Read about it here: https://en.wikipedia.org/wiki/Block-matching_algorithm#Three_Step_Search
    :param tBlock: macroblock from current frame
    :param aSearch: anchor search area
    :param blockSize: size of macroblock in pixels
    :return: macroblock from anchor search area with least MAD
    """
    
    
    minMAD = float("+inf")
    minP = None
    h= h-8
    w= w-8
    for y_seg in range(0,h+1,1):
        for x_seg in range(0, w+1, 1):
            p = (sx+x_seg+int(blockSize/2),sy + y_seg+ int(blockSize/2)) # sredina trenutnog bloka
            aBlock,px1,py1 = getBlockZone(p, anchor, tBlock, blockSize) # get anchor macroblock
            MAD = mannualMAD(tBlock, aBlock) # determine MAD
            if MAD < minMAD: # store point with minimum MAD
                if MAD < 0.01:
                    minMAD = MAD
                    minP = (px1,py1)
                else:
                    minP = (x, y)

        

    px, py = minP # center of anchor block with minimum MAD
    #px, py = px - int(blockSize / 2), py - int(blockSize / 2) # get top left corner of minP
    #px, py = max(0, px), max(0, py) # ensure minP is within bounds
    #matchBlock = aSearch[py:py + blockSize, px:px + blockSize] # retrieve best macroblock from anchor search area

    return px,py



def blockSearchBody(anchor, target, blockSize, searchArea=16):
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

            sx, sy,w_anchor,h_anchor = getAnchorSearchArea(x, y,anchor, blockSize, searchArea) #get anchor search area
            #new_Anchor = copy.copy(anchor)
            #drawedanchor = cv2.rectangle(new_Anchor, (sx,sy),( sx+w_anchor,sy+h_anchor), (0,255,0), 1)
            #cv2.imshow("Podrucje pretrage", drawedanchor)
            
            #print("AnchorSearchArea: ", anchorSearchArea.shape)

            px,py = getBestMatch(targetBlock,anchor,sx,sy,w_anchor,h_anchor, blockSize,x,y) #get best anchor macroblock
            
            #predicted[y:y+blockSize, x:x+blockSize] = anchorBlock #add anchor block to predicted frame
            
            vectors.append((px,py))
            
            
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

def main(anchorFrame, targetFrame, outfile="OUTPUT", saveOutput=False, blockSize = 8):
    """
    
    :param anchor: file path of I-Frame or I-Frame
    :param target: file path of Current Frame or Current Frame
    :return: image with vectors
    """
    editedFrame = copy.copy(targetFrame)
    anchorFrame, targetFrame = preprocess(anchorFrame, targetFrame, blockSize) #processes frame or filepath to frame
    
    hSegments, wSegments = segmentImage(anchorFrame, blockSize)
    vectors = blockSearchBody(anchorFrame, targetFrame, blockSize)
    
    bcount = 0
    for y in range(0, int(hSegments*blockSize), blockSize):
            for x in range(0, int(wSegments*blockSize), blockSize):
                if (x,y) != vectors[bcount] :
                        #print((x,y))
                        #print(vectors[bcount])
                    cv2.arrowedLine(editedFrame,vectors[bcount],(x,y), (0,255,0), 1)
                bcount = bcount + 1
    #residualFrame = getResidual(targetFrame, predictedFrame)
    #naiveResidualFrame = getResidual(anchorFrame, targetFrame)
    #reconstructTargetFrame = getReconstructTarget(residualFrame, predictedFrame)
    #showImages(targetFrame, predictedFrame, residualFrame)

    #residualMetric = getResidualMetric(residualFrame)
    #naiveResidualMetric = getResidualMetric(naiveResidualFrame)

    
    

    return editedFrame

if __name__ == "__main__":
    pass
    """
    anchorPath = "testImages/personFrame1.png"
    targetPath = "testImages/personFrame2.png"
    main(anchorPath, targetPath)
    """
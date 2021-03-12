from cv2 import cv2
import numpy as np
import os
import subprocess as sp
from cv2 import cv2
import pathlib


path ="C:\\Users\\rvalentin\\Desktop\\vectors.bin"


vectorsFile = open(path,"r+")
buffer = np.fromfile(vectorsFile,dtype=np.int_)
vectors = []

for i in range(0,len(buffer),2):
    vectors.append((buffer[i:i+2]))
    
print(vectors[35][0])


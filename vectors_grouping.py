import numpy as np
import kmeansold as kmeans
from cv2 import cv2

pathVectors = "D:\\vektori\\carAwayWhiteTSSBlock32Step35.bin"
#pathVectors = "D:\\auticBlock32Step35.bin"
#pathVectors= "D:\\Visual Studio Code\\rtrk\\vectors\\vektoriAutic327BLOCK32.bin"
# pathVectors= "D:\\Visual Studio Code\\rtrk\\vectors\\vektoriAutic327BLOCK8.bin"
vectorsFile = open(pathVectors,"r+")
buffer = np.fromfile(vectorsFile,dtype=np.int_)
vectorsFile.close()
vectors = []

for i in range(0,len(buffer),6):
    if(buffer[i+4]>2):
        itemFeatures = []
        value = buffer[i]
        itemFeatures.append(value)
        value = buffer[i+1]
        itemFeatures.append(value)
        value = buffer[i+2]
        
        itemFeatures.append(value)
        value = buffer[i+3]
        itemFeatures.append(value)
        value = buffer[i+4]
        itemFeatures.append(value)
        value = buffer[i+5]
        itemFeatures.append(value)
        vectors.append(itemFeatures)

k= 3
means = kmeans.CalculateMeans(k,vectors,maxIterations=10000)
clusters = kmeans.FindClusters(means, vectors)

pathImage = "D:\\car\\car116.png"
#pathImage = "D:\\auticNew\\autic328.png"
#pathImage = "D:\\car\\car116.png"
png = cv2.imread(pathImage)
boje=[(255,0,0),(0,255,0),(0,0,255),(255,255,255),(255,255,0),(255,0,255)]
saveImagePath = "D:\\Clustering Results\\PC\\carAwayWhiteTSSBlock32Step35.png"

index = 0
for cluster in clusters:
    boja = boje[index]
    for item in cluster:
        cv2.arrowedLine(png,(item[0],item[1]), (item[2],item[3]),boja, 1)
    index+=1
index=0
#cv2.imwrite(saveImagePath,png)
cv2.imshow("FRame",png)
cv2.waitKey()
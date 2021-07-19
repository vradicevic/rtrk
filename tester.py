import numpy as np

vectorsFile = open("C:\\Dummy evaluacija\\1280x720\\Vektori\\EBMA_128x72_Up_Step=15.bin","r+")
buffer = np.fromfile(vectorsFile,dtype=np.int16)
vectors = []
numOfVs = int(len(buffer)/6)


for i in range(0,len(buffer),6):
    vectors.append((buffer[i:i+6])) 
    #svaki vektor je složen od 5 integera na sljedeći način u bin-u
    # ::from-[0]=x i [1]=y   2 integera jedan x drugi y 
    # ::to- [2]=x i  [3]=y  2 integera jedan x drugi y 
    # ::length- [4] 1 integer udaljenosti from i to točke
    # ::angle- [5] 1 integer kut vektora
vectorsFile.close()
for i in range(0,numOfVs,1):
    print(vectors[i][5])
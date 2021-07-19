import numpy as np


def ReadVectors(vectorsPath):
    vectorsFile = open(vectorsPath,"r+")
    buffer = np.fromfile(vectorsFile,dtype=np.int16)
    vectors = []
    numOfVs = int(len(buffer)/6)


    for i in range(0,len(buffer),6):
        vectors.append((buffer[i:i+6])) 
        #svaki vektor je složen od 6 integera na sljedeći način u bin-u
        # ::from-[0]=x i [1]=y   2 integera jedan x drugi y 
        # ::to- [2]=x i  [3]=y  2 integera jedan x drugi y 
        # ::length- [4] 1 integer udaljenosti from i to točke
        # ::angle- [5] 1 integer kut vektora
    vectorsFile.close()
    return numOfVs,vectors

def EvaluateVectors(vectors,numOfVs,truth):
    ok=0
    for vector in vectors:
        
        if(vector[4]==truth[0] and vector[5]==truth[1]):
            
            ok+=1

    return ok
            




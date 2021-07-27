from drawClusteredVectors import *

rootPath = "D:\\vektori\\"
for z in range(0,40,2):
    vectorsPath= rootPath +"vectors"+str(z) + ".bin"
    belongsToPath = rootPath +"belongsTo"+str(z) + ".bin"
    
    

    DrawClusteredVectors(vectorsPath,belongsToPath,videoMirna,z+1,1280,720)
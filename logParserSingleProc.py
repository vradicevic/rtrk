#TOOL FOR READING TERA TERM LOGS
################################################################
import numpy as np
import xlwt
from xlwt import Workbook

def parseBMA(words, id):
    #word+1 = "]" 
    #word+2 = ""
    values = words[id].split("=")
    frame = values[1]
    values = words[id+1].split("=")
    time = values[1]
    log= [int(frame),int(time)]
    return log


def parsePREP(words,id):
    values = words[id].split("=")
    frame = values[1]
    values = words[id+2].split("=")
    numOfVs = values[1]
    log= [int(frame),int(numOfVs)]
    return log

def parseKMEAN(words,id):
    values = words[id].split("=")
    frame = values[1]
    values = words[id+1].split("=")
    time = values[1]
    values = words[id+2].split("=")
    numOfVs = values[1]
    log= [int(frame),int(time),int(numOfVs)]
    return log
    


def parse (log, broj_pon):
    #logBMAHOST = [] #list for storing execution time
    logBMADSP1 = []
    #logBMADSP2 = []
    logKMEAN = []
    logPREP = []
   
    for logline in log:
        words = logline.split()
        for i, word in enumerate(words):
            
                if word == '[HOST':
                    
                    if words[i+2][0:5]=="KMEAN":
                        log = parseKMEAN(words,i+2)
                        logKMEAN.append(log)
                    

                
                if word == '[HOST':
                    if words[i+2][0:4]=="PREP":
                        log = parsePREP(words,i+2)
                        logPREP.append(log)

                if word == '[DSP1':
                    if words[i+2][0:3]=="BMA":
                        log = parseBMA(words,i+2)
                        logBMADSP1.append(log)
                

    
    return logBMADSP1,logKMEAN,logPREP




f = open("C:\\Users\\Valentin\\Documents\\RTRK Diplomski\\RTRK Diplomski\\logovi\\CODE_OPTI_1PROC\\MYBMA_dummy_block=32.log", "r")
log = f.read().split('\n')
f.close()
wb = Workbook()
sheet1 = wb.add_sheet("dummyMYBMA",cell_overwrite_ok=True)
sheet1.write(0,0, "BMA")
sheet1.write(1,0, "Frame")
sheet1.write(1,1, "A15 ms")
sheet1.write(1,2, "DSP1 ms")
sheet1.write(1,3, "DSP2 ms")
sheet1.write(1,4, "KMEAN Vs")
sheet1.write(1,5, "KMEAN ms")
sheet1.write(1,6, "PREP Vs")
offset = 2



broj_pon = {}                   #dictionary for storing execution time with its number of occurrence
logBMADSP1,logKMEAN,logPREP = parse(log, broj_pon)


for log in logBMADSP1:
    sheet1.write(offset+log[0],0, log[0])
    sheet1.write(offset+log[0],2, log[1])




for log in logKMEAN:
    sheet1.write(offset+log[0],4, log[2])
    sheet1.write(offset+log[0],5, log[1])

for log in logPREP:
    sheet1.write(offset+log[0],6, log[1])

wb.save("C:\\Users\\Valentin\\Documents\\RTRK Diplomski\\RTRK Diplomski\\logovi\\xls\\1PROCOPTI\\dummyMYBMA.xls")
    

    

########################################################################
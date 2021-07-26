#TOOL FOR READING TERA TERM LOGS
################################################################
import numpy as np
import xlwt
from xlwt import Workbook
import os

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
    logBMA=[]
    for logline in log:
        words = logline.split()
        for i, word in enumerate(words):
                if word == '[DSP1':
                    if words[i+2][0:3]=="BMA":
                        log = parseBMA(words,i+2)
                        logBMA.append(log)
                

    
    return logBMA



dirPath  = "D:\\logovi\\PC\\640x360\\Block=8\\NOOPTI\\"
file_list = os.listdir(dirPath)
wb = Workbook()
for file in file_list:

    f = open(dirPath+file, "r")
    log = f.read().split('\n')
    f.close()
    
    sheet1 = wb.add_sheet(file[0:-13],cell_overwrite_ok=True)
    sheet1.write(0,0, "BMA")
    sheet1.write(1,0, "Frame")
    sheet1.write(1,1, "Time ms")

    offset = 2



    broj_pon = {}                   #dictionary for storing execution time with its number of occurrence
    logBMA = parse(log, broj_pon)
    for log in logBMA:
        
        sheet1.write(offset+log[0],0, log[0])
        sheet1.write(offset+log[0],1, log[1])


wb.save(dirPath+"640x360NOOPTIblock=8.xls")
    

    

########################################################################
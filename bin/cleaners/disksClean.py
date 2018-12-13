###############################################################
# disksClean.py
# last updated 03.12.2018
# purpose : disks cleaner module for log parser module
## authors: luckyducky + lamehacker
################################################################

import os

import pandas as pd
import csv

# for holding purposes manually entering machine ID from preferences (needs to be entered as a string)
LogID = []
captureTime = []
name = []
size = []
used = []
free = []
pctused = []
fileSys = []
mountPoint = []

# remove headers () and empty lists ()

def generateLogID(logCount, timeForLogID, machineID):
    if logCount <= 9 and logCount >= 0:
        placeholder = '000'
    elif logCount <= 99 and logCount >= 10:
        placeholder = '00'
    elif logCount > 99:
        placeholder = '0'
    date = timeForLogID[13:23]
    LogID.append(machineID + '_' + str(date) + '[' + placeholder + str(logCount + 1) + ']')


def initiator(dataDir, machineID, logPath):

    logCount = 0
    timestampFix = 0
    timeStamp = ''

    os.chdir(dataDir)

    # remove creation of .xlsx file

    os.chdir(logPath)
    with open('disks.log') as disksLog:
        for line in disksLog:

            if line.startswith('</log>') == True:
                logCount += 1

            if line.startswith('<captureTime>') == True:
                timeStamp = line

            if line.startswith('<name>') == True:
                name.append(line)
                captureTime.append(timeStamp)
                timestampFix += 1
                generateLogID(logCount, timeStamp, machineID)

            elif line.startswith('<size>') == True:
                size.append(line)

            elif line.startswith('<used>') == True:
                used.append(line)

            elif line.startswith('<free>') == True:
                free.append(line)

            elif line.startswith('<%used>') == True:
                pctused.append(line)

            elif line.startswith('<fileSys>') == True:
                fileSys.append(line)

            elif line.startswith('<mountPoint>') == True:
                mountPoint.append(line)

    df = pd.DataFrame(list(zip(LogID, captureTime, name, size, used, free, pctused, fileSys, mountPoint)))

    stuffToIgnore = ['<captureTime>', '</captureTime>', '<name>', '</name>', '<size>', '</size>', '<used>', '</used>',
                     '<free>', '</free>', '<%used>', '</%used>', '<fileSys>', '</fileSys>', '<mountPoint>',
                     '</mountPoint>', '\n']

    for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex=True)

    os.chdir(dataDir)

    df.to_csv('disksLog.csv')
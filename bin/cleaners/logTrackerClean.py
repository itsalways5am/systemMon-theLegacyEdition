###############################################################
# logTrackerClean.py
# last updated 24.11.2018
# purpose : logTracker cleaner module for log parser module
## authors: luckyducky + lamehacker + calebpitts
################################################################

import os

import pandas as pd
import csv

# for holding purposes manually entering machine ID from preferences (needs to be entered as a string)
LogID = []
captureTime = []
bootTime = []
processes = []
disks = []
networkInterfaces = []
battery = []


# remove headers() and emptylists()

# function to define structure of logID


def generateLogID(logCount, timeForLogID, machineID):
    if logCount <= 9 and logCount >= 0:
        placeholder = '000'
    elif logCount <= 99 and logCount >= 10:
        placeholder = '00'
    elif logCount > 99:
        placeholder = '0'
    date = timeForLogID[13:23]
    LogID.append(machineID + '_' + str(date) + '[' + placeholder + str(logCount) + ']')


def initiator(dataDir, machineID, logPath):
    i = 12
    logCount = 0

    os.chdir(dataDir)

    # remove creation of .xlsx

    os.chdir(logPath)
    with open('logTracker.log') as logTrackerLog:
        for line in logTrackerLog:

            if line.startswith('<log>') == True:
                i = 1
                continue
            if line.startswith('</log>') == True:
                logCount += 1
                generateLogID(logCount, timeForLogID, machineID)
                i = 11
                continue

            if i == 1:
                captureTime.append(line)
                timeForLogID = line
            elif i == 3:
                bootTime.append(line)
            elif i == 4:
                processes.append(line)
            elif i == 5:
                disks.append(line)
            elif i == 6:
                networkInterfaces.append(line)
            elif i == 7:
                battery.append(line)
            i += 1
    # creates dataframe using list(zip('name of lists to be zipped into dataFrame'))
    df = pd.DataFrame(list(zip(LogID, captureTime, bootTime, processes, disks, networkInterfaces, battery)))

    # creating list of strings for regex to strip prior to putting in dataFrame
    stuffToIgnore = ['<captureTime>', '</captureTime>', '<bootTime>', '</bootTime>', '<processes>', '</processes>',
                     '<disks>', '</disks>', '<networkInterfaces>', '</networkInterfaces>', '<battery>', '</battery>',
                     '\n']

    # needed to add a separate line for \n removal cause it wasn't working in the stuffToIgnore
    df = df.replace("\n", "", regex=True)
    for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex=True)

    os.chdir(dataDir)

    df.to_csv('logTrackerLog.csv')

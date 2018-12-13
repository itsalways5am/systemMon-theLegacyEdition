##########################################################
# processesClean.py
# last updated 03-12.2018
# purpose : proccesses cleaning module for log parser module
## authors: luckyducky + lamehacker + calebpitts
################################################################

import os

import pandas as pd
import csv

# for holding purposes manually entering machine ID from preferences (needs to be entered as a string)
LogID = []
captureTime = []
pid = []
parentPID = []
name = []
cpu = []
priority = []
mem = []
vms = []
rss = []
user = []
path = []


# remove headers and empty lists .csv conversion 2018-12-02

# function to definie strucutre of LogID
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

    os.chdir(logPath)
    with open('processes.log') as processesLog:
        for line in processesLog:

            if line.startswith('</log>') == True:
                logCount += 1

            if line.startswith('<captureTime>') == True:
                timeStamp = line

            if line.startswith('<pid>') == True:
                pid.append(line)
                captureTime.append(timeStamp)
                timestampFix += 1
                generateLogID(logCount, timeStamp, machineID)

            elif line.startswith('<parentPID>') == True:
                parentPID.append(line)

            elif line.startswith('<name>') == True:
                name.append(line)

            elif line.startswith('<%cpu>') == True:
                cpu.append(line)

            elif line.startswith('<priority>') == True:
                priority.append(line)

            elif line.startswith('<%mem>') == True:
                mem.append(line)

            elif line.startswith('<vms>') == True:
                vms.append(line)

            elif line.startswith('<rss>') == True:
                rss.append(line)

            elif line.startswith('<user>') == True:
                user.append(line)

            elif line.startswith('<path>') == True:
                path.append(line)

    df = pd.DataFrame(
        list(zip(LogID, captureTime, pid, parentPID, name, cpu, priority, mem, vms, rss, user, path)))

    stuffToIgnore = ['<captureTime>', '</captureTime>', '<pid>', '</pid>', '<parentPID>', '</parentPID>', '<name>',
                     '</name>', '<%cpu>', '</%cpu>', '<priority>', '</priority>', '<%mem>', '</%mem>', '<vms>',
                     '</vms>', '<rss>', '</rss>', '<user>', '</user>', '<path>', '</path>', '\n']

    for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex=True)

    os.chdir(dataDir)

    df.to_csv('processesLog.csv')


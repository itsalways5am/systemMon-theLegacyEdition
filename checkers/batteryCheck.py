###############################################################
# batteryCheck.py
# last updated 27.11.2018
# purpose : checks cleaned and raw battery files for discrepencies.
# authors: calebpitts
################################################################

from collections import defaultdict
import pandas as pd
import os
import re
import glob

TAG_RE = re.compile(r'<[^>]+>')  # Regex constraint for removing XML tags


# Gets col data from excel files
def get_clean_cols(data_path, col_dict):
    df = pd.read_excel(io=data_path)

    # Puts column data into lists
    for col in list(df):
        col_list = df[col].tolist()
        col_dict[col] = col_list

    return col_dict


# Gets battery data from raw log file
def get_battery_data(dir, raw_dict):
    with open(dir) as file:
        for line in file:
            if line.startswith('<captureTime>'):
                raw_dict['captureTime'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<supported>'):
                raw_dict['supported'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<detected>'):
                raw_dict['detected'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<charge>'):
                raw_dict['charge'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<remaining>'):
                raw_dict['remaining'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<status>'):
                raw_dict['status'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<plugged>'):
                raw_dict['plugged'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags

    return raw_dict


# Compares the corresponding raw and cleaned block of data. Returns False if discrepancy encountered.
def compare_block(col_name, raw_name, col_dict, raw_dict):
    block_discrepencies = []
    print("Checking {}...".format(col_name))
    for num, (col, raw) in enumerate(zip(col_dict[col_name], raw_dict[raw_name])):
        # print("COL:", str(col), "- RAW:", str(raw))  # Prints exact comparisons.
        if str(raw) != str(col):
            print("COL:", str(col), "- RAW:", str(raw))  # Prints exact comparisons.
            block_discrepencies.append("Discrepency in col '{}' row ".format(col_name) + str(num + 2))
    return block_discrepencies


# Provides output and insight as to whether there are any discrepencies between the clean and raw data.
def compare_data(col_dict, raw_dict):
    discrepencies = []
    try:
        discrepencies += compare_block("Log time", "captureTime", col_dict, raw_dict)
        discrepencies += compare_block("Battery supported", "supported", col_dict, raw_dict)
        discrepencies += compare_block("Battery detected", "detected", col_dict, raw_dict)
        discrepencies += compare_block("Current charge", "charge", col_dict, raw_dict)
        discrepencies += compare_block("Battery reamining for", "remaining", col_dict, raw_dict)
        discrepencies += compare_block("Charging status", "status", col_dict, raw_dict)
        discrepencies += compare_block("Plugged in", "plugged", col_dict, raw_dict)

    except TypeError:
        print("One of the columns had a different number of rows.")

    return discrepencies


def main(data_path, log_path):
    raw_dict = defaultdict(list)
    col_dict = defaultdict(list)

    col_dict = get_clean_cols(data_path, col_dict)
    os.chdir(log_path)

    # Listing all sub-directories for logs
    logSubDir = glob.glob('*', recursive=False)

    # Iterating through every sub-directory, finding all log files and running appropriate cleaner script
    for subDir in logSubDir:
        os.chdir(subDir)

        logFileList = []
        logFileList = glob.glob('*.log', recursive=False)

        # Iterates through logs for raw data collection.
        for logFile in logFileList:
            if logFile == 'battery.log':
                print('Running batteryLog check for date: ' + subDir)
                raw_dict = get_battery_data(str(os.getcwd()) + '/battery.log', raw_dict)

        os.chdir('../')

    print()
    return compare_data(col_dict, raw_dict)


if __name__ == '__main__':
    main()

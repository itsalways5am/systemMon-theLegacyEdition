###############################################################
# processesCheck.py
# last updated 30.11.2018
# purpose : checks cleaned and raw processes files for discrepencies.
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


# Gets processes data from raw log file
def get_processes_data(dir, raw_dict):
    with open(dir) as file:
        for line in file:
            if line.startswith('<captureTime>'):
                raw_dict['captureTime'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<pid>'):
                raw_dict['pid'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<parentPID>'):
                raw_dict['parentPID'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<name>'):
                raw_dict['name'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<cpu>'):
                raw_dict['cpu'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<priority>'):
                raw_dict['priority'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<mem>'):
                raw_dict['mem'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<vms>'):
                raw_dict['vms'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<rss>'):
                raw_dict['rss'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<user>'):
                raw_dict['user'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<path>'):
                raw_dict['path'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags

    return raw_dict


# Provides output and insight as to whether there are any discrepencies between the clean and raw data.
def compare_data(col_dict, raw_dict):
    discrepencies = []
    try:
        discrepencies += compare_block("Log time", "captureTime", col_dict, raw_dict)
        discrepencies += compare_block("PID", "pid", col_dict, raw_dict)
        discrepencies += compare_block("Parent PID", "parentPID", col_dict, raw_dict)
        discrepencies += compare_block("Process name", "name", col_dict, raw_dict)
        discrepencies += compare_block("% CPU", "cpu", col_dict, raw_dict)
        discrepencies += compare_block("Priority", "priority", col_dict, raw_dict)
        discrepencies += compare_block("% Mem", "mem", col_dict, raw_dict)
        discrepencies += compare_block("vms", "vms", col_dict, raw_dict)
        discrepencies += compare_block("rss", "rss", col_dict, raw_dict)
        discrepencies += compare_block("User", "user", col_dict, raw_dict)
        discrepencies += compare_block("Patj", "path", col_dict, raw_dict)  # Patj is a misnamed col from cleaners module

    except TypeError:
        print("One of the columns in 'processes' had a different number of rows.")  # Occurs when mismatch in raw and cleaned lengths occur

    return discrepencies


# Compares the corresponding raw and cleaned block of data. Returns False if discrepancy encountered.
def compare_block(col_name, raw_name, col_dict, raw_dict):
    block_discrepencies = []
    print("Checking {}...".format(col_name))
    for num, (col, raw) in enumerate(zip(col_dict[col_name], raw_dict[raw_name])):
        # print("COL:", str(col), "- RAW:", str(raw))  # Prints exact comparisons.
        if raw != col:
            block_discrepencies.append("Discrepency in col '{}' row ".format(col_name) + str(num + 2))
    return block_discrepencies


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
            if logFile == 'processes.log':
                print('Running processesLog check for date: ' + subDir)
                raw_dict = get_processes_data(str(os.getcwd()) + '/processes.log', raw_dict)

        os.chdir('../')

    print()
    return compare_data(col_dict, raw_dict)


if __name__ == '__main__':
    main()

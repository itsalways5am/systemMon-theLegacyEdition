###############################################################
# networkCheck.py
# last updated 1.12.2018
# purpose : checks cleaned and raw network files for discrepencies.
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
            elif line.startswith('<name>'):
                raw_dict['name'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<active>'):
                raw_dict['active'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<duplex>'):
                raw_dict['duplex'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<mtu>'):
                raw_dict['mtu'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<incomingBytes>'):
                raw_dict['incomingBytes'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<incomingPackets>'):
                raw_dict['incomingPackets'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<incomingErrors>'):
                raw_dict['incomingErrors'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<incomingDrops>'):
                raw_dict['incomingDrops'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<outgoingBytes>'):
                raw_dict['outgoingBytes'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<outgoingPackets>'):
                raw_dict['outgoingPackets'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<outgoingErrors>'):
                raw_dict['outgoingErrors'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<outgoingDrops>'):
                raw_dict['outgoingDrops'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<IPv4>'):
                raw_dict['IPv4'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<IPv4_Netmask>'):
                raw_dict['IPv4_Netmask'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<IPv4_broadcast>'):
                raw_dict['IPv4_broadcast'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<IPv6_p2p>'):
                raw_dict['IPv6_p2p'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<IPv6>'):
                raw_dict['IPv6'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<IPv4_netmask>'):
                raw_dict['IPv4_broadcast'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<IPv6_broadcast>'):
                raw_dict['IPv6_broadcast'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags

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
        discrepencies += compare_block("Interface name", "name", col_dict, raw_dict)
        discrepencies += compare_block("Activity detected", "active", col_dict, raw_dict)
        discrepencies += compare_block("Speed", "speed", col_dict, raw_dict)
        discrepencies += compare_block("Duplex info", "duplex", col_dict, raw_dict)
        discrepencies += compare_block("MTU", "mtu", col_dict, raw_dict)
        discrepencies += compare_block("Incoming Bytes", "incomingBytes", col_dict, raw_dict)
        discrepencies += compare_block("Incoming Packets", "incomingPackets", col_dict, raw_dict)
        discrepencies += compare_block("Incoming Errors", "incomingErrors", col_dict, raw_dict)
        discrepencies += compare_block("Incoming Drops", "incomingDrops", col_dict, raw_dict)
        discrepencies += compare_block("Outgoing Bytes", "outgoingBytes", col_dict, raw_dict)
        discrepencies += compare_block("Outgoing Packets", "outgoingPackets", col_dict, raw_dict)
        discrepencies += compare_block("Outgoing Errors", "outgoingErrors", col_dict, raw_dict)
        discrepencies += compare_block("Outgoing Drops", "outgoingDrops", col_dict, raw_dict)
        discrepencies += compare_block("IPv4", "IPv4", col_dict, raw_dict)
        discrepencies += compare_block("IPv4 Netmask", "IPv4_Netmask", col_dict, raw_dict)
        discrepencies += compare_block("IPv4 Broadcast", "IPv4_broadcast", col_dict, raw_dict)
        discrepencies += compare_block("IPv4 p2p", "IPv6_p2p", col_dict, raw_dict)
        discrepencies += compare_block("IPv6", "IPv6", col_dict, raw_dict)
        discrepencies += compare_block("IPv4 netmask", "IPv4_netmask", col_dict, raw_dict)
        discrepencies += compare_block("IPv6 Broadcast", "IPv6_broadcast", col_dict, raw_dict)
        # MAC address is missing... from the network Logs cleaner....

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
            if logFile == 'networkInterfaces.log':
                print('Running networkLog check for date: ' + subDir)
                raw_dict = get_battery_data(str(os.getcwd()) + '/networkInterfaces.log', raw_dict)

        os.chdir('../')

    print(raw_dict)
    print()
    return compare_data(col_dict, raw_dict)


if __name__ == '__main__':
    main()

import processesCheck
import batteryCheck
import bootCheck
import networkCheck
import diskCheck


def main():
    processes_discrepencies = processesCheck.main('../../data/processesLogs.xlsx', '../../logs')  # Parameters: cleaned path, log path
    battery_discrepencies = batteryCheck.main('../data/batteryLogs.xlsx', '../logs')
    # boot_discrepencies = bootCheck.main('../data/bootTimeLogs.xlsx', '../logs')
    network_discrepencies = networkCheck.main('../data/networkLogs.xlsx', '../logs')
    # disk_discrepencies = diskCheck.main('../data/diskLogs.xlsx', '../logs')

    # display_discrepancies(processes_discrepencies, "Processes")
    # display_discrepancies(battery_discrepencies, "Battery")
    # display_discrepancies(boot_discrepencies, "Boot Time")
    display_discrepancies(network_discrepencies, "Network")
    # display_discrepancies(disk_discrepencies, "Disk")


def display_discrepancies(type_discrepencies, type_name):
    print("\n", str(type_name), " Discrepencies:", sep="")
    if len(type_discrepencies) == 0:
        print("NONE")
    else:
        for discrepancy in type_discrepencies:
            print(discrepancy)  # COMMENT OUT, if you do not want to see the discrepancies
        print("\n", len(type_discrepencies), " discrepancies found in ", type_name, sep="")


if __name__ == '__main__':
    main()

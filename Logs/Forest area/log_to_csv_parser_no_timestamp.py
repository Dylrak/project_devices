import os, re, csv
from datetime import datetime, timedelta
# This file parses the .log files as they were created using the logging version of the firmware and extraPutty
# into clear-cut CSV-files containing all valid entries. Any entry with incorrect syntax is ignored.
# This version is made specifically for the forest area; the computer which we used to log this didn't have timestamping
# enabled and so we take the time on line 1 and add 150 ms for each entry.
if __name__ == '__main__':
    # valid line example: 13:04:14:543, -43,11
    valid_line_regex = re.compile("(-?\d{2,3}),\s*(-?\d{1,2})")
    timeout_line_regex = re.compile("Timeout\/error! No packet received\.")
    timestamp_regex = re.compile("(\d{2}:\d{2}:\d{2})")
    timestamp = ''
    for file in os.listdir(os.getcwd()):
        if file.endswith(".log"):
            new_filename = file.replace(".log", "") + "_signal" + ".csv"
            print("Saving", file, "as", new_filename + "...")
            timestamped_signal_values = []
            with open(file, 'r') as log_file:
                # Because these files contain no timestamp, we will add one through the time posted at the top of the file
                # plus 150ms per entry (the interval between pings as is default in the firmware):
                regex_obj = re.search(timestamp_regex, log_file.readline())
                if regex_obj:
                    timestamp = datetime.strptime(regex_obj.group(1), '%H:%M:%S')
                for line in log_file:
                    regex_obj = re.match(valid_line_regex, line)
                    if regex_obj:
                        timestamped_signal_values.append([timestamp.strftime('%H:%M:%S:%f')[:-3], regex_obj.group(1), regex_obj.group(2)])
                        print([timestamp.strftime('%H:%M:%S:%f')[:-3], regex_obj.group(1), regex_obj.group(2)])
                        timestamp = timestamp + timedelta(milliseconds=150)  # Add 150ms to timestamp
                    else:
                        regex_obj = re.match(timeout_line_regex, line)
                        if regex_obj:
                            timestamped_signal_values.append([timestamp.strftime('%H:%M:%S:%f')[:-3], "null"])
                            print([timestamp.strftime('%H:%M:%S:%f')[:-3], "null"])
                            timestamp = timestamp + timedelta(milliseconds=150)
            with open(new_filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                for signal_value in timestamped_signal_values:
                    csv_writer.writerow(signal_value)

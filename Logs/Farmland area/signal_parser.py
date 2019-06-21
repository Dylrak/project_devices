import os, re, csv
# This file parses the .log files as they were created using the logging version of the firmware and extraPutty
# into clear-cut CSV-files containing all valid entries. Any entry with a timeout or incorrect syntax is ignored.
if __name__ == '__main__':
    # valid line example: 13:04:14:543, -43,11
    valid_line_regex = re.compile("(\d{2}:\d{2}:\d{2}:\d{3}),\s*(-?\d{2,3}),\s*(-?\d{1,2})")
    timeout_line_regex = re.compile("(\d{2}:\d{2}:\d{2}:\d{3}), Timeout\/error! No packet received\.")
    for file in os.listdir(os.getcwd()):
        if file.endswith(".log"):
            new_filename = file.replace(".log", "") + "_signal" + ".csv"
            print("Saving", file, "as", new_filename + "...")
            timestamped_signal_values = []
            with open(file, 'r') as log_file:
                for line in log_file:
                    regex_obj = re.match(valid_line_regex, line)
                    if regex_obj:
                        timestamped_signal_values.append([regex_obj.group(1), regex_obj.group(2), regex_obj.group(3)])
                        print([regex_obj.group(1), regex_obj.group(2), regex_obj.group(3)])
            with open(new_filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                for signal_value in timestamped_signal_values:
                    csv_writer.writerow(signal_value)

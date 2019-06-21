import os, re, csv
from datetime import datetime, timedelta

def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, '%H:%M:%S:%f')

if __name__ == '__main__':
    for file in os.listdir(os.getcwd()):

        # Only loop through _distance files
        if not file.endswith("_distance.csv"):
            continue

        print(file)
        filename = file.replace("_distance.csv", "")

        super_cool_list = []
        # Loop through signal file
        with open(filename + "_signal.csv", 'r') as csv_file_signal:
            csv_read_signal = csv.reader(csv_file_signal, delimiter=',')

            for signal_row in csv_read_signal:
                signal_timestamp = parse_timestamp(signal_row[0])
                signal_rssi = signal_row[1]
                signal_snr = signal_row[2]

                # Compare timestamp with _distance file get timestamp between before and after timestamp
                with open(filename + "_distance.csv", 'r') as csv_file_distance:
                    csv_read_distance = csv.reader(csv_file_distance, delimiter=',')

                    # this is the previous row [timstamp,distance in meters]
                    prev_distance_row = None
                    for row in csv_read_distance:
                        if prev_distance_row is None:
                            prev_distance_row = row
                            continue

                        distance_timestamp = parse_timestamp(row[0])
                        prev_distance_timestamp = parse_timestamp(prev_distance_row[0])

                        if signal_timestamp < distance_timestamp and signal_timestamp > prev_distance_timestamp:
                            # calculate the meters based on previous data
                            d_gps_time =  distance_timestamp.timestamp() - prev_distance_timestamp.timestamp()
                            d_rssi_time = signal_timestamp.timestamp() - prev_distance_timestamp.timestamp()
                            ratio = d_rssi_time / d_gps_time
                            i_distance = ratio * float(row[1]) + (1 - ratio) * float(prev_distance_row[1])
                            i_distance = round(i_distance, 2)

                            super_cool_list.append([signal_timestamp.strftime('%H:%M:%S:%f')[:-3], i_distance, signal_rssi, signal_snr])

                        prev_distance_row = row

        # create csv from list
        with open(filename + "_goodshit.csv", 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(super_cool_list)

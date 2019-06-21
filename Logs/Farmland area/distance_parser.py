import os, re, csv
import math

from datetime import datetime, timedelta

# This file parses the .log files as they were created using the logging version of the firmware and extraPutty
# into clear-cut CSV-files containing all valid entries. Any entry with a timeout or incorrect syntax is ignored.

def convert_to_distance(origin_latitude, origin_longitude, latitude, longitude):
    """
    Calculate the Haversine distance.

    Returns
    -------
    distance_in_m : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    radius = 6371  # km

    dlat = math.radians(latitude - origin_latitude)
    dlon = math.radians(longitude - origin_longitude)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(origin_latitude)) * math.cos(math.radians(latitude)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return round(d * 1000, 2)


def parse_timestamp(timestamp):
    print(timestamp.split("T",1))
    time = timestamp.split("T",1)[1] # remove the date
    time_with_points = time.replace(".", ":")
    time_return = time_with_points.replace("Z", "")
    return time_return


def addtime(timestamp):
    timestamp_obj = datetime.strptime(timestamp, '%H:%M:%S:%f')
    timestamp_added_hours = timestamp_obj + timedelta(hours=2)
    return timestamp_added_hours.strftime('%H:%M:%S:%f')[:-3]


if __name__ == '__main__':
    for file in os.listdir(os.getcwd()):
        if not file.endswith(".csv"):
            continue

        if file.endswith("_signal.csv"):
            continue

        if file.endswith("_distance.csv"):
            continue

        if file.endswith("_goodshit.csv"):
            continue

        new_csv_data = []
        origin_lat = None
        origin_long = None

        print(file)

        with open(file, 'r') as csv_file:
            csv_read = csv.reader(csv_file, delimiter=',')
            next(csv_read, None) #Skip header row

            for row in csv_read:
                timestamp = addtime(parse_timestamp(row[0]))
                latitude = float(row[1])
                longitude = float(row[2])

                if origin_lat == None:
                    origin_lat = latitude
                    origin_long = longitude
                    new_csv_data.append([timestamp, 0])
                    continue

                distance = convert_to_distance(origin_lat,origin_long,latitude,longitude)

                new_csv_data.append([timestamp, distance])

        new_filename = file.replace(".csv", "") + "_distance" + ".csv"
        with open(new_filename, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(new_csv_data)

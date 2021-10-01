import csv

csv_data = csv.reader(open(FILE_PATH + ".csv"))
open_time_min = min(csv_data)[0]

csv_data = csv.reader(open(FILE_PATH + ".csv"))
open_time_max = max(csv_data)[0]

csv_data = csv.reader(open(FILE_PATH + ".csv"))
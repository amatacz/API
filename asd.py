import csv
import json

data = json.load(open("circuits.json"))
useful_columns = ["season", "circuitId", "circuitName"]
default_value = ""

with open("circuits.csv", mode="w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=useful_columns)
    writer.writeheader()


    # for obj in data:
    #     row = {}
    #     for column in useful_columns:
    #         if column in obj.keys():
    #             row[column] = obj[column]
    #         else:
    #             row[column] = default_value
    #     writer.writerow(row)
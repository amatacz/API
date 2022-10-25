import os

import requests
import pandas as pd
import json
import csv
from pathlib import Path

# JAK OGARNĄĆ WSZYSTKIE WYNIKI - API JEST PODZIELONE NA STRONY - JAK DODAŁAM ?limit=1000.json DO FORMATKI REQUEST NIE PRZESZŁO


endpoints = ['circuits', 'drivers', 'constructors', 'races', 'results']
#endpoints = ['races']

seasons = list(range(2000, 2023))


def api():
    for endpoint in endpoints:
        responses = {}
        for season in seasons:
            response = requests.get('https://ergast.com/api/f1/{season}/{endpoint}.json?limit=1000'.format(season=season, endpoint=endpoint), verify=False)
            responses[season] = response.json()

        with open('{endpoint}.json'.format(endpoint=endpoint), 'w', encoding="utf-8") as f:
            json.dump(responses, f, indent=2)


def circuits_csv_loader():
    data = json.load(open("circuits.json"))

    useful_columns = ["season", "circuitId", "circuitName"]
    default_value = ""

    with open("circuits.csv", mode="w", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=useful_columns)
        writer.writeheader()

        for obj in data.values():
            for season in seasons:
                row = {}
                for i in range(0, len(obj['MRData']['CircuitTable']['Circuits'])):
                    row["season"] = season
                    row["circuitId"] = obj['MRData']['CircuitTable']['Circuits'][i]["circuitId"]
                    row["circuitName"] = obj['MRData']['CircuitTable']['Circuits'][i]["circuitName"]

                    writer.writerow(row)


def constructors_csv_loader():
    data = json.load(open("constructors.json"))

    useful_columns = ["season", "constructorId", "name", "nationality"]
    default_value = ""

    with open("constructors.csv", mode="w", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=useful_columns)
        writer.writeheader()

        for obj in data.values():
            for season in seasons:
                row = {}
                for i in range(0, len(obj['MRData']['ConstructorTable']['Constructors'])):
                    row["season"] = season
                    row["constructorId"] = obj['MRData']['ConstructorTable']['Constructors'][i]["constructorId"]
                    row["name"] = obj['MRData']['ConstructorTable']['Constructors'][i]["name"]
                    row["nationality"] = obj['MRData']['ConstructorTable']['Constructors'][i]["nationality"]

                    writer.writerow(row)


def drivers_csv_loader():
    data = json.load(open("drivers.json"))

    useful_columns = ["season", "driverId", "givenName", "familyName", "nationality"]
    default_value = ""

    with open("drivers.csv", mode="w", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=useful_columns)
        writer.writeheader()

        for obj in data.values():
            for season in seasons:
                row = {}
                for i in range(0, len(obj['MRData']['DriverTable']['Drivers'])):
                    row["season"] = season
                    row["driverId"] = obj['MRData']['DriverTable']['Drivers'][i]["driverId"]
                    row["givenName"] = obj['MRData']['DriverTable']['Drivers'][i]["givenName"]
                    row["familyName"] = obj['MRData']['DriverTable']['Drivers'][i]["familyName"]
                    row["nationality"] = obj['MRData']['DriverTable']['Drivers'][i]["nationality"]

                    writer.writerow(row)


def races_csv_loader():
    data = json.load(open("races.json"))
    useful_columns = ['raceId', 'year', 'name', 'round']

    with open("races.csv", mode="w", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=useful_columns)
        writer.writeheader()

        for obj in data.values():
            for season in seasons:
                row = {}
                for i in range(0, len(obj['MRData']['RaceTable']['Races'])):
                    row["raceId"] = obj['MRData']['RaceTable']['Races'][i]["round"]+str(season)
                    row["year"] = season
                    row["round"] = obj['MRData']['RaceTable']['Races'][i]["round"]
                    row["name"] = obj['MRData']['RaceTable']['Races'][i]["raceName"]

                    writer.writerow(row)

# tu mi nie działa
def results_csv_loader():
    data = json.load(open("results.json"))
    useful_columns = ["resultId", "raceId","driverId","constructorId","number","grid","position","positionText","positionOrder","points","laps","time","milliseconds","fastestLap","rank","fastestLapTime","fastestLapSpeed","statusId"]

    with open("results.csv", mode="w", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=useful_columns)
        writer.writeheader()

        for obj in data.values():
            for season in seasons:
                row = {}
                j = 1
                for z in range(0, len(obj['MRData']['RaceTable']['Races'])):
                    for i in range(0, len(obj['MRData']['RaceTable']['Races'])):
                        row["resultId"] = j
                        j += 1
                        row["raceId"] = obj['MRData']['RaceTable']['Races'][i]["round"]+str(season)
                        row["driverId"] = obj["MRData"]["RaceTable"]['Races'][z]['Results'][i]['Driver']['driverId']
                        # row["constructorId"] = obj["MRData"]["RaceTable"]["Results"]["Constructor"]["constructorId"]
                        # row["driverId"] = obj["MRData"]["RaceTable"]["Results"]["number"]
                        # row["driverId"] = obj["MRData"]["RaceTable"]["Results"]["grid"]
                        # row["driverId"] = obj["MRData"]["RaceTable"]["Results"]["position"]



                    writer.writerow(row)
                    #print(len(obj['MRData']['RaceTable']['Races']))





#api()

results_csv_loader()

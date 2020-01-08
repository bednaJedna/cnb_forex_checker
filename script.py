import argparse
import json
import re
from os.path import isfile

from requests import get

URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={DAY}.{MONTH}.{YEAR}"


def convert_to_json_structure(raw_day_data: str):
    dataobject = {}
    datalist = raw_day_data.splitlines()
    datekey = parse_date(datalist[0])
    headerkeys = datalist[1].split(sep="|")[1:]
    datalists = [row.split(sep="|") for row in datalist[2:]]

    dataobject[datekey] = {}

    for row in datalists:
        dataobject[datekey][row[0]] = {}
        for i, item in enumerate(row[1:]):
            dataobject[datekey][row[0]][headerkeys[i]] = item

    return dataobject


def add_data_to_json(loaded_data: dict, new_data: dict):

    ldatakeys = list(loaded_data.keys())
    ndatakey = list(new_data.keys())[0]

    if ndatakey in ldatakeys:
        return loaded_data

    else:
        loaded_data[ndatakey] = new_data[ndatakey]
        return loaded_data


def save_as_json(data: dict):
    with open("data.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def open_json():
    if not isfile("data.json"):
        with open("data.json", mode="w") as f:
            json.dump({}, f)

    with open("data.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_date():
    parser = argparse.ArgumentParser(description="Parse date.")
    parser.add_argument("day", action="store", type=str, help="day in format 'dd'.")
    parser.add_argument("month", action="store", type=str, help="month in format 'mm'.")
    parser.add_argument("year", action="store", type=str, help="year in format 'yyyy'.")
    args = parser.parse_args()
    return args


def get_raw(link: str):
    return get(link).text


def parse_date(firstline: str):
    regex = re.compile(r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}")
    return re.findall(regex, firstline)[0]


def insert_dates(link: str, day: str, month: str, year: str):
    return link.replace("{DAY}", day).replace("{MONTH}", month).replace("{YEAR}", year)


def main():
    raw = get_raw(insert_dates(URL, args.day, args.month, args.year))
    new_data = convert_to_json_structure(raw)
    loaded_data = open_json()
    updated_data = add_data_to_json(loaded_data, new_data)
    save_as_json(updated_data)


if __name__ == "__main__":
    args = get_date()

    if args.day and args.month and args.year:
        main()

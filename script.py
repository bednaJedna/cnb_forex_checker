import argparse
import json
import re
from datetime import datetime, timedelta
from os.path import isfile
from random import randrange
from time import sleep

from requests import get
from tqdm import trange

URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={DATE}"


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
    parser.add_argument(
        "start_date", action="store", type=str, help="date in format 'dd.mm.yyyy'."
    )
    parser.add_argument(
        "end_date", action="store", type=str, help="date in format 'dd.mm.yyyy'."
    )
    args = parser.parse_args()
    return args


# see https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
def get_timedelta(end_date: str, start_date: str):
    edate = datetime.strptime(end_date, "%d.%m.%Y")
    sdate = datetime.strptime(start_date, "%d.%m.%Y")
    diff = edate - sdate
    return diff.days


def update_date(old_date: str):
    odate = datetime.strptime(old_date, "%d.%m.%Y")
    tdelta = timedelta(days=1)
    ndate = odate + tdelta
    return ndate.strftime("%d.%m.%Y")


def get_raw(link: str):
    return get(link).text


def parse_date(firstline: str):
    regex = re.compile(r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}")
    return re.findall(regex, firstline)[0]


def insert_date(link: str, date: str):
    return link.replace("{DATE}", date)


def just_chill(min: int, max: int, step: int):
    sleep(randrange(min, max, step))


def main():
    args = get_date()

    if args.start_date and args.end_date:
        days = get_timedelta(args.end_date, args.start_date) + 1
        day = args.start_date

        for i in trange(days, desc="Grabbing FXs", unit="day"):
            if i > 0:
                day = update_date(day)
            raw = get_raw(insert_date(URL, day))
            new_data = convert_to_json_structure(raw)
            loaded_data = open_json()
            updated_data = add_data_to_json(loaded_data, new_data)
            save_as_json(updated_data)
            just_chill(3, 6, 1)


if __name__ == "__main__":
    main()

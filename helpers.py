import json
from datetime import datetime as dt
from datetime import timedelta
from pprint import PrettyPrinter

from hamcrest import assert_that, is_in


def load_data(filepath: str):
    with open(filepath, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def convert_to_datetime(date_: str):
    return dt.strptime(date_, "%d.%m.%Y")


def find_nearest_date(date_: str, dates: list, downwards: bool):

    if date_ not in dates:
        date_ = dt.strptime(date_, "%d.%m.%Y")

        if not downwards:
            date_ = date_ + timedelta(days=1)
        else:
            date_ = date_ - timedelta(days=1)

        date_ = date_.strftime("%d.%m.%Y")

        return find_nearest_date(date_, dates, downwards)
    else:
        return date_


def get(data: object, country: str, from_: str, to: str):
    # debug
    # p = PrettyPrinter(indent=2)
    output = {}
    dates = list(data.keys())
    # tries to find nearest valid date with data upwards
    from_ = find_nearest_date(from_, dates, False)
    # tries to find nearest valid date with data downwards
    to = find_nearest_date(to, dates, True)
    countries = list(data[from_].keys())
    assert_that(country, is_in(countries))

    d_from = convert_to_datetime(from_)
    d_to = convert_to_datetime(to)

    for date, cdata in list(data.items()):
        if (convert_to_datetime(date) < d_from) or (convert_to_datetime(date) > d_to):
            continue
        else:
            if country not in output:
                output[country] = {}

            if date not in output[country]:
                output[country][date] = {}
                output[country][date] = cdata[country]
    # debug
    # p.pprint(output)
    return output


if __name__ == "__main__":
    data = load_data("./data.json")
    result = get(data, "EMU", "01.12.2019", "31.01.2020")

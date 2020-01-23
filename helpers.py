import json
from datetime import datetime as dt
from pprint import PrettyPrinter

from hamcrest import assert_that, is_in


def load_data(filepath: str):
    with open(filepath, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def convert_to_datetime(date_: str):
    return dt.strptime(date_, "%d.%m.%Y")


def get(data: object, country: str, from_: str, to: str):
    # debug
    p = PrettyPrinter(indent=2)
    output = {}
    dates = list(data.keys())
    assert_that(from_, is_in(dates))
    assert_that(to, is_in(dates))
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
    p.pprint(output)
    return output


if __name__ == "__main__":
    data = load_data("./data.json")
    result = get(data, "EMU", "02.01.2020", "22.01.2020")

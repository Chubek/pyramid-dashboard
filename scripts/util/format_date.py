from dotenv import dotenv_values
from datetime import date, datetime

temp = dotenv_values(".env")


def format_date(date):
    year = date.year
    month = date.month
    day = date.day

    rep = temp['DATE_PATTERN']

    rep = rep.replace("YY", year)
    rep = rep.replace("DD", day)
    rep = rep.replace("MM", month)

    return rep


def return_date(date_str):
    splet = date_str.split("/")
    return datetime.date(splet[2], splet[0], splet[1])

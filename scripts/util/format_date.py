from dotenv import dotenv_values
import string 

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

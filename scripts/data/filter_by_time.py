import pandas as pd
import datetime
from scripts.util.format_date import format_date
from dotenv import dotenv_values
from scripts.util.get_days import get_days
from dateutil import parser

temp = dotenv_values(".env")



def filter_daily(df, day_start, num_days):
    #day_start = parser.parse(day_start)

    day_end = day_start + datetime.timedelta(days=num_days)

    ts_start = pd.Timestamp(day_start)
    ts_end = pd.Timestamp(day_end)

    return df[(df[temp['DATE_TIME_COLUMN']] > ts_start) & (df[temp['DATE_TIME_COLUMN']] <= ts_end)]

def filter_weekly(df, week_start, num_weeks):
    week_start = parser.parse(week_start)


    print(week_start, "week_start")

    week_end = week_start + datetime.timedelta(days=7 * num_weeks)

    ts_start = pd.Timestamp(week_start)
    ts_end = pd.Timestamp(week_end)

    return df[(df[temp['DATE_TIME_COLUMN']] > ts_start) & (df[temp['DATE_TIME_COLUMN']] <= ts_end)]


def filter_monthly(df, day_start, num_months):
    day_start = parser.parse(day_start)

    day_end = day_start + datetime.timedelta(days=get_days(day_start) * num_months)

    ts_start = pd.Timestamp(day_start)
    ts_end = pd.Timestamp(day_end)

    return df[(df[temp['DATE_TIME_COLUMN']] > ts_start) & (df[temp['DATE_TIME_COLUMN']] <= ts_end)]
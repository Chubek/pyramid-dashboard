import pandas as pd
import datetime
from scripts.util.format_date import format_date
from dotenv import dotenv_values
from scripts.util.get_days import get_days

temp = dotenv_values(".env")



def filter_daily(df, day_date):
    if day_date == "today":
        dt = datetime.datetime.now()

    ts = pd.Timestamp(format_date(dt))

    return df[df[temp['DATE_TIME_COLUMN']] == ts]

def filter_weekly(df, week_start):
    week_end = week_start + datetime.timedelta(days=7)

    ts_start = pd.Timestamp(format_date(week_start))
    ts_end = pd.Timestamp(format_date(week_end))

    return df[(df[temp['DATE_TIME_COLUMN']] > ts_start) & (df[temp['DATE_TIME_COLUMN']] <= ts_end)]


def filter_monthly(df, day_start):
    day_end = day_start + datetime.timedelta(days=get_days(day_start))

    ts_start = pd.Timestamp(format_date(day_start))
    ts_end = pd.Timestamp(format_date(day_end))

    return df[(df[temp['DATE_TIME_COLUMN']] > ts_start) & (df[temp['DATE_TIME_COLUMN']] <= ts_end)]
import pandas as pd
from dotenv import dotenv_values

temp = dotenv_values(".env")

def to_datetime(x):
    try:
        return pd.Timestamp(x)
    except:
        return pd.Timestamp(temp['FALLBACK_DATE'])
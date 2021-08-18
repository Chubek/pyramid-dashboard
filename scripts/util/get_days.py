import datetime

def is_leap(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def get_days(date):
    month_name = date.strftime("%B")

    if month_name in ["January", "March", "May", "July", "August", "October", "December"]:
        day = 30
    elif month_name == "February":
        if is_leap(date.year):
            day = 28
        else:
            day = 29
    else:
        return 31

    return day



import time
import datetime
from datetime import date
from datetime import timedelta


def get_date_int(today_str):
    """Returns 'int' tuple, where index value [0] represents year, [1] - month, [2] - day.
     Must be given 'str' argument, formatted as 'yyyy-mm-dd' (e.g. '2023-01-03')."""

    year = int(today_str[0:4])
    month = int(today_str[5:7])
    day = int(today_str[8:10])

    return year, month, day


def get_weekday(today_str):
    """Checks which day of the week is the day given.
    Must be given 'str' argument, formatted as 'yyyy-mm-dd' (e.g. '2023-01-03')."""

    year = int(today_str[0:4])
    month = int(today_str[5:7])
    day = int(today_str[8:10])

    if date(year, month, day).weekday() == 0:
        return 'Monday'

    elif date(year, month, day).weekday() == 1:
        return 'Tuesday'

    elif date(year, month, day).weekday() == 2:
        return 'Wednesday'

    elif date(year, month, day).weekday() == 3:
        return 'Thursday'

    elif date(year, month, day).weekday() == 4:
        return 'Friday'

    elif date(year, month, day).weekday() == 5:
        return 'Saturday'

    elif date(year, month, day).weekday() == 6:
        return 'Sunday'


def make_date_readable(date_unreadable):
    """Writes time in easy-to-read type (e.g. 'January 03, 2023').
    Must be given 'str' argument, formatted as 'yyyy-mm-dd' (e.g. '2023-01-03')."""

    date_readable = datetime.datetime.strptime(date_unreadable, '%Y-%m-%d')
    date_readable = date_readable.strftime("%B %d, %Y")

    return date_readable


def add_day(date_tuple):
    yda_year = date_tuple[0]
    yda_month = date_tuple[1]
    yda_day = date_tuple[2]

    yda = date(yda_year, yda_month, yda_day)
    tda = str(yda + timedelta(days=1))

    return tda


# Initiating program start date:
start_year = 2023
start_month = 1
start_day = 1

# Using start date parameters to create 'int' and 'str' date:
first_day_int = date(start_year, start_month, start_day)
first_day_str = str(first_day_int)


# The first 'day after the first day' can`t be in the 'while' loop,
# because it uses not 'yesterday', but 'first_day' parameter:

def add_day_0(yesterday_str):
    yda_year = int(yesterday_str[0:4])
    yda_month = int(yesterday_str[5:7])
    yda_day = int(yesterday_str[8:10])

    yda = date(yda_year, yda_month, yda_day)
    tda = str(yda + timedelta(days=1))

    return tda


today = first_day_str
# today = add_day_0(first_day_str)
today_gui = make_date_readable(today)
day_name = get_weekday(today)
print(f"{today_gui}, {day_name}")

yesterday = get_date_int(today)


# After the 'yesterday' is no longer 'the_first_day', we can initiate 'while' loop:
while True:
    time.sleep(1)
    today = add_day(yesterday)
    today_gui = make_date_readable(today)

    day_name = get_weekday(today)
    yesterday = get_date_int(today)
    if day_name == 'Saturday' or day_name == 'Sunday':
        print()
        continue
    else:
        print(f"{today_gui}, {day_name}")

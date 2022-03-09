from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from datetime import date
from datetime import timedelta

import csv

outbound_departure_airport = []
outbound_arrival_airport = []
outbound_departure_time = []
outbound_arrival_time = []
inbound_departure_airport = []
inbound_arrival_airport = []
inbound_departure_time = []
inbound_arrival_time = []
total_price = []
taxes = []

cheapest_out_prices = []
cheapest_in_prices = []

out_taxes = []
in_taxes = []

# Initiating service, that will be able to manipulate with the web-page:
browser = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)
browser.get("https://www.fly540.com/")

# Creating list that contains number of days left before departure:
depart_after_days = [10, 20]

# Creating list that contains number of days of which will be returning AFTER departure:
return_after_days = [7]


def click_by_xpath(xpath: str):
    """Finds element in the web-page using XPath and selects (clicks) it."""

    selection = browser.find_element(
        By.XPATH,
        value=xpath
    )
    return selection.click()


def find_by_xpath(xpath: str):
    """Finds element in the web-page using XPath, but DOES NOT select (click) it."""

    selection = browser.find_element(
        By.XPATH,
        value=xpath
    )
    return selection


def get_days_left(days_before_flight: int):
    """Adds given number of days (as integer) to today. Returns 'day' result as integer."""

    today = date.today()
    flight_date = today + timedelta(days=days_before_flight)

    # Converts 'date' type to string, so it could manipulate with value more easily:
    flight_str = str(flight_date)

    # From 'flight_str' gets only the 'day' material and coverts it to 'int':
    flight_str_len = len(flight_str)
    flight_day = flight_str[flight_str_len - 2:]
    flight_day = int(flight_day)

    return flight_day


# TODO: In future args must not be lists, as it is right now:
def get_return_day(depart_after: list, return_after: list):
    """Counts on which day of the month return will happen. Returns 'day' result as integer."""

    today = date.today()
    flight_day = today + timedelta(days=depart_after[0])
    returning_day = flight_day + timedelta(days=return_after[0])

    # Converts 'date' type to string, so it could manipulate with value more easily:
    return_str = str(returning_day)

    # From 'flight_str' gets only the 'day' material and coverts it to 'int':
    return_str_len = len(return_str)
    return_day = return_str[return_str_len - 2:]
    return_day = int(return_day)

    return return_day


def get_return_after(depart_after: int, return_after: int):
    """Adds given number of days ('return_after') to 'depart_after' argument.
    Returns number (as integer) of days left before returning."""

    return_after = depart_after + return_after
    return return_after


def get_month_left():
    """Finds day picker table and gets <a> </a> lines, which contains all remaining days in the month.
    Return list of all days in the month remaining."""

    days_left = browser.find_elements(
        By.XPATH,
        value='//table//a'
    )
    return days_left


# TODO: Combine with 'get_return_month' function:
def get_correct_month(flight_after: int, month_days_left: int, xpath: str):
    """Checks if flight day will be in the current month by subtracting left days in the month ('month_days_left' arg)
    from days left before flight ('flight_after' arg).

    If there are not enough days left in the month, program will:
     - change the month by using 'xpath' argument;
     - return new 'flight_after' value as integer."""

    if flight_after > month_days_left:
        # Changes the month:
        selection = browser.find_element(
            By.XPATH,
            value=xpath
        )
        selection.click()

        # Changes and return new 'flight_after' value as integer:
        flight_after = flight_after - month_left
        return flight_after


# TODO: Combine with 'get_correct_month' function:
def get_return_month(depart_day, return_after, xpath: str):
    """Only used in web-page 'Return' calendar / date-picker.

    Function:
     - Automatically changes the month to the next one (!!!);
     - Updates 'return_after' parameter;
     - Returns updated 'return_after' parameter."""

    # Gets all the days left in the month selected:
    mnt_left = browser.find_elements(
        By.XPATH,
        value='//table//a'
    )

    # Gets how many days are left in the month after departure day:
    mth_left_aft_depart = len(mnt_left) - int(depart_day)

    # Changes the month:
    selection = browser.find_element(
        By.XPATH,
        value=xpath
    )
    selection.click()

    # Updates 'return_after_days' parameter:
    days_before_return = return_after - mth_left_aft_depart

    return days_before_return


def select_depart_day(date_list: list, dep_day: int):
    """Selects the day in the web-page calendar / date-picker.
    Only works will when the month is already correct."""

    for i in date_list:
        day = i.text
        day = int(day)
        if day == dep_day:
            i.click()
            break


def get_iata(list_given: list, xpath: str):
    """Finds full flight airport data the web-page by using xpath. Returns only IATA as string."""

    airport = browser.find_element(
        By.XPATH,
        value=xpath
    )

    airport = airport.text
    iata = airport[-4:-1]

    # Adds IATA to the list given:
    list_given.append(iata)

    return list_given


def get_flight_time(
        list_given: list,
        hours_xpath: str,
        date_xpath: str,
        dep_aft_x_days
):
    """Returns list of added string of full departure time."""

    def extract_data(xpath):
        """Extracts data from the web-page by using xpath.
        Makes it readable. Returns result as string."""

        etr_data = browser.find_element(
            By.XPATH,
            value=xpath
        )
        etr_data = etr_data.text
        return etr_data

    # Getting departure hour and date,
    # as well as getting rid of commas (','), so it would not confuse the .csv file:
    dep_hour = extract_data(hours_xpath)
    dep_date = extract_data(date_xpath)
    dep_date = dep_date.replace(",", "")

    # Gets departure year:
    today = date.today()
    year = today + timedelta(days=dep_aft_x_days)
    year = year.strftime("%Y")

    # Creates string that contains all the needed information and adds it to the 'list_given':
    full_dep_date = dep_date + ' ' + year + ' ' + dep_hour + ' local time'
    list_given.append(full_dep_date)

    return list_given


def get_info_box_xpath(dep_xpath, ret_xpath, rnd_trips: list):
    """By using the departure / return tables XPath ('dep_xpath' and 'ret_xpath' arguments),
    and number of round trips ('rnd_trips: list' argument), creates full XPath of each info-box.
    Returns list, where the XPath values are strings."""

    xpath_list = []
    xpath_given = [dep_xpath, ret_xpath]

    for xpath in xpath_given:
        for rnd_trip in rnd_trips:
            div = "div[" + str(rnd_trip) + "]"
            xpath_created = xpath + div + "/"
            xpath_list.append(xpath_created)

    return xpath_list


# TODO: Need to be merged with 'get_inbound_lists' in future:
# TODO: Functions used must be in-house, not from 'out-side' in future:
def get_outbound_lists(out_box_xpath, rnd_trips):
    """Fills outbound lists with the necessary information.

    Adds information to the list mentioned:
     - 'outbound_departure_airport';
     - 'outbound_arrival_airport';
     - 'outbound_departure_time';
     - 'outbound_arrival_time';
     - 'cheapest_out_prices'."""

    for rnd_trip in rnd_trips:
        div = "div[" + str(rnd_trip) + "]"
        box_xpath = out_box_xpath + div + "/"

        # Gets and adds value to 'outbound_departure_time' list:
        get_flight_time(
            outbound_departure_time,
            box_xpath + 'table/tbody/tr/td[1]/span[3]',
            box_xpath + 'table/tbody/tr/td[1]/span[4]',
            depart_after_days[0]
        )

        # Gets and adds value to 'outbound_departure_airport' list:
        get_iata(
            outbound_departure_airport,
            box_xpath + 'table/tbody/tr/td[1]/span[5]'
        )

        # Gets and adds value to 'outbound_arrival_time' list:
        get_flight_time(
            outbound_arrival_time,
            box_xpath + 'table/tbody/tr/td[3]/span[2]',
            box_xpath + 'table/tbody/tr/td[3]/span[3]',
            depart_after_days[0]
        )

        # Gets and adds value to 'outbound_arrival_airport' list:
        get_iata(
            outbound_arrival_airport,
            box_xpath + 'table/tbody/tr/td[3]/span[4]'
        )

        # Gets the cheapest outbound price:
        cheapest_out_price = browser.find_element(
            By.XPATH,
            value=(box_xpath + 'table/tbody/tr/td[4]/span[2]')
        )

        cheapest_out_price = cheapest_out_price.text
        cheapest_out_price = int(cheapest_out_price)
        cheapest_out_prices.append(cheapest_out_price)

        # Opens 'See More' graph in order to take the highest price parameter:
        click_by_xpath(str(box_xpath + 'table/tbody/tr/td[1]/span[3]'))

        # TODO: Does not work properly, because of "ValueError: invalid literal for int() with base 10: ''".
        #  Must be mentioned, that error is not stable (that means sometimes it comes, sometimes - not).
        #  Must be fixed in future:

        # # Getting the highest price <div> parameter:
        # depart_box_root = "/html/body/div[1]/div/section/div[3]/form/div[1]"
        #
        # for rnd_trip in rnd_trips:
        #
        #     # Opens 'See More' graph in order to take the highest price parameter:
        #     click_by_xpath(str(depart_box_root) + str(box_xpath) + 'table/tbody/tr/td[1]/span[3]')
        #
        #     price_div = str(depart_box_root) + "/div[2]/div[" + str(rnd_trip) + "]/div/div/div[3]/div/div[2]/span"
        #
        #     # Using now-created 'price_div' parameter to extract the highest price:
        #     high_price = find_by_xpath(price_div)
        #     high_price = high_price.text
        #
        #     # Getting rid of currency letters (USD or KES), and leaving only integers:
        #     high_price = high_price[4:]
        #     high_price = int(high_price)
        #
        #     # Getting 'one way' (not full) taxes:
        #     taxes = high_price - cheapest_out_price
        #     out_taxes.append(high_price)


# TODO: Need to be merged with 'get_outbound_lists' in future:
# TODO: Functions used must be in-house, not from 'out-side' in future:
def get_inbound_lists(in_box_xpath, rnd_trips):
    """Fills inbound lists with the necessary information.

    Adds information to the list mentioned:
     - 'inbound_departure_airport';
     - 'inbound_arrival_airport';
     - 'inbound_departure_time';
     - 'inbound_arrival_time';
     - 'cheapest_in_prices'."""

    for rnd_trip in rnd_trips:
        div = "div[" + str(rnd_trip) + "]"
        box_xpath = in_box_xpath + div + "/"

        # Gets and adds value to 'outbound_departure_time' list:
        get_flight_time(
            inbound_departure_time,
            box_xpath + 'table/tbody/tr/td[1]/span[3]',
            box_xpath + 'table/tbody/tr/td[1]/span[4]',
            depart_after_days[0]
        )

        # Gets and adds value to 'outbound_departure_airport' list:
        get_iata(
            inbound_departure_airport,
            box_xpath + 'table/tbody/tr/td[1]/span[5]'
        )

        # Gets and adds value to 'outbound_arrival_time' list:
        get_flight_time(
            inbound_arrival_time,
            box_xpath + 'table/tbody/tr/td[3]/span[2]',
            box_xpath + 'table/tbody/tr/td[3]/span[3]',
            depart_after_days[0]
        )

        # Gets and adds value to 'outbound_arrival_airport' list:
        get_iata(
            inbound_arrival_airport,
            box_xpath + 'table/tbody/tr/td[3]/span[4]'
        )

        # Gets the cheapest inbound price:
        cheapest_in_price = browser.find_element(
            By.XPATH,
            value=(box_xpath + 'table/tbody/tr/td[4]/span[2]')
        )

        cheapest_in_price = cheapest_in_price.text
        cheapest_in_price = int(cheapest_in_price)
        cheapest_in_prices.append(cheapest_in_price)

        # Opens 'See More' graph in order to take the highest price parameter:
        click_by_xpath(str(box_xpath + 'table/tbody/tr/td[1]/span[3]'))

        # TODO: Does not work properly, because of "ValueError: invalid literal for int() with base 10: ''".
        #  Must be mentioned, that error is not stable (that means sometimes it comes, sometimes - not).
        #  Must be fixed in future:

        # # Getting the highest price <div> parameter:
        # return_box_root = "/html/body/div[1]/div/section/div[3]/form/div[2]"
        #
        # for rnd_trip in rnd_trips:
        #
        #     # Opens 'See More' graph in order to take the highest price parameter:
        #     click_by_xpath(str(box_xpath + 'table/tbody/tr/td[1]/span[3]'))
        #
        #     price_div_root = str(return_box_root) + str(box_xpath)
        #     price_div = price_div_root + "/div[2]/div[" + str(rnd_trip) + "]/div/div/div[3]/div/div[2]/span"
        #
        #     # Using now-created 'price_div' parameter to extract the highest price:
        #     high_price = find_by_xpath(price_div)
        #     high_price = high_price.text
        #
        #     # Getting rid of currency letters (USD or KES), and leaving only integers:
        #     high_price = high_price[4:]
        #     high_price = int(high_price)
        #
        #     # Getting 'one way' (not full) taxes:
        #     out_tax = high_price - cheapest_in_price
        #     out_taxes.append(out_tax)


# Selects 'round trip' option, which makes sure both depart & return flights will need to be selected:
click_by_xpath('//*[@id="frmFlight"]/div[1]/div[1]/label')

# Selects currency as USD in the 'currency' drop-down menu:
click_by_xpath('//*[@id="frmFlight"]/div[1]/div[3]/select/option[2]')

# Selects 'FROM' drop-down menu, and from it selects 'Nairobi JKIA (NBO):
click_by_xpath('//*[@id="depairportcode"]/option[2]')

# Selects 'TO' drop-down menu, and from it selects 'Mombasa (MBA)':
click_by_xpath('//*[@id="arrvairportcode"]/option[1]')


# _______________________________________________ DEPART DATE PICKER _______________________________________________ #

# Opens 'Depart' calendar / date-picker:
click_by_xpath('//*[@id="date_from"]')

# Gets days left before departure day:
departure_day = get_days_left(depart_after_days[0])

# Gets days left in the current month:
month_left = len(get_month_left())

# Checks if departure day will take place in the current month:
left_to_depart = get_correct_month(
    depart_after_days[0],
    month_left,
    '//*[@id="ui-datepicker-div"]/div/a[2]'
)

if left_to_depart is not None:
    # Changes the month till it finds the correct one:
    while int(left_to_depart) > month_left:
        left_to_depart = get_correct_month(
            left_to_depart,
            month_left,
            '//*[@id="ui-datepicker-div"]/div/a[2]'
        )

# After the correct departure month is known, program gets all (or remaining) days of the departure month.
# Because this is the 'correct' month in which the departure will take place, one of the days will be the one:
dates_dep = get_month_left()

# After the correct departure month is known, selects the correct departure day:
select_depart_day(dates_dep, departure_day)


# _______________________________________________ RETURN DATE PICKER _______________________________________________ #

# Opens 'Return' calendar / date-picker:
click_by_xpath('//*[@id="frmFlight"]/div[2]/div[4]/div/label')

# Getting exact return 'day' parameter:
day_of_return = get_return_day(depart_after_days, return_after_days)

# Program checks if the 'day_of_return' will be in the month selected:
if int(day_of_return) < int(departure_day):

    return_aft = get_return_month(
        departure_day,
        return_after_days[0],
        '//*[@id="ui-datepicker-div"]/div/a[2]/span'
    )

    # Gets days left in the selected month:
    month_left = get_month_left()

    while return_aft > len(month_left):
        return_aft = get_return_month(
            departure_day,
            return_aft,
            '//*[@id="ui-datepicker-div"]/div/a[2]/span'
        )

# After the correct returning month is known, program gets all (or remaining) days of the returning month.
# Because this is the 'correct' month in which the return will take place, one of the days will be the one:
dates_ret = get_month_left()

# After the correct returning month is known, selects the correct returning day:
select_depart_day(dates_ret, day_of_return)

# Clicks on 'Search flights':
click_by_xpath('//*[@id="searchFlight"]')


# ___________________________________________ INITIATING DATA EXTRACTION ___________________________________________ #

# XPath of information boxes windows:
dep_box_xpath = '//*[@id="book-form"]/div[1]/div[2]/'
ret_box_xpath = '//*[@id="book-form"]/div[2]/div[2]/'

# Getting number of flights in a selected day (as well as data tables in web-page):
all_flights = browser.find_elements(
    By.XPATH,
    value='//table[@class="table"]'
)

all_flights = (len(all_flights))

# Getting all 'round_flights' of the day in a list format:
round_flights = int(all_flights / 2)
round_trips = list(range(1, (round_flights + 1)))

# Adding extracted values to the outbound and inbound lists:
get_outbound_lists(dep_box_xpath, round_trips)
get_inbound_lists(ret_box_xpath, round_trips)

# Getting total price parameter by adding 'depart' and 'return' prices:
for i in range(len(cheapest_out_prices)):
    price = cheapest_out_prices[i] + cheapest_in_prices[i]
    total_price.append(price)


# ______________________________________________ WRITING DATA TO .CSV ______________________________________________ #

# # Getting list of all flight info boxes in the web-page:
# info_box = get_info_box_xpath(dep_box_xpath, ret_box_xpath, round_trips)
# print(info_box)

print(outbound_departure_airport)
print(outbound_arrival_airport)
print(outbound_departure_time)
print(outbound_arrival_time)
print(inbound_departure_airport)
print(inbound_arrival_airport)
print(inbound_departure_time)
print(inbound_arrival_time)

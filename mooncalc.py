import datetime

import ephem
import pytz
from astral import Astral
from colorama import Fore, Style
from colorama import init

init()

A = Astral()


def ordinal(number):
    return "%d%s" % (number, "tsnrhtdd"[(number / 10 % 10 != 1) * (number % 10 < 4) * number % 10::4])


A.solar_depression = 'civil'
CITY_NAME = 'Austin'
CITY = A[CITY_NAME]
TZ = pytz.timezone(CITY.timezone)
TIME_ZONE = CITY.timezone
NOW = datetime.datetime.now(TZ)


def get_phase_on_day(year, month, day):
    date = ephem.Date(datetime.date(year, month, day))
    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)
    lunation = (date - pnm) / (nnm - pnm)

    return lunation


def print_moon():
    phase = get_phase_on_day(NOW.year, NOW.month, NOW.day)

    if phase == 0 or phase == 1:
        moon = "%swaxing%s %s (new moon)" % (Fore.GREEN + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F311")
    elif 0 < phase < 0.25:
        moon = "%swaxing%s %s (crescent)" % (Fore.GREEN + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F312")
    elif phase == 0.25:
        moon = "%swaxing%s %s (first quarter)" % (
            Fore.GREEN + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F313")
    elif 0.25 < phase < 0.5:
        moon = "%swaxing%s %s (gibbous)" % (Fore.GREEN + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F314")
    elif phase == 0.5:
        moon = "%swaning%s %s (full moon)" % (Fore.RED + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F315")
    elif 0.5 < phase < 0.75:
        moon = "%swaning%s %s (gibbous)" % (Fore.RED + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F316")
    elif phase == 0.75:
        moon = "%swaning%s %s (last quarter)" % (Fore.RED + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F317")
    elif 0.75 < phase < 1:
        moon = "%swaning%s %s (crescent)" % (Fore.RED + Style.BRIGHT, Fore.RESET + Style.RESET_ALL, u"\U0001F318")
    else:
        moon = ""

    print("\nThe moon is currently %s.\n" % moon)


print_moon()

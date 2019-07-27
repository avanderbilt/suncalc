import datetime
import pytz
import ephem

from colorama import init
from datetime import timedelta
from astral import Astral
from colorama import Fore, Style

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


def print_sun():
    sun = CITY.sun(date=datetime.datetime.now(), local=True)

    sunrise = sun['sunrise']
    noon = sun['noon']
    sunset = sun['sunset']
    midnight = A.solar_midnight_utc(NOW + timedelta(days=1), CITY.longitude).replace(tzinfo=pytz.utc).astimezone(TZ)

    sunrise_time = sunrise.strftime('%-I:%M %p')
    noon_time = noon.strftime('%-I:%M %p')
    sunset_time = sunset.strftime('%-I:%M %p')
    midnight_time = midnight.strftime('%-I:%M %p')

    if sunrise > NOW:
        will_rise_or_rose = "will rise"
    else:
        will_rise_or_rose = "rose"

    if noon > NOW:
        will_be_or_was = "will cross"
    else:
        will_be_or_was = "crossed"

    if sunset > NOW:
        will_set_or_set = "will set"
    else:
        will_set_or_set = "set"

    if midnight > NOW:
        will_reach_or_reached = "will reach"
    else:
        will_reach_or_reached = "reached"

    print("%sThe sun %s at %s%s.%s" % (Fore.YELLOW, will_rise_or_rose, Fore.YELLOW + Style.BRIGHT, sunrise_time,
                                       Style.RESET_ALL + Fore.RESET))
    print("%sThe sun %s the meridian at %s%s.%s" % (Fore.YELLOW, will_be_or_was, Fore.YELLOW + Style.BRIGHT, noon_time,
                                                    Style.RESET_ALL + Fore.RESET))
    print("%sThe sun %s at %s%s.%s" % (Fore.YELLOW, will_set_or_set, Fore.YELLOW + Style.BRIGHT, sunset_time,
                                       Style.RESET_ALL + Fore.RESET))
    print("%sThe sun %s the nadir at %s%s.%s\n" % (Fore.YELLOW, will_reach_or_reached, Fore.YELLOW + Style.BRIGHT,
                                                   midnight_time, Style.RESET_ALL + Fore.RESET))


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

    print("The moon is currently %s (%s).\n" % (moon, "{0:.0%}".format(phase)))


def print_report():
    print("%sSolar and Lunar Report for %s on %s %s:%s\n" % (Fore.WHITE + Style.BRIGHT, CITY_NAME,
                                                             NOW.strftime("%A, %B"), ordinal(NOW.day),
                                                             Style.RESET_ALL + Fore.RESET))

    print_sun()
    print_moon()

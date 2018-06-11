import pandas as pd
from datetime import datetime
from helperfunctions import *
import matplotlib.pyplot as plt
import calendar

aa = pd.read_csv('spotrates.csv')
aa.expiration = pd.to_datetime(aa.expiration)


def toTimeStamp(d):
    return calendar.timegm(d.timetuple())


def calculateoptionrates(expirations, accumpvlist, boxrateadjust):
    interprates = np.interp(expirations.apply(toTimeStamp), accumpvlist.expiration.apply(toTimeStamp), accumpvlist.spot)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    timeinterval = (expirations - today) / np.timedelta64(1, 'D') / 365

    return interprates / timeinterval - boxrateadjust


# aa = pd.Series([datetime(2019, m, 21) for m in range(1, 13)])
# bb = pd.read_csv('spotrates.csv')
# bb.expiration = pd.to_datetime(bb.expiration)
#
# cc = calculateoptionrates(aa, bb)
# print(cc)

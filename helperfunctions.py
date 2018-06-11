import pandas as pd
import numpy as np
from datetime import datetime


def forwardratecalculator(today, startdate, enddate, startrate, endrate):
    t1 = (startdate - today).days / 365.0
    t2 = (enddate - today).days / 365.0

    return (t2 * endrate - t1 * startrate) / (((enddate - startdate).days) / 365.0)


def divforwardpricecalculator(startforward, startdate, enddate, bucketrate, divrate):
    t = (enddate - startdate).days / 365.0

    return startforward * np.exp((bucketrate - divrate) * t)


def discreteforwardpricecalculator(startforward, startdate, enddate, bucketrate, divamount):
    t = (enddate - startdate).days / 365.0

    return startforward * np.exp(bucketrate * t) - divamount



def rollcalculator(discreteroll, divroll, discreteportion):
    return discreteroll * discreteportion + divroll * (1 - discreteportion)

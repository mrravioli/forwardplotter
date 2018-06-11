from helperfunctions import *


class ForwardCurve:
    def __init__(self, dataprovider):
        self.provider = dataprovider

    def getbucketrates(self, spotrates):
        dates = pd.to_datetime(spotrates.expiration)
        spotrates = spotrates.spot

        bucketrates = [spotrates[0]]
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        for i in range(len(dates)-1):
            bucketrates += [forwardratecalculator(today, dates[i], dates[i + 1], spotrates[i], spotrates[i + 1])]

        result = pd.DataFrame(dates)
        result['bucketrates'] = pd.Series(bucketrates)

        return result

    def _getforwardpricesandrolls(self, spotrates, driverindex, driverprice, discreteamounts, divrates,
                                  discreteportion):
        bucketrates = (self.getbucketrates(spotrates)).bucketrates
        dates = pd.to_datetime(spotrates.expiration)

        discreterolls = [0] * len(spotrates)
        divrolls = [0] * len(spotrates)
        discreteforward = [0] * len(spotrates)
        divforward = [0] * len(spotrates)
        rolls = [0] * len(spotrates)
        forwards = [0] * len(spotrates)

        discreterolls[driverindex] = 0
        divrolls[driverindex] = 0
        discreteforward[driverindex] = driverprice
        divforward[driverindex] = driverprice
        rolls[driverindex] = 0
        forwards[driverindex] = driverprice

        for i in range(driverindex + 1, len(spotrates)):
            discreteforward[i] = discreteforwardpricecalculator(discreteforward[i - 1], dates[i - 1], dates[i],
                                                                bucketrates[i], discreteamounts[i])
            divforward[i] = discreteforwardpricecalculator(discreteforward[i - 1], dates[i - 1], dates[i],
                                                           bucketrates[i], divrates[i])
            rolls[i] = rollcalculator(discreteforward[i] - discreteforward[i - 1], divforward[i] - divforward[i - 1],
                                      discreteportion)
            forwards[i] = forwards[i - 1] + rolls[i]


        for i in range(driverindex):
            discreteforward[driverindex - i - 1] = discreteforwardpricecalculator(discreteforward[driverindex - i],
                                                                dates[driverindex - i], dates[driverindex - i - 1],
                                                                bucketrates[driverindex - i],
                                                                discreteamounts[driverindex - i])
            divforward[driverindex - i - 1] = discreteforwardpricecalculator(discreteforward[driverindex - i],
                                                                dates[driverindex - i], dates[driverindex - i - 1],
                                                                bucketrates[driverindex - i],
                                                                discreteamounts[driverindex - i])
            rolls[driverindex - i - 1] = rollcalculator(
                discreteforward[driverindex - i] - discreteforward[driverindex - i - 1],
                divforward[driverindex - i] - divforward[driverindex - i],
                discreteportion)

        return forwards
from helperfunctions import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

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

    def getforwardpricesandrolls(self, spotrates, driverindex, driverprice, discreteamounts, divrates,
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
            forwards[driverindex - i - 1] = forwards[driverindex - i] - rolls[driverindex - i - 1]

        return forwards


aa = pd.read_csv('spotrates.csv')
bb = ForwardCurve('dataprovider')

cc = bb.getforwardpricesandrolls(aa, 8, 100, [0.1]*len(aa), [0.008]*len(aa), 0.5)




fig, ax = plt.subplots()

plt.subplots_adjust(left=0.25, bottom=0.25)
t = aa.expiration
l, = plt.plot(t, cc, linestyle='-',marker='o')

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

sfreq = Slider(axfreq, 'Freq', 50, 200, valinit=100)
samp = Slider(axamp, 'Amp', 0, 0.3, valinit=0.1)


def update(val):
    amp = samp.val
    freq = sfreq.val
    new_data = bb.getforwardpricesandrolls(aa, 8, freq, [amp]*len(aa), [0.008]*len(aa), 0.5)
    l.set_ydata(new_data)
    fig.relim()
    fig.autoscale_view()
    fig.canvas.draw_idle()
sfreq.on_changed(update)
samp.on_changed(update)

plt.show()

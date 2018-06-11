import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


class ForwardCurvePlotter:
    def __init__(self, forwardcurve):
        self.forwardcurve = forwardcurve

    def plot(self):
        fig, ax = plt.subplots()

        plt.subplots_adjust(left=0.25, bottom=0.25)
        spotrates = self.forwardcurve.dataprovider.spotrates
        t = spotrates.expiration
        f = self.forwardcurve.getforwardpricesandrolls
        l, = plt.plot(t, f, linestyle='-', marker='o')

        axcolor = 'lightgoldenrodyellow'
        axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

        sfreq = Slider(axfreq, 'Freq', 50, 200, valinit=100)
        samp = Slider(axamp, 'Amp', 0, 0.3, valinit=0.1)

        def update(val):
            amp = samp.val
            freq = sfreq.val
            new_data = self.forwardcurve.getforwardpricesandrolls(spotrates, 8, freq, [amp] * len(spotrates), [0.008] * len(spotrates), 0.5)
            l.set_ydata(new_data)
            fig.canvas.draw_idle()

        sfreq.on_changed(update)
        samp.on_changed(update)

        plt.show()

from bsoption import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.subplots_adjust(left=0.25, bottom=0.25)

isCall0 = isCall_updated = 1
k0 = k_updated = 100
r0 = r_updated = 0.02
vol0 = vol_updated = 0.2
div0 = div_updated = 0.01


X = np.arange(0.1, 200, 5)
Y = np.arange(0.1, 20, 0.1)
X, Y = np.meshgrid(X, Y)
zs = np.array([BSOption(isCall0, x, k0, y, r0, vol0, div0).get_delta() for x, y in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)

ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)


# option type updater
type_radio_ax = plt.axes([0.025, 0.5, 0.15, 0.15])
type_radio = RadioButtons(type_radio_ax, ('Call', 'Put'), active=0)


def update_type(label):
    global isCall_updated

    if label == 'Call':
        isCall_updated = 1
    elif label == 'Put':
        isCall_updated == 0

    print(label=='Put', isCall_updated)

    ax.clear()
    zs_updated = np.array(
        [BSOption(isCall_updated, x, k_updated, y, r_updated, vol_updated, div_updated).get_delta() for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z_updated = zs_updated.reshape(X.shape)

    ax.plot_surface(X, Y, Z_updated, cmap=cm.coolwarm)
    fig.canvas.draw_idle()


type_radio.on_clicked(update_type)


# strike slide
strike_slide_ax = plt.axes([0.2, 0.2, 0.65, 0.02])
strike_slide = Slider(strike_slide_ax, "strike", 10, 200, valinit=k0)
r_slide_ax = plt.axes([0.2, 0.15, 0.65, 0.02])
r_slide = Slider(r_slide_ax, "risk free rate", 0, 0.1, valinit=r0)
vol_slide_ax = plt.axes([0.2, 0.1, 0.65, 0.02])
vol_slide = Slider(vol_slide_ax, "vol", 0.01, 2, valinit=vol0)
div_slide_ax = plt.axes([0.2, 0.05, 0.65, 0.02])
div_slide = Slider(div_slide_ax, "dividend rate", 0, 0.3, valinit=div0)


def update_parameters(val):
    global k_updated
    global r_updated
    global vol_updated
    global div_updated

    k_updated = strike_slide.val
    r_updated = r_slide.val
    vol_updated = vol_slide.val
    div_updated = div_slide.val

    ax.clear()
    zs_updated = np.array(
        [BSOption(isCall_updated, x, k_updated, y, r_updated, vol_updated, div_updated).get_delta() for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z_updated = zs_updated.reshape(X.shape)

    ax.plot_surface(X, Y, Z_updated, cmap=cm.coolwarm)
    fig.canvas.draw_idle()


strike_slide.on_changed(update_parameters)
r_slide.on_changed(update_parameters)
vol_slide.on_changed(update_parameters)
div_slide.on_changed(update_parameters)


ax.set_xlabel('underlying price')
ax.set_ylabel('time to maturity')
ax.set_zlabel('delta')

plt.show()

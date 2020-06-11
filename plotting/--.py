"""
Brief illustration of re-plotting vs data-updating.

@author: plesser
"""

import matplotlib.pyplot as plt
import numpy as np

def update(n_steps):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 1)

    line = ax.plot(np.arange(n_steps),
                   np.full(n_steps, np.nan), 'b-')[0]

    for n in range(n_steps):
        ydata = line.get_ydata()
        ydata[n] = np.random.random()
        line.set_ydata(ydata)
        plt.pause(1e-6)


if __name__ == '__main__':
    update(1000)

    plt.show()

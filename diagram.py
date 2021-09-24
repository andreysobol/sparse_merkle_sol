import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

def create_plot(gas_used_add, gas_used_remove):

    xdata1 = [item for item in range(0, len(gas_used_add))]
    xdata2 = [item for item in range(0, len(gas_used_remove))]

    # create some y data points
    ydata1 = gas_used_add
    ydata2 = gas_used_remove

    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)


    ax.plot(xdata1, ydata1, color='tab:blue', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata2, ydata2, color='tab:orange', marker='o', markersize=1, linewidth = 0.0)

    # set the limits
    ax.set_xlim([0, 1024])
    ax.set_ylim([0, 350000])

    ax.set_title('Add (blue) and Remove (orange)')

    # display the plot
    plt.savefig('plot.png')
    plt.show()

import json

def read_from_file_and_run():
    with open('raw_data.json') as json_file:
        data = json.load(json_file)
        create_plot(data["gas_used_add"], data["gas_used_remove"])

read_from_file_and_run()
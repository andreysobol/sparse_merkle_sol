import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

def create_plot(gas_used_add, gas_used_remove):
    # Fixing random state for reproducibility
    #np.random.seed(19680801)

    # create random data
    #xdata = np.random.random([2, 10])

    # split the data into two parts
    #xdata1 = xdata[0, :]
    #xdata2 = xdata[1, :]

    # sort the data so it makes clean curves
    #xdata1.sort()
    #xdata2.sort()

    xdata1 = [item for item in range(0, len(gas_used_add))]
    xdata2 = [item for item in range(0, len(gas_used_remove))]

    # create some y data points
    ydata1 = gas_used_add
    ydata2 = gas_used_remove

    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xdata1, ydata1, color='tab:blue', linewidth = 0.25)
    ax.plot(xdata2, ydata2, color='tab:orange', linewidth = 0.25)

    # create the events marking the x data points
    #xevents1 = EventCollection(xdata1, color='tab:blue', linelength=0.05)
    #xevents2 = EventCollection(xdata2, color='tab:orange', linelength=0.05)

    # create the events marking the y data points
    #yevents1 = EventCollection(ydata1, color='tab:blue', linelength=0.05,
    #                        orientation='vertical')
    #yevents2 = EventCollection(ydata2, color='tab:orange', linelength=0.05,
    #                        orientation='vertical')

    # add the events to the axis
    #ax.add_collection(xevents1)
    #ax.add_collection(xevents2)
    #ax.add_collection(yevents1)
    #ax.add_collection(yevents2)

    # set the limits
    ax.set_xlim([0, 1024])
    ax.set_ylim([0, 350000])

    ax.set_title('Add (blue) and Remove (orange)')

    # display the plot
    #plt.savefig('plot.png')
    plt.show()

import json

def read_from_file_and_run():
    with open('raw_data.json') as json_file:
        data = json.load(json_file)
        create_plot(data["gas_used_add"], data["gas_used_remove"])

read_from_file_and_run()
#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

def create_plot(gas_used_add_sha, gas_used_remove_sha, gas_used_add_keccak, gas_used_remove_keccak):

    xdata1 = [item for item in range(0, len(gas_used_add_sha))]
    xdata2 = [item for item in range(0, len(gas_used_remove_sha))]

    xdata3 = [item for item in range(0, len(gas_used_add_keccak))]
    xdata4 = [item for item in range(0, len(gas_used_remove_keccak))]

    # create some y data points
    ydata1 = gas_used_add_sha
    ydata2 = gas_used_remove_sha

    ydata3 = gas_used_add_keccak
    ydata4 = gas_used_remove_keccak

    # plot the data
    fig = plt.figure()
    fig.set_size_inches(10, 7)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel("gas")
    ax.set_xlabel("update index")


    ax.plot(xdata1, ydata1, color='orangered', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata2, ydata2, color='darkred', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata3, ydata3, color='lime', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata4, ydata4, color='green', marker='o', markersize=1, linewidth = 0.0)

    ax.legend(['Sha256 add element', 'Sha256 remove element', 'Keccak256 add element', 'Keccak256 remove element'])

    # set the limits
    ax.set_xlim([0, 1024])
    ax.set_ylim([0, 400000])

    ax.set_title('Gas usage')

    # display the plot
    plt.savefig('plot.png')
    plt.show()

def create_plot2(
    gas_used_add_sha,
    gas_used_remove_last_sha,
    gas_used_remove_random_sha,
    gas_used_add_keccak,
    gas_used_remove_last_keccak,
    gas_used_remove_random_keccak,
):

    xdata1 = [item for item in range(0, len(gas_used_add_sha))]
    xdata2 = [item for item in range(0, len(gas_used_remove_last_sha))]
    xdata3 = [item for item in range(0, len(gas_used_remove_random_sha))]

    xdata4 = [item for item in range(0, len(gas_used_add_keccak))]
    xdata5 = [item for item in range(0, len(gas_used_remove_last_keccak))]
    xdata6 = [item for item in range(0, len(gas_used_remove_random_keccak))]

    # create some y data points
    ydata1 = gas_used_add_sha
    ydata2 = gas_used_remove_last_sha
    ydata3 = gas_used_remove_random_sha

    ydata4 = gas_used_add_keccak
    ydata5 = gas_used_remove_last_keccak
    ydata6 = gas_used_remove_random_keccak

    # plot the data
    fig = plt.figure()
    fig.set_size_inches(10, 7)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel("gas")
    ax.set_xlabel("update index")


    ax.plot(xdata1, ydata1, color='orangered', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata2, ydata2, color='darkred', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata3, ydata3, color='magenta', marker='o', markersize=1, linewidth = 0.0)

    ax.plot(xdata4, ydata4, color='lime', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata5, ydata5, color='green', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata6, ydata6, color='aquamarine', marker='o', markersize=1, linewidth = 0.0)

    ax.legend([
        'Sha256 add element',
        'Sha256 remove last',
        'Sha256 remove random',
        'Keccak256 add element',
        'Keccak256 remove last',
        'Keccak256 remove random',
    ])

    # set the limits
    ax.set_xlim([0, 1024])
    ax.set_ylim([0, 400000])

    ax.set_title('Gas usage')

    # display the plot
    plt.savefig('plot2.png')
    plt.show()

def create_plot_set_sha(
    gas_used_add_sha,
    gas_used_remove_last_sha,
    gas_used_remove_random_sha,
):

    xdata1 = [item for item in range(0, len(gas_used_add_sha))]
    xdata2 = [item for item in range(0, len(gas_used_remove_last_sha))]
    xdata3 = [item for item in range(0, len(gas_used_remove_random_sha))]

    # create some y data points
    ydata1 = gas_used_add_sha
    ydata2 = gas_used_remove_last_sha
    ydata3 = gas_used_remove_random_sha

    # plot the data
    fig = plt.figure()
    fig.set_size_inches(10, 7)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel("gas")
    ax.set_xlabel("update index")


    ax.plot(xdata1, ydata1, color='red', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata2, ydata2, color='green', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata3, ydata3, color='blue', marker='o', markersize=1, linewidth = 0.0)

    ax.legend([
        'Sha256 add element',
        'Sha256 remove last',
        'Sha256 remove random',
    ])

    # set the limits
    ax.set_xlim([0, 1024])
    ax.set_ylim([0, 400000])

    ax.set_title('Gas usage')

    # display the plot
    plt.savefig('plot_set_sha.png')
    plt.show()

def create_plot_set_keccak(
    gas_used_add_keccak,
    gas_used_remove_last_keccak,
    gas_used_remove_random_keccak,
):

    xdata4 = [item for item in range(0, len(gas_used_add_keccak))]
    xdata5 = [item for item in range(0, len(gas_used_remove_last_keccak))]
    xdata6 = [item for item in range(0, len(gas_used_remove_random_keccak))]

    # create some y data points
    ydata4 = gas_used_add_keccak
    ydata5 = gas_used_remove_last_keccak
    ydata6 = gas_used_remove_random_keccak

    # plot the data
    fig = plt.figure()
    fig.set_size_inches(10, 7)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel("gas")
    ax.set_xlabel("update index")


    ax.plot(xdata4, ydata4, color='red', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata5, ydata5, color='green', marker='o', markersize=1, linewidth = 0.0)
    ax.plot(xdata6, ydata6, color='blue', marker='o', markersize=1, linewidth = 0.0)

    ax.legend([
        'Keccak256 add element',
        'Keccak256 remove last',
        'Keccak256 remove random',
    ])

    # set the limits
    ax.set_xlim([0, 1024])
    ax.set_ylim([0, 400000])

    ax.set_title('Gas usage')

    # display the plot
    plt.savefig('plot_set_keccak.png')
    plt.show()

import json

def read_from_file_and_run():
    with open('raw_data_sha.json') as json_sha_file:
        with open('raw_data_keccak.json') as json_keccak_file:
            data_sha = json.load(json_sha_file)
            data_keccak = json.load(json_keccak_file)
            create_plot(data_sha["gas_used_add"], data_sha["gas_used_remove"], data_keccak["gas_used_add"], data_keccak["gas_used_remove"])

    #with open('raw_data_set_sha.json') as json_sha_file:
    #    with open('raw_data_set_keccak.json') as json_keccak_file:
    #        data_sha = json.load(json_sha_file)
    #        data_keccak = json.load(json_keccak_file)
    #        create_plot2(
    #            data_sha["gas_used_add"],
    #            data_sha["gas_used_remove_last"],
    #            data_sha["gas_used_remove_random"],
    #            data_keccak["gas_used_add"],
    #            data_keccak["gas_used_remove_last"],
    #            data_keccak["gas_used_remove_random"],
    #        )

    with open('raw_data_set_sha.json') as json_sha_file:
        data_sha = json.load(json_sha_file)
        create_plot_set_sha(
            data_sha["gas_used_add"],
            data_sha["gas_used_remove_last"],
            data_sha["gas_used_remove_random"],
        )

    with open('raw_data_set_keccak.json') as json_keccak_file:
        data_keccak = json.load(json_keccak_file)
        create_plot_set_keccak(
            data_keccak["gas_used_add"],
            data_keccak["gas_used_remove_last"],
            data_keccak["gas_used_remove_random"],
        )

read_from_file_and_run()

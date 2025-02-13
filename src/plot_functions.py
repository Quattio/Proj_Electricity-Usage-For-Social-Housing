import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(bin_width, data, xlabel, outputname, x_max=None): 
    binWidth = bin_width
    bins = np.arange(min(data), max(data) + binWidth, binWidth)

    plt.figure()
    plt.hist(data, bins=bins, edgecolor='black', alpha=0.75)
    plt.xlabel(xlabel)
    plt.ylabel('Counts')
    if x_max is not None:
        plt.xlim(0, x_max) 
    plt.savefig('../Plots/' + outputname + '.png')
    plt.close()




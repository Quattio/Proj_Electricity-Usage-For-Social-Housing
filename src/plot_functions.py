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


def plot_histogram_two_overlap(bin_width, data1, data2, xlabel, outputname, unit, x_max=None):
    binWidth = bin_width
    bins = np.arange(min(min(data1), min(data2)), max(max(data1), max(data2))+binWidth, binWidth )

    plt.figure()
    plt.hist(data1, bins=bins, edgecolor='black', alpha=0.75, label='pre Quatt:' + ' average is ' + str(round(data1.mean(), 1)) + ' ' + unit )
    plt.hist(data2, bins=bins, edgecolor='black', alpha=0.75, label='after Quatt:' + ' average is ' + str(round(data2.mean(), 1)) + ' ' + unit)
    plt.xlabel(xlabel)
    plt.ylabel('Counts')
    if x_max is not None:
        plt.xlim(0, x_max)
    plt.legend(fontsize=50)
    #plt.yscale("log")
    plt.savefig('../Plots/' + outputname + '.png')
    plt.close()


def plot_as_usage_during_day(data_during_day, xaxis, columname, ylabel, outputname, monthname):

    plt.figure(figsize=(30, 16))

    max_value = data_during_day[columname].max()
    min_value = data_during_day[columname].min()
    max_time = data_during_day.loc[data_during_day[columname].idxmax(), xaxis]
    min_time = data_during_day.loc[data_during_day[columname].idxmin(), xaxis]

    plt.plot(data_during_day[xaxis], data_during_day[columname], color='b')

    plt.ylabel(ylabel)

    time_slots = data_during_day[xaxis]
    hourly_ticks = time_slots[::6]
    plt.xticks(hourly_ticks, rotation=45, fontsize=20)
    plt.scatter([max_time], [max_value], color='r', s=600, label='Max Value', zorder=3)  
    plt.scatter([min_time], [min_value], color='g', s=600, label='Min Value', zorder=3)  
    plt.annotate(f'Max: {max_value:.4f}', xy=(max_time, max_value), xytext=(max_time, max_value + 0.0005),
                 arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=40, color='red')
    plt.annotate(f'Min: {min_value:.4f}', xy=(min_time, min_value), xytext=(min_time, min_value - 0.0005),
                 arrowprops=dict(facecolor='green', arrowstyle='->'), fontsize=40, color='green')

    plt.legend(fontsize=18)
    plt.grid()
    plt.savefig('../Plots/' + outputname + monthname + '.png')
    plt.close()


def plot_proerty_diffgroup(bin_centers, data, xlabel, ylabel, outputname):
    plt.figure(figsize=(30, 16))
    plt.plot(bin_centers[1:], data[1:-1], marker='o', markersize=20, linestyle='-', linewidth=8, color='b')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.legend()
    plt.savefig('../Plots/' + outputname )

def plot_proerty_diffgroup_two_overlap(bin_centers, data1, data2, xlabel, ylabel, outputname):
    plt.figure(figsize=(30, 16))
    plt.plot(bin_centers[1:], data1[1:-1], marker='o', markersize=20, linestyle='-', linewidth=8, color='b', label='pre Quatt')
    plt.plot(bin_centers[1:], data2[1:-1], marker='s', markersize=20, linestyle='-', linewidth=8, color='r', label='after Quatt')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig('../Plots/' + outputname )


def plot_property_diffenergylabel(energylabels, data, number_of_customer_diffenergylabel, bar_labels, xlabel, ylabel, outputname): 
    barlabel = [str(i)+ ' houses' for i in number_of_customer_diffenergylabel]
    fig, ax = plt.subplots()
    bar = ax.bar(energylabels, data, label=bar_labels)
    ax.bar_label(bar, labels=barlabel, label_type='edge', fontsize=35, padding=30)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.savefig('../Plots/' + outputname )

def printresult(data, nubmer_of_customer_afterQuatt):
    print("\033[1;31mFor all houses: " + "\033[0m")
    print("\033[1;31mAverage of gas_usage per year per house: \033[35m" + str(sum(data['gas_usage']) / nubmer_of_customer_afterQuatt) + " m^3" + "\033[0m")
    print("\033[1;31mAverage of co2_emission  per year per house: \033[35m" + str(sum(data['co2_emission']) / nubmer_of_customer_afterQuatt) + " kg" + "\033[0m")
    print("\033[1;31mAverage of gas_usage per year per house per M2: \033[35m" + str(sum(data['gas_usage_perM2']) / nubmer_of_customer_afterQuatt) + " m" + "\033[0m")
    print("\033[1;31mAverage of co2_emission per year per house per M2: \033[35m" + str(sum(data['co2_emission_perM2']) / nubmer_of_customer_afterQuatt) + " kg/m^2" + "\033[0m")
    print(prequatt['NATURAL_GAS_perM2'])
    print(data['gas_usage_perM2'])

def plot_statistics_energylabels(energylabels, number_of_customer_diffenergylabel):
    barlabel = [str(i)+ ' houses' for i in number_of_customer_diffenergylabel]

    fig, ax = plt.subplots()
    bar = ax.bar(energylabels, number_of_customer_diffenergylabel, label=barlabel)
    ax.bar_label(bar, labels=barlabel, label_type='edge', fontsize=35, padding=30)
    plt.xlabel("Energy Labels")
    plt.ylabel("Number of houses")
    #plt.legend()
    plt.savefig('../Plots/' + 'statistics_energylabels.png' )

def plot_statistics_housesize(bin_centers, houselabels, number_of_customer_diffenenthousesize):

    barlabel = [str(i)+ ' houses' for i in number_of_customer_diffenenthousesize]

    fig, ax = plt.subplots(figsize=(30, 16))
    bar = ax.bar(houselabels, number_of_customer_diffenenthousesize, label=barlabel)
    ax.bar_label(bar, labels=barlabel, label_type='edge', fontsize=35, padding=30)
   
    ax.set_xticks(range(len(houselabels)))  
    ax.set_xticklabels(houselabels, fontsize=40) 

    plt.xlabel("House size (M2)")
    plt.ylabel("Number of houses")
    #plt.legend()
    plt.savefig('../Plots/' + 'statistics_housesize.png' )




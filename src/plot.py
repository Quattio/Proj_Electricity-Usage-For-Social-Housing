import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plot_functions
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utility import PythonPlotDefaultParameters

def main():

    # load data
    cicdata = pd.read_csv('../Data/CIC_MoreThanOneYear.csv')
    deal=pd.read_csv('../Data/Deal.csv')
    data = pd.read_csv('../Data/CombinedData.csv')

    # parameters
    housebins = [0, 50, 100, 150, 200, 250, 300, 350, 400, float('inf')]
    houselabels = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400', '400+']

    # calculation
    nubmer_of_customer = len(data)
    data['HOUSESIZE_CATEGORY'] = pd.cut(data['PROPERTY_DIMENSIONSOFTHEHOUSE'], bins=housebins, labels=houselabels, right=False)
    data['gas_usage']          = data['Q_CV'] / 1000 / 8.8 # Wh -> kWh -> m^3
    data['gas_usage_perM2']    = data['Q_CV'] / 1000 / 8.8 / data['PROPERTY_DIMENSIONSOFTHEHOUSE']
    data['co2_emission']       = data['Q_CV'] / 1000 / 8.8 * 1.788  + (data['E_HP1'] + data['E_HP2']) * 0.272 / 1000  # in kg
    data['co2_emission_perM2'] = (data['Q_CV'] / 1000 / 8.8 * 1.788  + (data['E_HP1'] + data['E_HP2']) * 0.272 / 1000) / data['PROPERTY_DIMENSIONSOFTHEHOUSE']

    # print result
    for housesize in houselabels:
        print("\033[1;31mFor house size \033[35m" + housesize )
        print("\033[1;31mFor house size \033[35m" + housesize + "\033[1;31m, average of gas_usage per year per house: \033[35m" + str(sum(data[data['HOUSESIZE_CATEGORY'] == housesize]['gas_usage']) / len(data[data['HOUSESIZE_CATEGORY'] == housesize])) + " m^3" + "\033[0m")
        print("\033[1;31mFor house size \033[35m" + housesize + "\033[1;31m, average of co2_emission per year per house: \033[35m" + str(sum(data[data['HOUSESIZE_CATEGORY'] == housesize]['co2_emission']) / len(data[data['HOUSESIZE_CATEGORY'] == housesize])) + " kg" + "\033[0m")
        print("\033[1;31mFor house size \033[35m" + housesize + "\033[1;31m, average of gas_usage per year per house per M2: \033[35m" + str(sum(data[data['HOUSESIZE_CATEGORY'] == housesize]['gas_usage_perM2']) / len(data[data['HOUSESIZE_CATEGORY'] == housesize])) + " m" + "\033[0m")
        print("\033[1;31mFor house size \033[35m" + housesize + "\033[1;31m, average of co2_emission per year per house per M2: \033[35m" + str(sum(data[data['HOUSESIZE_CATEGORY'] == housesize]['co2_emission_perM2']) / len(data[data['HOUSESIZE_CATEGORY'] == housesize])) + " kg/m^2" + "\033[0m")
        print('\n')

    print("\033[1;31mFor all houses: " + "\033[0m")
    print("\033[1;31mAverage of gas_usage per year per house: \033[35m" + str(sum(data['gas_usage']) / nubmer_of_customer) + " m^3" + "\033[0m")
    print("\033[1;31mAverage of co2_emission  per year per house: \033[35m" + str(sum(data['co2_emission']) / nubmer_of_customer) + " kg" + "\033[0m")
    print("\033[1;31mAverage of gas_usage per year per house per M2: \033[35m" + str(sum(data['gas_usage_perM2']) / nubmer_of_customer) + " m" + "\033[0m")
    print("\033[1;31mAverage of co2_emission per year per house per M2: \033[35m" + str(sum(data['co2_emission_perM2']) / nubmer_of_customer) + " kg/m^2" + "\033[0m")

    # plot
    plot_functions.plot_histogram(10, data['gas_usage'], 'Gas Usage (m^3)', 'gas_usage', 1000)
    plot_functions.plot_histogram(0.05, data['gas_usage_perM2'], 'Gas Usage per M2 (m)', 'gas_usage_perM2', 10)  
    plot_functions.plot_histogram(20, data['co2_emission'], 'CO2 emission (kg)', 'co2_emission', 4000)
    plot_functions.plot_histogram(0.5, data['co2_emission_perM2'], 'CO2 emission per M2 (kg/m^2)', 'co2_emission_perM2', 40)
    plot_functions.plot_histogram(10, data['PROPERTY_DIMENSIONSOFTHEHOUSE'], 'house_area (m^2)', 'house_area', 1000)

if __name__ == "__main__":
    main()




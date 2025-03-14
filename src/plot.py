import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plot_functions
import sys
import os
import utility

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utility import PythonPlotDefaultParameters

def main():
    installation_type = 'Hybrid'

    # initial empty result file
    df_result = pd.DataFrame(index=range(60000))


    monthname_all = ['10_2023_to_03_2024', '10_2023_to_03_2024_Hybrid', '10_2023_to_03_2024_DUO']
    # monthname_all = ['01_2024_to_01_2025']
    # monthname_all = ['02_2024']
    # monthname_all = ['02_2024', '03_2024', '04_2024', '05_2024', '06_2024', '07_2024', '08_2024', '09_2024', '10_2024', '11_2024', '12_2024', '01_2025', '10_2023_to_03_2024', '01_2024_to_01_2025']

    for monthname in monthname_all:   

        # load data
        afterquatt = pd.read_csv('../Data/CombinedData.csv')
        prequatt = pd.read_csv('../Data/pre_quatt.csv')
        # load electricity data
        data_electricity_usage_year          = pd.read_csv('../Data/data_during_day_Electricity_Usage_01_02_2024_to_01_02_2025_Hybrid.csv')
        data_electricity_usage_heatingseason = pd.read_csv('../Data/data_during_day_Electricity_Usage_01_10_2024_to_20_02_2025.csv')
        # load data:during the day
        data_during_day = pd.read_csv('../Data/data_during_day_' + monthname + '.csv')


        # prepare
        prequatt, afterquatt, data_resampled, aggrgate_during_day_10mins, aggrgate_during_day_hourly = utility.prepare(prequatt, afterquatt, data_during_day, data_electricity_usage_year, data_electricity_usage_heatingseason, 'DUO')

        # parameters
        housebins = [0, 50, 100, 150, 200, 250, 300, 350, 400, float('inf')]
        houselabels = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400', '400+']
        bin_centers = [(housebins[i] + housebins[i + 1]) / 2 for i in range(len(housebins) - 1) if housebins[i + 1] != float('inf')]

        energylabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'X']

        # property calculation
        electricity_usage_year = data_electricity_usage_year['electricity_usage'].mean()
        print("electricity_usage_year: " + str(electricity_usage_year) + ' kWh')
        electricity_usage_heatingseason = data_electricity_usage_heatingseason['electricity_usage'].mean()
        #print("electricity_usage_heatingseason: " + str(electricity_usage_heatingseason) + ' kWh')

        utility.calculations(afterquatt, prequatt,housebins, houselabels)

        # property for sub group calculation
        number_of_customer_diffenenthousesize       = []
        gas_usage_perM2_afterQuatt_diffhousesize    = []
        gas_usage_perhouse_afterQuatt_diffhousesize = []
        co2_emission_perM2_afterQuatt_diffhousesize = []
        gas_usage_perM2_preQuatt_diffhousesize      = []
        gas_usage_perhouse_preQuatt_diffhousesize   = []
        co2_emission_perM2_preQuatt_diffhousesize   = []

        number_of_customer_diffenergylabel            = []
        gas_usage_perM2_afterQuatt_diffenergylabel    = []
        co2_emission_perM2_afterQuatt_diffenergylabel = []
        gas_usage_perM2_preQuatt_diffenergylabel      = []
        co2_emission_perM2_preQuatt_diffenergylabel   = []

        for housesize in houselabels:
            number_of_customer_diffenenthousesize      .append(len(afterquatt[afterquatt['HOUSESIZE_CATEGORY'] == housesize])) 
            gas_usage_perhouse_afterQuatt_diffhousesize.append(sum(afterquatt[afterquatt['HOUSESIZE_CATEGORY'] == housesize]['gas_usage']) / len(afterquatt[afterquatt['HOUSESIZE_CATEGORY'] == housesize]))
            gas_usage_perM2_afterQuatt_diffhousesize   .append(sum(afterquatt[afterquatt['HOUSESIZE_CATEGORY'] == housesize]['gas_usage_perM2']) / len(afterquatt[afterquatt['HOUSESIZE_CATEGORY'] == housesize]))
            co2_emission_perM2_afterQuatt_diffhousesize.append(sum(afterquatt[afterquatt['HOUSESIZE_CATEGORY'] == housesize]['co2_emission_perM2']) / len(afterquatt[afterquatt['HOUSESIZE_CATEGORY'] == housesize]))
            gas_usage_perhouse_preQuatt_diffhousesize  .append(sum(prequatt[prequatt['HOUSESIZE_CATEGORY'] == housesize]['NATURAL_GAS']) / len(prequatt[prequatt['HOUSESIZE_CATEGORY'] == housesize]) )
            gas_usage_perM2_preQuatt_diffhousesize     .append(sum(prequatt[prequatt['HOUSESIZE_CATEGORY'] == housesize]['NATURAL_GAS_perM2']) / len(prequatt[prequatt['HOUSESIZE_CATEGORY'] == housesize]) )
            co2_emission_perM2_preQuatt_diffhousesize  .append(sum(prequatt[prequatt['HOUSESIZE_CATEGORY'] == housesize]['co2_emission_updated_perM2']) / len(prequatt[prequatt['HOUSESIZE_CATEGORY'] == housesize]) )
        for energylabel in energylabels:
            if len(afterquatt[afterquatt['ENERGIELABEL'] == energylabel]) !=0:
                number_of_customer_diffenergylabel           .append( len(afterquatt[afterquatt['ENERGIELABEL'] == energylabel]) )
                gas_usage_perM2_afterQuatt_diffenergylabel   .append( sum(afterquatt[afterquatt['ENERGIELABEL'] == energylabel]['gas_usage_perM2']) / len(afterquatt[afterquatt['ENERGIELABEL'] == energylabel]))   
                co2_emission_perM2_afterQuatt_diffenergylabel.append( sum(afterquatt[afterquatt['ENERGIELABEL'] == energylabel]['co2_emission_perM2']) / len(afterquatt[afterquatt['ENERGIELABEL'] == energylabel]))
                gas_usage_perM2_preQuatt_diffenergylabel     .append( sum(prequatt[prequatt['ENERGIELABEL'] == energylabel]['NATURAL_GAS_perM2']) / len(prequatt[prequatt['ENERGIELABEL'] == energylabel]) )
                co2_emission_perM2_preQuatt_diffenergylabel  .append( sum(prequatt[prequatt['ENERGIELABEL'] == energylabel]['co2_emission_updated_perM2']) / len(prequatt[prequatt['ENERGIELABEL'] == energylabel]) )

        # plot_functions.printresult(afterquatt, nubmer_of_customer_afterQuatt)

        #########
        # plot
        #########
        '''
        # Part 1: usage before/after Quatt
        plot_functions.plot_histogram(100 , afterquatt['gas_usage']         , 'Gas usage per year per house (m^3)'   , 'gas_usage_afterQuatt')
        plot_functions.plot_histogram(0.05, afterquatt['gas_usage_perM2']   , 'Gas usage per year per M2 (m)'        , 'gas_usage_perM2_afterQuatt', 10)  
        plot_functions.plot_histogram(20  , afterquatt['co2_emission']      , 'CO2 emission per year per house (kg)' , 'co2_emission_afterQuatt', 4000)
        plot_functions.plot_histogram(0.5 , afterquatt['co2_emission_perM2'], 'CO2 emission per year per M2 (kg/m^2)', 'co2_emission_perM2_afterQuatt', 40)
        plot_functions.plot_histogram(10  , afterquatt['PROPERTY_DIMENSIONSOFTHEHOUSE'], 'house_area (m^2)'          , 'house_area', 1000)

        plot_functions.plot_histogram(100 , prequatt['NATURAL_GAS']               , 'Gas usage per year per house (m^3)'   , 'gas_usage_preQuatt', 4000)
        plot_functions.plot_histogram(0.05, prequatt['NATURAL_GAS_perM2']         , 'Gas usage per year per M2 (m)'        , 'gas_usage_preM2_preQuatt', 20) 
        plot_functions.plot_histogram(20  , prequatt['co2_emission_updated']      , 'CO2 emission per year per house (kg)' , 'co2_emission_preQuatt', 4000)
        plot_functions.plot_histogram(0.5 , prequatt['co2_emission_updated_perM2'], 'CO2 emission per year per M2 (kg/m^2)', 'co2_emission_perM2_afterQuatt', 40)

        plot_functions.plot_histogram_two_overlap(100,  prequatt['NATURAL_GAS']               , afterquatt['gas_usage'], 'Gas usage per year per house (m^3)', 'gas_usage_together', 'm^3', 3000)
        plot_functions.plot_histogram_two_overlap(0.5,  prequatt['NATURAL_GAS_perM2']         , afterquatt['gas_usage_perM2'], 'Gas usage per year per M2 (m)', 'gas_usage_perM2_together', 'm', 20)
        plot_functions.plot_histogram_two_overlap(150,  prequatt['co2_emission_updated']      , afterquatt['co2_emission'], 'CO2 emission per year per house (kg)', 'co2_emission_together', 'kg', 7000) # first data is alwayse preQuatt
        plot_functions.plot_histogram_two_overlap(0.5,  prequatt['co2_emission_updated_perM2'], afterquatt['co2_emission_perM2'], 'CO2 emission per year per M2 (kg/m^2)', 'co2_emission_perM2_together', 'kg/m^2', 40)
        '''

        # save result
        # df_result['BinCenter_DifferentHouseSize'] = pd.Series(bin_centers).reindex(df_result.index, fill_value=np.nan)
        # df_result['BinCenter_DifferentHouseSize'].loc[8]=500 
        # df_result['EnergyLabels'] = pd.Series(energylabels).reindex(df_result.index, fill_value=np.nan)

        ''' FIXME: It is raw data, not histogram.
        df_result['Gas_Usage_Per_Year_Per_House_AfterQuatt'] = afterquatt['gas_usage']
        df_result['Gas_Usage_Per_Year_Per_House_PreQuatt'] = prequatt['NATURAL_GAS']
        df_result['Gas_Usage_Per_Year_Per_M2_AfterQuatt'] = afterquatt['gas_usage_perM2']
        df_result['Gas_Usage_Per_Year_Per_M2_PreQuatt'] = prequatt['NATURAL_GAS_perM2']
        df_result['CO2_Emission_Per_Year_Per_House_AfterQuatt']    = afterquatt['co2_emission']
        df_result['CO2_Emission_Per_Year_Per_House_PreQuatt']    = prequatt['co2_emission_updated']
        df_result['CO2_Emission_Per_Year_Per_M2_AfterQuatt']    = afterquatt['co2_emission_perM2']
        df_result['CO2_Emission_Per_Year_Per_M2_PreQuatt']    = prequatt['co2_emission_updated_perM2']
        '''

        # df_result['Gas_Usage_Per_Year_Per_M2_AfterQuatt_DifferentHouseSize']    = pd.Series(gas_usage_perM2_afterQuatt_diffhousesize).reindex(df_result.index, fill_value=np.nan) 
        # df_result['Gas_Usage_Per_Year_Per_House_AfterQuatt_DifferentHouseSize'] = pd.Series(gas_usage_perhouse_afterQuatt_diffhousesize).reindex(df_result.index, fill_value=np.nan)
        # df_result['Gas_Usage_Per_Year_Per_M2_PreQuatt_DifferentHouseSize']      = pd.Series(gas_usage_perM2_preQuatt_diffhousesize).reindex(df_result.index, fill_value=np.nan) 
        # df_result['Gas_Usage_Per_Year_Per_House_PreQuatt_DifferentHouseSize']   = pd.Series(gas_usage_perhouse_preQuatt_diffhousesize).reindex(df_result.index, fill_value=np.nan) 
        # df_result['CO2_Emission_Per_Year_Per_M2_AfterQuatt_DifferentHouseSize'] = pd.Series(co2_emission_perM2_afterQuatt_diffhousesize).reindex(df_result.index, fill_value=np.nan)
        # df_result['CO2_Emission_Per_Year_Per_M2_PreQuatt_DifferentHouseSize']   = pd.Series(co2_emission_perM2_preQuatt_diffhousesize).reindex(df_result.index, fill_value=np.nan)

        # df_result['Gas_Usage_Per_Year_Per_M2_AfterQuatt_DifferentEnergyLabel'] = pd.Series(gas_usage_perM2_afterQuatt_diffenergylabel).reindex(df_result.index, fill_value=np.nan)
        # df_result['Gas_Usage_Per_Year_Per_M2_PreQuatt_DifferentEnergyLabel'] = pd.Series(gas_usage_perM2_preQuatt_diffenergylabel).reindex(df_result.index, fill_value=np.nan)
        # df_result['CO2_Emission_Per_Year_Per_M2_AfterQuatt_DifferentEnergyLabel']    = pd.Series(co2_emission_perM2_afterQuatt_diffenergylabel).reindex(df_result.index, fill_value=np.nan)
        # df_result['CO2_Emission_Per_Year_Per_M2_PreQuatt_DifferentEnergyLabel']    = pd.Series(co2_emission_perM2_preQuatt_diffenergylabel).reindex(df_result.index, fill_value=np.nan)

        '''
        # different house size
        plot_functions.plot_proerty_diffhousesize(bin_centers,  gas_usage_perM2_preQuatt_diffhousesize, 'house size (m^2)', 'gas usage per year per m^2', 'gas_usage_perM2_preQuatt_diffhousesize.png')
        plot_functions.plot_proerty_diffhousesize(bin_centers,  co2_emission_perM2_preQuatt_diffhousesize, 'house size (m^2)', 'co2 emission per year per m^2', 'co2_emission_perM2_preQuatt_diffhousesize.png')
        plot_functions.plot_proerty_diffhousesize(bin_centers,  gas_usage_perM2_afterQuatt_diffhousesize, 'house size (m^2)', 'gas usage per year per m^2', 'gas_usage_perM2_afterQuatt_diffhousesize.png')
        plot_functions.plot_proerty_diffhousesize(bin_centers,  co2_emission_perM2_afterQuatt_diffhousesize, 'house size (m^2)', 'co2 emission per year per m^2', 'co2_emission_perM2_afterQuatt_diffhousesize.png')

        plot_functions.plot_proerty_diffhousesize_two_overlap(bin_centers, gas_usage_perM2_preQuatt_diffhousesize, gas_usage_perM2_afterQuatt_diffhousesize, 'house size (m^2)', 'Gas usage per year per M2 (m)', 'gas_usage_perM2_together_diffhousesize.png')
        plot_functions.plot_proerty_diffhousesize_two_overlap(bin_centers, co2_emission_perM2_preQuatt_diffhousesize, co2_emission_perM2_afterQuatt_diffhousesize, 'house size (m^2)', 'co2 emission per year per m^2', 'co2_emission_perM2_together_diffhousesize.png')
        plot_functions.plot_proerty_diffhousesize_two_overlap(bin_centers, gas_usage_perhouse_preQuatt_diffhousesize, gas_usage_perhouse_afterQuatt_diffhousesize, 'house size (m^2)', 'Gas usage per year per house (m)', 'gas_usage_perHouse_together_diffhousesize.png')
        '''

        '''
        # different energylable
        plot_functions.plot_property_diffenergylabel(energylabels, gas_usage_perM2_preQuatt_diffenergylabel     , number_of_customer_diffenergylabel, energylabels, 'Energy Labels', 'gas usage per year per m^2', 'gas_usage_perM2_preQuatt_diffenergylabel.png')
        plot_functions.plot_property_diffenergylabel(energylabels, gas_usage_perM2_afterQuatt_diffenergylabel   , number_of_customer_diffenergylabel, energylabels, 'Energy Labels', 'gas usage per year per m^2', 'gas_usage_perM2_afterQuatt_diffenergylabel.png')
        plot_functions.plot_property_diffenergylabel(energylabels, co2_emission_perM2_preQuatt_diffenergylabel  , number_of_customer_diffenergylabel, energylabels, 'Energy Labels', 'co2 emission per year per m^2', 'co2_emission_perM2_preQuatt_diffhousesize.png')
        plot_functions.plot_property_diffenergylabel(energylabels, co2_emission_perM2_afterQuatt_diffenergylabel, number_of_customer_diffenergylabel, energylabels, 'Energy Labels', 'co2 emission per year per m^2', 'co2_emission_perM2_afterQuatt_diffhousesize.png')

        plot_functions.plot_statistics_housesize(bin_centers, houselabels, number_of_customer_diffenenthousesize)
        plot_functions.plot_statistics_energylabels(energylabels, number_of_customer_diffenergylabel)
        '''

        #plot_functions.SankeyDiagram(afterquatt)


        # Part 2: usage during day

        # plot_functions.plot_usage_during_day(aggrgate_during_day_10mins, 'time_slot', 'avg_gas_usage'        , 'Average Gas Usage (m^3)'        , 'average_gas_usage_during_day'        , monthname)
        # plot_functions.plot_usage_during_day(aggrgate_during_day_10mins, 'time_slot', 'avg_co2_emission'     , 'Average CO2 Emission (kg)'      , 'average_co2_emission_during_day'     , monthname)
        plot_functions.plot_usage_during_day(aggrgate_during_day_10mins, 'time_slot', 'avg_electricity_usage', 'Average Electricity Usage (kWh)', 'average_electricity_usage_during_day', monthname)

        # plot_functions.plot_usage_during_day(aggrgate_during_day_hourly, 'time_slot_hourly', 'avg_gas_usage'        , 'Average Gas Usage (m^3)'        , 'average_gas_usage_during_day_hourly'        , monthname)
        # plot_functions.plot_usage_during_day(aggrgate_during_day_hourly, 'time_slot_hourly', 'avg_co2_emission'     , 'Average CO2 Emission (kg)'      , 'average_co2_emission_during_day_hourly'     , monthname)
        # plot_functions.plot_usage_during_day(aggrgate_during_day_hourly, 'time_slot_hourly', 'avg_electricity_usage', 'Average Electricity Usage (kWh)', 'average_electricity_usage_during_day_hourly', monthname)

        # plot_functions.plot_usage_during_year(data_resampled, 'avg_gas_usage',         '', 'Average Gas Usage (m^3)'        , 'average_gas_usage_during_year')
        # plot_functions.plot_usage_during_year(data_resampled, 'avg_electricity_usage', '', 'Average Electricity Usage (kWh)', 'average_electricity_usage_during_year')
        # plot_functions.plot_usage_during_year(data_resampled, 'avg_co2_emission',      '', 'Average CO2 Emission (kg)'      , 'average_co2_emission_during_year')


        # df_result['DuringTheDay_10mins_Avg_Gas_Usage_M3_' + monthname] = aggrgate_during_day_10mins['avg_gas_usage']
        # df_result['DuringTheDay_10mins_Avg_CO2_Emission_kWh_' + monthname] = aggrgate_during_day_10mins['avg_co2_emission'] 
        # df_result['DuringTheDay_10mins_Avg_Electricity_Usage_kg' + monthname] = aggrgate_during_day_10mins['avg_electricity_usage'] 

        '''
        if monthname == '10_2023_to_03_2024' or '01_2024_to_01_2025':
            df_result['DuringTheDay_1hour_Avg_Gas_Usage_M3_' + monthname] = aggrgate_during_day_hourly['avg_gas_usage']
            df_result['DuringTheDay_1hour_Avg_Electricity_Usage_kWh_' + monthname] = aggrgate_during_day_hourly['avg_electricity_usage']
            df_result['DuringTheDay_1hour_CO2_Emission_kg_' + monthname] = aggrgate_during_day_hourly['avg_co2_emission']

        if monthname == '01_2024_to_01_2025':
            df_result['Avg_Gas_Usage_M3_1day_' + monthname]          = data_resampled['avg_gas_usage'] 
            df_result['Avg_Electricity_Usage_kWh_1day_' + monthname] = data_resampled['avg_electricity_usage']
            df_result['Avg_CO2_Emission_kg_1day_' + monthname]       = data_resampled['avg_co2_emission']
        '''
 
    # print(df_result.keys())
    # df_result.to_excel('../Results/result.xlsx')

if __name__ == "__main__":
    main()




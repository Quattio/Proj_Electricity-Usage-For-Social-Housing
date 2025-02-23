import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plot_functions
import sys
import os
import utility


def prepare(prequatt, data, data_during_day, data_electricity_usage_year, data_electricity_usage_heatingseason):

    data_electricity_usage_year = data_electricity_usage_year.dropna()
    data_electricity_usage_heatingseason = data_electricity_usage_heatingseason.dropna()

    prequatt = prequatt.dropna()
    data = data.merge(prequatt[['DEAL_ID', 'ENERGIELABEL']], left_on='OBJECTID', right_on='DEAL_ID', how='left')
    data.drop(columns=['DEAL_ID'], inplace=True)

    data_during_day['interval_time'] = pd.to_datetime(data_during_day['interval_time'])

    data_during_day['time_slot'] = data_during_day['interval_time'].dt.strftime('%H:%M:%S')
    data_during_day['time_slot_hourly'] = data_during_day['interval_time'].dt.strftime('%H:00:00')

    aggrgate_during_day_10mins = data_during_day.groupby('time_slot').agg({
        'activeCIC': 'mean',
        'avg_gas_usage': 'mean',
        'avg_co2_emission': 'mean',
        'avg_electricity_usage': 'mean'
    }).reset_index()

    aggrgate_during_day_hourly = data_during_day.groupby('time_slot_hourly').agg({
        'activeCIC': 'mean',  
        'avg_gas_usage': 'sum',  
        'avg_co2_emission': 'sum',  
        'avg_electricity_usage': 'sum'  
    }).reset_index()

    data_during_day.set_index('interval_time', inplace=True)
    data_resampled = data_during_day.resample('1D').agg({
        'activeCIC': 'mean',  
        'avg_gas_usage': 'sum', 
        'avg_co2_emission': 'sum',  
        'avg_electricity_usage': 'sum'  
    }).reset_index()

    return prequatt, data, data_resampled, aggrgate_during_day_10mins, aggrgate_during_day_hourly


def calculations(data, prequatt, housebins, houselabels):
    nubmer_of_customer_afterQuatt = len(data)
    number_of_prequatt = len(prequatt)

    #print("nubmer_of_customer_afterQuatt: " + str(nubmer_of_customer_afterQuatt))
    #print("prequatt: " + str(number_of_prequatt))

    data['HOUSESIZE_CATEGORY'] = pd.cut(data['PROPERTY_DIMENSIONSOFTHEHOUSE'], bins=housebins, labels=houselabels, right=False)
    prequatt['HOUSESIZE_CATEGORY'] = pd.cut(prequatt['AREA'], bins=housebins, labels=houselabels, right=False)

    data['gas_usage']          = data['Q_CV'] / 1000 / 8.8 # Wh -> kWh -> m^3
    data['gas_usage_perM2']    = data['Q_CV'] / 1000 / 8.8 / data['PROPERTY_DIMENSIONSOFTHEHOUSE']
    data['electricity_usage']  = (data['E_HP1'] + data['E_HP2']) / 1000 # kWh
    data['co2_emission']       = data['Q_CV'] / 1000 / 8.8 * 1.788  + (data['E_HP1'] + data['E_HP2']) * 0.272 / 1000  # in kg
    data['co2_emission_perM2'] = (data['Q_CV'] / 1000 / 8.8 * 1.788  + (data['E_HP1'] + data['E_HP2']) * 0.272 / 1000) / data['PROPERTY_DIMENSIONSOFTHEHOUSE']

    prequatt['NATURAL_GAS_perM2'] = prequatt['NATURAL_GAS'] / prequatt['AREA']
    prequatt['co2_emission_updated'] = prequatt['NATURAL_GAS'] * 1.788 + prequatt['ELECTRICITY'] * 0.638 * 0.272 # 63.8% is the percentage of heat usage of all electricity usage for Dutch family 
    prequatt['co2_emission_updated_perM2'] = prequatt['co2_emission_updated']/prequatt['AREA']



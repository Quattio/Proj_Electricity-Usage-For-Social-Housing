import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os


def printwelcome():
    print("\n")
    print("#" * 69)
    print("#" + " " * 12 + "\033[1mWelcome to Fleet Performance KPIs Analysis!\033[0m" + " " * 12 + "#")
    print("#" * 69)
    print("\n")

def ending():
    print("\n")
    print("#" * 69)
    print("#" + " " * 12 + "\033[1mEnd of Fleet Performance KPIs Analysis. Good Bye!\033[0m" + " " * 6 + "#")
    print("#" * 69)
    print("\n")


def LoadRawData():

    datafilename = ""

    # EmployeeHeatPumpData
    #datafilename = "../Data/EmployeeHeatPump/EmployeeHeatPump.csv"

    print("#" * 69)
    print("\033[1;31mStart Loading Raw Data:\033[0m")
    df_load = pd.read_csv(datafilename)
    print("\033[32mTotal Number of CiC Records: \033[35m" + str(len(df_load)) + "\033[0m")
    print("\033[32mTotal Number of Unique CiCs: \033[35m" + str(len(df_load['clientid'].unique())) + "\033[0m")
    print("\033[32mStart of collecting data: \033[35m" + str(min(df_load['time_ts'])) + "\033[0m")
    print("\033[32mEnd of collecting data: \033[35m" + str(max(df_load['time_ts'])) + "\033[0m")
    print("#" * 69)
    print('\n')

    return df_load


def excutefilters(df_load, filter_list, general_filters):
    for filter_name in filter_list:
        filter_function = getattr(general_filters, filter_name, None)

        if callable(filter_function):
            number_before_filter = len(df_load)
            filter_function(df_load)
            print("\033[36m" + str(filter_name) + str(" Pass Ratio: \033[35m") + f"{len(df_load)/number_before_filter*100:.2f}" + "%")
        else:
            print(f"Filter '{filter_name}' doesn't exist.")

def applyfilters(df_load, FilterList, filters, filters_sector_name):
    RawRecordNumber = len(df_load)
    print("#" * 69)
    print("\033[1;31m" + filters_sector_name + ":" + "\033[0m")    

    excutefilters(df_load, FilterList, filters)

    print("\033[32mTotal Pass Ratio: \033[35m" + f"{len(df_load) / RawRecordNumber * 100:.2f} %" +  "\033[0m")
    print("#" * 69)     
    print("\n")


def check_quality(df):
    print("#" * 69)
    print("\033[1;31mStart Quality Check:\033[0m")
    print("\033[32mTotal Number of Analysed CiC Records: \033[35m" + str(len(df)) + "\033[0m")
    print("\033[32mTotal Number of Analysed Unique CiCs: \033[35m" + str(len(df['clientid'].unique())) + "\033[0m")
    nan_counts = df.isnull().sum()
    nan_columns = nan_counts[nan_counts > 0]
    
    if not nan_columns.empty:
        error_message = "\033[32mData quality check: \033[35m" + "DataFrame contains NaN values.\033[0m\n"
        error_message += "\033[32mNaN counts by column:\033[0m\n"  
        for column, count in nan_columns.items():
            error_message += f" \033[36m- {column}\033[0m: \033[35m{count} NaN values\033[0m\n" 
        print(error_message)
    else:
        print("\033[32mData quality check passed: No NaN values found.\033[0m")  
    print('\n')
    print("#" * 69)

def CheckBinXY(x, y):
    if len(x) != len(y):
        print("x axis has length:" + str(len(x)))
        print("y axis has length:" + str(len(y)))
        raise ValueError(f"\033[31mBin Numbers Check: X and Y axis have different dimentions.\033[0m\n")

def custom_floor(ts, start_time, freq_minutes):
    delta = (ts - start_time).total_seconds() // (freq_minutes * 60)
    return start_time + pd.Timedelta(minutes=delta * freq_minutes)

def UnvertToKelvin(inputColumn):
    return inputColumn + 273.15

def MergeWindow(df_load, cic, MergeWindow, fleet_start_time, fleet_end_time, freqvalue):

    ## Check if there is any MergeWindow has no data 
    # prepare
    df_load_original = df_load

    # Find merged window without record out of range
    all_hours               = pd.date_range(start = fleet_start_time, end=fleet_end_time, freq=freqvalue)

    grouping_Result = pd.Series(0, index=all_hours)  
    for i in range(len(all_hours) - 1):
        mask = (df_load['time_ts'] >= all_hours[i]) & (df_load['time_ts'] < all_hours[i + 1])
        grouping_Result[all_hours[i]] = df_load.loc[mask].shape[0]

    timewindow_with_records = grouping_Result.index
    missingcount_outside_dataTaking = all_hours.difference(timewindow_with_records)
    half_freq = pd.Timedelta(freqvalue) / 2
    missingcount_outside_dataTaking_center = missingcount_outside_dataTaking + half_freq

    # Find merged window with "One or Zero" record in the range
    missingcount_within_dataTaking  = (grouping_Result == 0).sum()
    onecount_within_dataTaking      = (grouping_Result == 1).sum()
    missingcount_within_dataTaking_TimeIndex = grouping_Result[grouping_Result == 0].index
    onecount_within_dataTaking_TimeIndex     = grouping_Result[grouping_Result == 1].index
    missingcount_within_dataTaking_PositionIndex = grouping_Result.index.get_indexer(missingcount_within_dataTaking_TimeIndex) 
    onecount_within_dataTaking_PositionIndex     = grouping_Result.index.get_indexer(onecount_within_dataTaking_TimeIndex)
    totalPositionIndex = list(missingcount_within_dataTaking_PositionIndex) + list(onecount_within_dataTaking_PositionIndex)
 
    # Drop the record (only for one record case)  #FIXME
    df_load_min = df_load['time_ts'].min().normalize()
    df_load_filtered_records = df_load[df_load['time_ts'].apply(custom_floor, args=(df_load_min, MergeWindow)).isin(onecount_within_dataTaking_TimeIndex)].copy()
    df_load = df_load[~df_load.index.isin(df_load_filtered_records.index)].copy()

    # Get Index for MergeWindow Bin Edge (right bin edge in each merged time window?)
    df_load.loc[:, 'time_bin'] = pd.cut(df_load['time_ts'], bins=all_hours, right=False)

    MergeWindow_BinEdge = ( df_load.groupby('time_bin', observed=False).apply(lambda x: x.index[-1] if not x.empty else None).dropna())
    if len(MergeWindow_BinEdge)>0:
        MergeWindow_BinEdge = MergeWindow_BinEdge.tolist()
    else:
        MergeWindow_BinEdge = []
    MergeWindow_BinEdge.insert(0, 0)

    # Get BinCenter
    # Remember "Timestamp.floor('7200min')" starts from 1970-01-01 00:00:00.
    start_time = fleet_start_time

    end_time = fleet_end_time

    start_time_half = start_time + pd.Timedelta(minutes=MergeWindow/2)
    end_time_half = end_time + pd.Timedelta(minutes=MergeWindow/2) 

    BinCenterForMergeWindow = pd.date_range(start=start_time_half, end=end_time_half, freq=freqvalue)
    BinCenterForMergeWindow = pd.Series(BinCenterForMergeWindow)

    # Drop the BinCenterForMergeWindow for MergeWindow with zero or just one record inside
    BinCenterForMergeWindow = BinCenterForMergeWindow.drop(  totalPositionIndex ).reset_index(drop=True)
    BinCenterForMergeWindow = BinCenterForMergeWindow[~BinCenterForMergeWindow.isin(missingcount_outside_dataTaking_center)].reset_index(drop=True)

    return MergeWindow_BinEdge, BinCenterForMergeWindow, df_load  



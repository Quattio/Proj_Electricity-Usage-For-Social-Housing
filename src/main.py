import argparse
import math
import time
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import Filters
import Utility.Plot_Functions as Plot_function
import Utility.UtilityFunctions as UtilityFunctions

def main():


    ## Load data
    df_load = UtilityFunctions.LoadRawData()

    ## Filters
    # Genral Filters 
    generalfilterList = ['FilterOnTestRigs', 'FilterOnInactiveCiC', 'FilterOnDropZero', 'FilterOnDropABit', 'FilterOnIncreaseCounter', 'FilterOnAllNull'] 
    UtilityFunctions.applyfilters(df_load, generalfilterList, Filters.GeneralFilters, filters_sector_name='General Filters')
    # Check Data Quality: Nan Value
    UtilityFunctions.check_quality(df_load)


    ## Preparation
    df_load['time_ts'] = pd.to_datetime(df_load['time_ts'], utc=True)
    BinCenterForMergeWindow_allCiC_RespectiveBins= []
    MergeWindow = 1440 # 60: hourly, 1440: daily, 5 days:7200, 43200:monthly (30 days) 
    freqvalue = str(MergeWindow) + 'min'
    fleet_start_time = df_load['time_ts'].min().normalize()
    fleet_end_time_max = df_load['time_ts'].max()
    fleet_end_time = pd.date_range(start = fleet_start_time, end = fleet_end_time_max, freq=freqvalue).max()
    BinCenterForMergeWindow_WholeTimeRange = pd.Series(pd.date_range(start = fleet_start_time + pd.Timedelta(minutes=MergeWindow/2), end=fleet_end_time + pd.Timedelta(minutes=MergeWindow/2), freq=freqvalue))
    final_ciclist = []
    print("\033[1;31mMerged Time Window is: \033[35m" + str(freqvalue) + "\033[0m")


    ## Loop for CiC 
    raw_ciclist = df_load['clientid'].unique()
    total_cic = len(raw_ciclist)
    for cic_idx, cic in enumerate(raw_ciclist):

        # print CiC progress status
        current_segment = (cic_idx + 1) * 10 // total_cic
        if current_segment > (cic_idx * 10 // total_cic):
            print(f"\033[36mCurrent process: " + "\033[35m" + f"{current_segment * 10}" + "%\033[36m CiC\033[0m")

        # get one CiC
        df_OneCiC = df_load[df_load['clientid'] == cic].copy() 
        df_OneCiC = df_OneCiC.reset_index(drop=True)

        # get the BinEdge for online data， AND drop record if there is only one record in a merged window
        # BinEdge is the last record index in each Merge Window
        MergeWindow_BinEdge, BinCenterForMergeWindow, df_OneCiC = UtilityFunctions.MergeWindow(df_OneCiC, cic, MergeWindow, fleet_start_time, fleet_end_time, freqvalue)
        UtilityFunctions.CheckBinXY(MergeWindow_BinEdge[1:], BinCenterForMergeWindow)

        # if there is only one record for this CiC, we just skip this one.
        if len(df_OneCiC) <= 1 or len(BinCenterForMergeWindow)<1:
            continue 
        BinCenterForMergeWindow_allCiC_RespectiveBins.append(BinCenterForMergeWindow)

        ##########################
        # Add your Analysis here #
        ##########################    

        # add cic list
        final_ciclist.append(cic) 

    #######################
    # Save the KPI Retuls #
    #######################

if __name__ == "__main__":
    UtilityFunctions.printwelcome()
    start_time = time.time()
    main()
    print(f"\n\033[1;31mProgram runtime: {(time.time() - start_time) / 60:.4f} minutes\033[0m")
    UtilityFunctions.ending()


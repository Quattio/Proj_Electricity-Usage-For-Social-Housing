#! /usr/bin/env python3

# Example Useage: python Plot.py --inputCSCfile CIC-87845a22-3d04-5f8c-8d4e-c1e735a9e472   

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import QuattDataLoader.Utility.PythonPlotDefaultParameters
import datetime
import QuattDataLoader.Clickhouse.Utility_ClickHouse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputCSCfile', help='Input CSC file to be loaded.', default=None)
    arguments = parser.parse_args()

    loaddata = pd.read_csv(arguments.inputCSCfile)
    timestamps = loaddata['Date']
    times = pd.to_datetime(timestamps, utc=True)


    QuattDataLoader.Clickhouse.Utility_ClickHouse.PlotMatrix(times, loaddata, 1, len(loaddata.columns))
    #QuattDataLoader.Clickhouse.Utility_ClickHouse.Plot(times, loaddata['ActiveClientID'], 'ActiveClientID', 'ActiveClientID')  

if __name__ == '__main__':
    main()





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 17:05:38 2022

@author: vivianliu
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as dt
import glob
from pathlib import Path
#Purpose of this function is to take OMNI data at one hour intervals and convert it to
#one minute intervals

#Function takes an input filepath and an output filepath as parameters
#Returns a dataframe of inputted data at one minute intervals
#Also creates a csv file with cleaned data
def read_OMNI_1HR(input_path, output_path):
    print("Start OMNI 1HR")
    files = os.path.join(input_path, "OMNI*.csv")
    #Combine OMNI files
    files = glob.glob(files)

    #Create dataframe with all OMNI files
    df = pd.concat(map(pd.read_csv, files), ignore_index = True)
    
    #Convert first column to datetime
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], format = "%Y-%m-%dT%H:%M:%S.%fZ")
    df.columns.values[0] = "Datetime"
    
    #Duplicate each data value by 60 so that the hour intervals can be redistributed to minute intervals
    df = pd.concat([df]*60, ignore_index=True)
    
    #Sort the data by date
    df.index = df["Datetime"]
    df = df.sort_index()

    #Create string values for the start and end date to use in date_range function
    start_date = str(df["Datetime"].iloc[0].year) + "-" +  str(df["Datetime"].iloc[0].month) + "-" + str(df["Datetime"].iloc[0].day)\
+ " " + str(df["Datetime"].iloc[0].hour) + ":" + str((df["Datetime"].iloc[0].minute - 30)) + ":" + str(df["Datetime"].iloc[0].second)

    end_date = str(df["Datetime"].iloc[len(df) - 1].year) + "-" +  str(df["Datetime"].iloc[len(df) - 1].month) + "-" + str(df["Datetime"].iloc[len(df) - 1].day)\
+ " " + str(df["Datetime"].iloc[len(df) - 1].hour) + ":" + str((df["Datetime"].iloc[len(df) - 1].minute + 29)) + ":" + str(df["Datetime"].iloc[len(df) - 1].second)

    #Convert hour intervals to minutes while making all values of each minute interval the value taken at that hour
    df["Datetime"] = pd.date_range(start = start_date, freq = "T", periods = len(df))
    
    df = df.reset_index(drop = True)
    print(df)
    
    df.to_csv(output_path, index = False)
    
    print("OMNI 1HR finished")
    
    return df




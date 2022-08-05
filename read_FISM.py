#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 17:12:49 2022

@author: vivianliu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as dt

#Purpose of this function is to clean FISM data so it can be combined with other 
#solar and geomagnetic indice data

#Function takes an input filepath and an output filepath as parameters
#Returns a dataframe with the cleaned data at one minute intervals
#Also creates a csv file with clean data
def read_fism(input_path, output_path):
    print("Start FISM")
    
    df = pd.read_csv(input_path)
    df["Datetime"] = pd.to_datetime(df["time (yyyyDDD)"], format = "%Y%j")
    df = df.drop("time (yyyyDDD)", axis = 1)
    
    #Use reindex to fill in any missing days and create a new dataframe with all dates as index
    new_date_range = pd.date_range(start = df["Datetime"].iloc[0], end = df["Datetime"].iloc[len(df) - 1], freq="D")
    df2 = df.reindex(new_date_range)
    
    #Drop all the columns in the dataframe leaving the datetime index
    df2 = df2.drop(df2.iloc[:,0:], axis = 1)

    #Make a new column called datetime with datetime index
    df2["Datetime"] = df2.index
    
    #Merge original dataframe with new reindexed dataframe
    #how = "left" to keep Datetime values of df2
    df = df2.merge(df, how="left", on = "Datetime")

    #Copy each row 1440 times for 1440 minutes in a day
    df = pd.concat([df]*1440, ignore_index=True)
    
    #Sort the dataframe by date
    df.index = df["Datetime"]
    df = df.sort_index()
    
    #Set start date for starting minute intervals
    start_date = str(df["Datetime"].iloc[0].year) + "-" +  str(df["Datetime"].iloc[0].month) + "-" + str(df["Datetime"].iloc[0].day)\
        +  " " + str(df["Datetime"].iloc[0].hour - 12) + ":" + str(df["Datetime"].iloc[0].minute) + ":" + str(df["Datetime"].iloc[0].second)
    
    #end_date = str(df["Datetime"].iloc[len(df) - 1].year) + "-" + str(df["Datetime"].iloc[len(df) - 1].month) + "-" + str(df["Datetime"].iloc[len(df) - 1].day)\
     #   + " " + str(df["Datetime"].iloc[len(df) - 1].hour + 11) + ":" + str((df["Datetime"].iloc[len(df) - 1].minute) + 59) + ":" + str(df["Datetime"].iloc[len(df) - 1].second)
        
    #Turn the time intervals to 1 minute intervals
    df.index = pd.date_range(start = start_date, freq = "T", periods = len(df))
    
    #Replace Datetime columns with new 1 minute interval times
    df = df.drop("Datetime", axis = 1)
    df["Datetime"] = df.index
    
    df.to_csv(output_path, index = False)
    
    print("FISM finished")
    
    return df


#read_fism("/Users/vivianliu/Documents/NASA_data/fism_daily_hr.csv", "/Users/vivianliu/Documents/NASA_data/fism_cleaned.csv")






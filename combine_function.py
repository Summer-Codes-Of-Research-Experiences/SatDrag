#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 22:08:04 2022

@author: vivianliu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as dt
import glob
from pathlib import Path

#Function takes either a string filepath or dataframe from the read OMNI or read_GRACE_CHAMP
#as its first two arguments and a string output file path as the third argument. 
#It merges the two datasets together on the datetime column and saves it in a csv file at the given filepath
#The function returns the merged dataframe
def combine(output_filepath, *args):
    print("Start combine")      
    if (type(args[0]) == pd.core.frame.DataFrame):
        merged_df = args[0]
    elif (type(args[0]) == str):
        merged_df = pd.read_csv(args[0])
        
    merged_df["Datetime"] = merged_df["Datetime"].astype("datetime64[ns]")

    for element in args[1:]:
        if (type(element) == pd.core.frame.DataFrame):
            df2 = element
        elif (type(element) == str):
            df2 = pd.read_csv(element)
        df2["Datetime"] = df2["Datetime"].astype("datetime64[ns]")
        merged_df = pd.merge(merged_df, df2, on = "Datetime", how = "outer")
        
    print(merged_df)
    
    #Convert datetime to separate numerical columns
    merged_df["year"] = merged_df["Datetime"].dt.year
    merged_df["month"] = merged_df["Datetime"].dt.month
    merged_df["day"] = merged_df["Datetime"].dt.day
    merged_df["hour"] = merged_df["Datetime"].dt.hour
    merged_df["minute"] = merged_df["Datetime"].dt.minute
    merged_df["second"] = merged_df["Datetime"].dt.second

    #Drop datetime column to avoid datetime type error
    merged_df.sort_values(by = ["Datetime"])
    print(merged_df)
   # merged_df = merged_df.drop("Datetime", axis = 1)
    
    #Remove any rows with NaN values
    print(merged_df)
    merged_df = merged_df.dropna(axis = 0, how = "any")
    print(merged_df)
    
    merged_df.to_csv(output_filepath, index = False)
    
    print("Combine finished")
    
    return merged_df

#Function has same purpose as combine function but keeps a datetime column
def combine_wdatetime(output_filepath, *args):
    print("Start combine")      
    if (type(args[0]) == pd.core.frame.DataFrame):
        merged_df = args[0]
    elif (type(args[0]) == str):
        merged_df = pd.read_csv(args[0])
        
    merged_df["Datetime"] = merged_df["Datetime"].astype("datetime64[ns]")

    for element in args[1:]:
        if (type(element) == pd.core.frame.DataFrame):
            df2 = element
        elif (type(element) == str):
            df2 = pd.read_csv(element)
        df2["Datetime"] = df2["Datetime"].astype("datetime64[ns]")
        merged_df = pd.merge(merged_df, df2, on = "Datetime", how = "outer")
        
    #Drop datetime column to avoid datetime type error
    merged_df.sort_values(by = ["Datetime"])
    
    #Remove any rows with NaN values
    merged_df = merged_df.dropna(axis = 0, how = "any")
    
    merged_df.to_csv(output_filepath, index = False)
    
    print("Combine finished")
    
    return merged_df

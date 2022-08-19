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

#Function takes multiple data files or dataframes and combines them into one dataframe
#Parameters:
    #output_filepath: a filepath to store a csv file of the resulting dataframe
    #*args: takes a variable number of parameters in the form of either a filepath or dataframe
#Return: Function returns a dataframe of all the input data combined. 
#Function also creates a csv file of the resulting dataframe at the inputted output filepath
def combine(output_filepath, *args):
    print("Start combine")      
    #Create dataframe using first input in the *args list
    if (type(args[0]) == pd.core.frame.DataFrame):
        merged_df = args[0]
    elif (type(args[0]) == str):
        merged_df = pd.read_csv(args[0])
    
    #Convert Datetime column to datetime type
    merged_df["Datetime"] = merged_df["Datetime"].astype("datetime64[ns]")

    #For loop combines all the rest of the input arguments with the first dataframe
    for element in args[1:]:
        #Create a second dataframe from current input based on format
        if (type(element) == pd.core.frame.DataFrame):
            df2 = element
        elif (type(element) == str):
            df2 = pd.read_csv(element)
        #Convert Datetime columns to datetime type
        df2["Datetime"] = df2["Datetime"].astype("datetime64[ns]")
        #Merge newly created dataframe with the original dataframe
        merged_df = pd.merge(merged_df, df2, on = "Datetime", how = "outer")
        
    
    #Create separate numerical columns with datetime values
    merged_df["year"] = merged_df["Datetime"].dt.year
    merged_df["month"] = merged_df["Datetime"].dt.month
    merged_df["day"] = merged_df["Datetime"].dt.day
    merged_df["hour"] = merged_df["Datetime"].dt.hour
    merged_df["minute"] = merged_df["Datetime"].dt.minute
    merged_df["second"] = merged_df["Datetime"].dt.second

    #Drop datetime column to avoid datetime type error
    merged_df.sort_values(by = ["Datetime"])
    
    #Remove any rows with NaN values
    merged_df = merged_df.dropna(axis = 0, how = "any")

    #Createa a csv file with combined data
    merged_df.to_csv(output_filepath, index = False)
    
    print("Combine finished")
    
    return merged_df

#Function has same purpose as combine function but doesn't create new columns for individual datetime values
def combine_wdatetime(output_filepath, *args):
    print("Start combine")      
    if (type(args[0]) == pd.core.frame.DataFrame):
        merged_df = args[0]
    elif (type(args[0]) == str):
        merged_df = pd.read_csv(args[0])
        
    merged_df["Datetime"] = merged_df["Datetime"].astype("datetime64[ns]")

    #Merge all input data
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 14:42:49 2022

@author: vivianliu
"""

import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

#This function takes an input folder path and an output csv filepath as parameters
#It returns a dataframe of all the files concatenated together
#Also creates a csv file with cleaned data
def read_MSIS (input_path, output_path):
    print("Start MSIS")
    
    files = os.path.join(input_path, "MSIS*.csv")
    #Combine MSIS files
    files = glob.glob(files)

    #Create dataframe with all OMNI files
    df = pd.concat(map(pd.read_csv, files), ignore_index = True)
    
    #Set date column to datetime type
    df["Datetime"] = pd.to_datetime(df["Datetime"], format = "%Y-%m-%d %H:%M:%S")
    
    df = df[["Datetime", "Total mass density"]]
    
    #Sort dataframe values by date
    df = df.sort_values(by = "Datetime")
    
    df.to_csv(output_path, index = False)
    
    print("MSIS finished")
    
    return df
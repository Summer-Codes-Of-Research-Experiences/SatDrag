#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 21:51:52 2022

@author: vivianliu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as dt
import glob
from pathlib import Path

#Function takes an input GRACE or CHAMP data folder path and an output filepath as parameters
#It creates a csv data file at the given output file location and returns the resulting dataframe
def read_grace_champ(input_path, output_filepath):
    print("Start GRACE/CHAMP")
    #Specifies columns widths in document
    colspecs = colspecs=[(0,2), (3,6), (7,15), (16,19), (20,29), (30, 40), (41, 48), (49, 56), (57, 66), (67, 77), (78, 85), (86, 98), (99, 111), (112, 124), (125, 137), (138, 150), (151, 153), (154, 156), (157, 162)]

    #Creates filepath to folder with files
    file_path = Path(input_path)

    #Initializes dataframe
    df = pd.DataFrame()

    #Concatenates data from all files
    df =  pd.concat([pd.read_fwf(i, skiprows = 2, header = None, colspecs = colspecs, converters={0:str,1:str}) for  i in file_path.glob('Density*.ascii')], ignore_index = True)
    #Sets column names
    df.columns = ["Year","DOY","Sec","CLat","SLat","SLon","Height","STime","DipLat","MagLon","MagTime","Density","400kmDensity","410kmDensity","DensityHeight","DenUncertainty","NuminBin","NuminBinThrusters","AveDragCoef"]


    #Year and day to string
    df["datetime"] = df["Year"].map(str) + "-" + df["DOY"].map(str)
    #Year and date to datetime object type

    df["datetime"] = pd.to_datetime(df["datetime"], format = "%y-%j")
    #Add the time onto date and convert to datetime
    df["datetime"] = [(df["datetime"].iloc[i] + pd.Timedelta(seconds = df["Sec"].iloc[i])) for i in range(len(df))]
    df["datetime"] = pd.to_datetime(df["datetime"])

    df = df.groupby("datetime").mean().reset_index()

    #the index equal to datetime
    df.index = df["datetime"]
    df.index.name = None
    df = df.sort_index(axis = 0)

    #Plots data before resampling and interpolation
    plt.plot(df["datetime"], df["Density"], label = "pre")
    plt.scatter(df["datetime"], df["Density"], label = "pre", s = 0.75)
    plt.xlim(df["datetime"].iloc[35000], df["datetime"].iloc[39000])

    #Create resample index intervals of 1 minute
    resample_index = pd.date_range(start=df.index[0] - pd.Timedelta(seconds = df["Sec"].iloc[0]), end=df.index[-1] + pd.Timedelta(seconds = (60 - df["Sec"].iloc[0])), freq='1Min')
    #Create dummy frame with NaN values in the resample indices
    dummy_frame = pd.DataFrame(np.NaN, index=resample_index, columns=df.columns)
    #Combine dummy frame with original dataframe
    df = df.combine_first(dummy_frame).sort_index()

    #Remove duplicated indices for resampling
    #df = df[~df.index.duplicated(keep='first')]
    #Interpolate and resample data into 1 minute intervals
    df = df.interpolate(method = 'pad', limit = 2).resample('1Min').asfreq()

    #Plots data after resampling and interpolation
    plt.plot(df["datetime"], df["Density"], label = "post", c = "orange")
    plt.legend(loc = "upper right")
    plt.show()

    #Add on numerical indices
    df.reset_index(inplace = True)
    #Set first column name to "Datetime"
    df = df.rename(columns = {"index":"Datetime"})
    df = df[df.Density <= 1e-11]
    df = df.drop("datetime", axis = 1)
    
    df.to_csv(output_filepath, index = False)
    
    print("GRACE/CHAMP finished")
    
    return df
    
    
    
    
    
    
    
    
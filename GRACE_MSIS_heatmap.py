#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:18:54 2022

@author: vivianliu
"""

import pandas as pd
import numpy as np
import seaborn as sns


#Purpose: Create a heatmap of the input features against the difference between GRACE and MSIS densities
#Function takes a input filepath or a dataframe as a parameter
### NOTE: Data must already contain cleaned GRACE and MSIS data
#Does not have a return value but creates a heatmap of each feature against the
#difference between GRACE and MSIS densities

def create_heatmap(data):
    if (type(data) == pd.core.frame.DataFrame):
        df = data;
    elif (type(data) == str):
        df = pd.read_csv(data)
        
    #Create column for the difference between GRACE and MSIS densities
    df["Difference"] = df["Total mass density"] - df["400kmDensity"]
    
    #Plot graphs of  indicies (uncomment for plot)
    """
    fig, axes = plt.subplots(nrows = 9, ncols = 1, sharex = True)
    
    df.plot(x = 'Datetime', y = 'SYM/H_INDEX_nT', ax = axes[0], ylabel = 'Sym-H', legend=False)
    df.plot(x = 'Datetime', y = '3-H_KP*10_', ax = axes[1], ylabel = 'KP', legend=False)
    df.plot(x = 'Datetime', y = 'DAILY_F10.7_', ax = axes[2], ylabel = 'f10.7', legend=False)
    df.plot(x = 'Datetime', y = '1-M_AE_nT', ax = axes[3], ylabel = 'AE', legend=False)
    df.plot(x = 'Datetime', y = '3-H_AP_nT', ax = axes[4], ylabel = 'AP', legend=False)
    df.plot(x = 'Datetime', y = 'SOLAR_LYMAN-ALPHA_W/m^2', ax = axes[5], ylabel = 'Solar Lyman Alpha', legend=False)
    df.plot(x = 'Datetime', y = 'mg_index (core to wing ratio (unitless))', ax = axes[6], ylabel = 'Mg II', legend=False)
    df.plot(x = 'Datetime', y = 'irradiance (W/m^2/nm)', ax = axes[7], ylabel = 'Irridance', legend=False)
    df.plot(x = 'Datetime', y = 'Difference', ax = axes[8], ylabel = 'Difference', legend=False)
    """
    
    df_min = df["Difference"].min()
    df_max = df["Difference"].max()
    
    step = (df_max - df_min) / 20
    #Create bins based on difference values while averaging all other variables
    df = df.groupby(pd.cut(df["Difference"], np.arange(df_min, df_max, step))).mean()
    
    #Normalize all the values
    df = (df-df.mean())/df.std()
    
    #Name x-axis
    df.index.names = ["4GRACE/MSIS Difference Ranges (kg/m^3)"]
    
    #Drop initial difference column
    df = df.drop("Difference", axis = 1)
    
    #Store feature names in a series
    columns = df.columns
    
    #Transpose dataframe
    df = df.transpose()
    
    
    #Create heatmap
    plot = sns.heatmap(df, cmap = "Blues", annot = False, yticklabels = columns)
    
    plot.set_ylabel('Input Variables', fontsize=10)
    plot.set_title("Average Normalized Values of Solar and Geomagnetic\nIndices Against GRACE/MSIS Density Differences\n", fontsize = 13)


    
    
    
    
    
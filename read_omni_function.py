#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 21:21:33 2022

@author: vivianliu
"""

import pandas as pd
import numpy as np
import os
import glob


#Function takes path of input data folder, path of file to be outputted to, 
#a boolean to remove bad values, and a percentage threshold as parameters

#It creates a csv data file at the specified output filepath and returns
#the output filepath
def read_omni(input_path, output_filepath, remove_bad = True, percentage = 0.25):
    print("Start OMNI")
    files = os.path.join(input_path, "OMNI*.csv")
    #Combine OMNI files
    files = glob.glob(files)

    #Create dataframe with all OMNI files
    df_sw = pd.concat(map(pd.read_csv, files), ignore_index = True)

    #Set time column to datetime
    df_sw.iloc[:,0] = pd.to_datetime(df_sw.iloc[:,0], format='%Y-%m-%dT%H:%M:%S.%fZ')

    #Rename column to "Datetime" for easier access
    df_sw.rename(columns = {'EPOCH_TIME_yyyy-mm-ddThh:mm:ss.sssZ':"Datetime"}, inplace = True)


    #Replace bad values with NaN
    df_sw = df_sw.replace([999.99], [np.nan])
    df_sw = df_sw.replace([9999.99], [np.nan])
    df_sw = df_sw.replace([99999.9], [np.nan])
    df_sw = df_sw.replace([99.99], [np.nan])
    df_sw = df_sw.replace([1.00000e+07], [np.nan])
    
    #Remove columns with frequent bad values
    if (remove_bad == True): 
        df_sw = df_sw.dropna(thresh=(1-percentage)*len(df_sw), axis=1)

    #Create a csv file with cleaned data
    df_sw.to_csv(output_filepath, index = False)
    
    print("OMNI finished")
    
    return output_filepath

    
    
    
    
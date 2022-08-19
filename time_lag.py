#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 01:05:32 2022

@author: vivianliu
"""

import pandas as pd
#This function takes a cleaned dataframe and returns a timelag analysis

#Parameters:
    #data: input dataframe either in filepath or dataframe format
    #lag: integer time in minutes of lag
    #features (optional): list of which features to perform analysis on
#Return: Features along with their r-sqaured correlation values for the timelag

def time_correlation(data, lag, features = all):
    print("Start time lag: ", lag, " minutes")
    #Convert inputted data to dataframe format
    if (type(data) == pd.core.frame.DataFrame):
        df = data;
    elif (type(data) == str):
        df = pd.read_csv(data)
    
    #Create a list with the features that analysis will be performed on
    if (type(features) == list):
        using_features = ["Datetime"]
        for element in features:
            using_features.append(element)
    #Create a list with all the features
    else:
        using_features = data.columns
        
    #Set the dataframe to one with only the features for the timelag
    df = df[using_features]
    
    #Sort the dataframe by datetime and remove the index
    df = df.sort_values(by = "Datetime")
    df = df.reset_index(drop=True)
    
    #Create a new dataframe that is a copy of the current dataframe
    #Used as the lagging dataset
    df1 = df
    
    #Drop the datetime column from both dataframes
    df1 = df1.drop("Datetime", axis = 1)
    df = df.drop("Datetime", axis = 1)
    
    #Reduce the initial dataframe length by number of minutes of lag
    df = df.iloc[0: -lag]
    #Push back second dataframe by number of minutes of lag
    df1 = df1.iloc[lag:]
    
    #Reset the index of the new dataframe
    df1 = df1.reset_index(drop=True)

    #Create list of the correlations between the two dataframes
    correlation = df.corrwith(df1, axis = 0)
    
    print(correlation)



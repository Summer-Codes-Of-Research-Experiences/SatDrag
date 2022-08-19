#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:43:45 2022

@author: vivianliu
"""
import pandas as pd

#Function adds the gradient of each row as a separate column in the original dataframe
#Parameters:
    #data: cleaned data input in the form of a filepath or dataframe
    #target: target feature that is going to be used in the machine learning model
    #features (optional): the features that user wants the gradient of
#Return: A dataframe with all the original columns and new gradient columns
def create_gradient(data, target,features = all):
    print("Start gradient")
    #Create dataframe based on input format
    if (type(data) == pd.core.frame.DataFrame):
        df = data
    elif (type(data) == str):
        df = pd.read_csv(data)
        
    ###Save unchanged columns (datetime and target variable)##
    df_date = df["Datetime"]
    df_target = df[target]
    #Dataframe to hold all individual datetime columns
    df_datetime = df[["year", "month", "day", "hour", "minute", "second"]]
    
    #Drop datetime from original dataframe
    df = df.drop(["Datetime", target], axis = 1)
    
    #Create a new dataframe that stores the difference between each row and row before
    df2 = df.diff()
    
    #Get rid of any features in the new dataframe that user doesn't want the gradient of
    if (features != all):
        df2 = df2[features]
    
    #Add the target and datetime columns back to the original dataframe
    df["Datetime"] = df_date
    df[target] = df_target
    df[["year", "month", "day", "hour", "minute", "second"]] = df_datetime
    
    #Create a list to hold new gradient column names
    new_columns = []
    #Add the new gradient column names to newly created list
    for element in df2.columns:
        new_columns.append(element + "_diff")
    
    #Rename the columns of gradient dataframe
    df2.columns = new_columns
    
    #Create a datetime columns for gradient dataframe with original datetime for merging
    df2["Datetime"] = df_date
    
    #Merge the original dataframe and the gradient dataframe
    df = df.merge(df2, on = "Datetime", how = "outer")
    
    #Drop any bad values
    df = df.dropna(axis = 0, how = "any")
    
    print("Finished gradient")
    
    return df

#Function creates a dataframe with the gradient values of specified features
#Parameters:
    #data: cleaned data input in the form of a filepath or dataframe
    #target: target feature that is going to be used in the machine learning model
    #features (optional): the features that user wants the gradient of
#Return: A dataframe with only original datetime and target variable columns and gradient columns
def only_gradient(data, target, features = all):
    if (type(data) == pd.core.frame.DataFrame):
        df = data
    elif (type(data) == str):
        df = pd.read_csv(data)
        
    ###Save unchanged columns (datetime and target variable)##
    df_date = df["Datetime"]
    df_target = df[target]
    df_datetime = df[["year", "month", "day", "hour", "minute", "second"]]
    
    #Drop datetime from original dataframe
    df = df.drop(["Datetime", target], axis = 1)
    
    #Create a new dataframe that stores the difference between each row and row before
    df2 = df.diff()
    
    #Get rid of any features in the new dataframe that user doesn't want the gradient of
    if (features != all):
        df2 = df2[features]
    
    #Create a list to hold new gradient column names
    new_columns = []
    #Add the new gradient column names to newly created list
    for element in df2.columns:
        new_columns.append(element + "_diff")
    
    #Rename gradient dataframe columns
    df2.columns = new_columns
    
    #Add the original datetime and target variables to new dataframe
    df2["Datetime"] = df_date
    df2[target] = df_target
    df2[["year", "month", "day", "hour", "minute", "second"]] = df_datetime
    
    #Drop any rows with bad values
    df = df2.dropna(axis = 0, how = "any")
    
    print("Finished gradient")
    
    return df



    

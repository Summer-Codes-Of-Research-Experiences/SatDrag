#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:19:54 2022

@author: vivianliu
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as dt
import glob
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score

#This function takes data and runs a random forest regressor on it
#Parameters
#   data: a data frame or string pathname type
#   target_variable: string with target variable name
#   features (optional): takes a list type with the names of all the variables to include. Default is all
#   estimators (optional): integer for number of estimators in random forest. Default is 150
#   rdm_state (optional): integer for random state of random forest regression. Defult is 16
#   test_portion (optional): float between 0 and 1 for proportion of data used for test. Default is 0.25
#   plot: boolean input indicating whether or not to plot the prediction and true data. Default is False
#Returns:
#   Does not return a value. Prints out measurements of accuracy as well as feature importances
def run_random_forest(data, target_variable, features = all, drop_features = None, estimators = 150, rdm_state = 16, test_portion = 0.25, plot = False):
    print("Start random forest")
    if (type(data) == pd.core.frame.DataFrame):
        merged_df = data;
    elif (type(data) == str):
        merged_df = pd.read_csv(data)
    
    merged_df = merged_df[~(merged_df["Datetime"] < '2002-05-01')]
    
    merged_df = merged_df.drop("Datetime", axis = 1)
    
    #Set target and feature variables
    target = merged_df[target_variable]
    target = target*(10**12)
    merged_df = merged_df.drop(target_variable, axis = 1)

    features_list = list(merged_df.columns)
    
    #Adjust features being used based on user input
    if (features == all):
        features_list = features_list
    elif (type(features) == list):
        using_features = ["year", "month", "day", "hour", "minute", "second"]
        for element in features:
            using_features.append(element)
        features_list = using_features
    
    
    print(features_list)
    
    merged_df = merged_df[features_list]
    print(merged_df)
    
    if (drop_features != None):
        merged_df = merged_df.drop(drop_features, axis = 1)
        for element in drop_features:
            features_list.remove(element)
    
    #Set training and testing groups
    train_features, test_features, train_target, test_target = train_test_split(merged_df, target, test_size = test_portion, random_state = rdm_state)

    #Train model

    rf = RandomForestRegressor(n_estimators = estimators, random_state = rdm_state)
    rf.fit(train_features, train_target)

    #Make predictions and calculate error
    predictions = rf.predict(test_features)

    mean_abs_error = mean_absolute_error(test_target, predictions)
    print("\nMean Absolute Error: ", mean_abs_error, " kg/m^3.")

    #Fit metrics
    mape = mean_absolute_percentage_error(test_target, predictions)
    print("Mean Absolute Percentage Error: ", mape)
    score = r2_score(test_target, predictions)

    print("Score: ", score)

    #Examine feature importances
    importances = list(rf.feature_importances_)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(features_list, importances)]
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]
    
    #
    #
    #Plot Data
    #
    #
    if (plot == True):
        #Create arrays for datetime data
        months = merged_df.iloc[:, features_list.index('month')]
        days = merged_df.iloc[:, features_list.index('day')]
        years = merged_df.iloc[:, features_list.index('year')]
        hours = merged_df.iloc[:, features_list.index('hour')]
        minutes = merged_df.iloc[:, features_list.index('minute')]
        seconds = merged_df.iloc[:, features_list.index('second')]
    
        #Convert datetime arrays to datetype type
        dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) + " " + str(int(hour)) + ":" + str(int(minute)) + ":" + str(int(second)) for year, month, day, hour, minute, second in zip(years, months, days, hours, minutes, seconds)]
        dates = [dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]
    
        #Create dataframe using datetime and target data
        true_data = pd.DataFrame(data = {'date': dates, 'actual': target})
        true_data = true_data.sort_values(by = "date")
        true_data["actual"] = true_data["actual"] / (10**12)
    
        months = test_features.iloc[:, features_list.index('month')]
        days = test_features.iloc[:, features_list.index('day')]
        years = test_features.iloc[:, features_list.index('year')]
        hours = test_features.iloc[:, features_list.index('hour')]
        minutes = test_features.iloc[:, features_list.index('minute')]
        seconds = test_features.iloc[:, features_list.index('second')]
    
        test_dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) + " " + str(int(hour)) + ":" + str(int(minute)) + ":" + str(int(second)) for year, month, day, hour, minute, second in zip(years, months, days, hours, minutes, seconds)]
        test_dates = [dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in test_dates]
    
        #Make a new dataframe with prediction data
        prediction_data = pd.DataFrame(data = {"dates": test_dates, "predictions": predictions})
        prediction_data = prediction_data.sort_values(by = "dates")
        prediction_data["predictions"] = prediction_data["predictions"] / (10**12)
    
        plt.plot(true_data["date"], true_data["actual"], "b-", label = "actual")
    
        plt.plot(prediction_data["dates"], prediction_data["predictions"], "mo", label = "predicted", markersize = 3)
    
    
        #plt.xlim(true_data["date"].iloc[25000], true_data["date"].iloc[26500])
        plt.xticks(rotation = 60)
        plt.xlabel("Date")
        plt.ylabel("400 km Density")
        plt.title("Actual and Predicted Values of\nRandom Forest for 400km Density")
        plt.legend()
    
    
    
    
    
    
    
    
    
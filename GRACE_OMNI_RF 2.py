#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 10:16:05 2022

@author: vivianliu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as dt
from datetime import datetime, timedelta
from time import strftime
from time import gmtime
import glob
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import r2_score

#
#
###  READ IN SOLAR WIND DATA  ###
#
#

#Import all OMNI files
files = os.path.join("/Users/jayden/Downloads/OMNI_data_files", "OMNI_HRO_1MIN*.csv")
#Combine OMNI files
files = glob.glob(files)

#Create dataframe with all OMNI files
df_sw = pd.concat(map(pd.read_csv, files), ignore_index = True)

#Set time column to datetime
df_sw['EPOCH_TIME_yyyy-mm-ddThh:mm:ss.sssZ'] = pd.to_datetime(df_sw['EPOCH_TIME_yyyy-mm-ddThh:mm:ss.sssZ'], format='%Y-%m-%dT%H:%M:%S.%fZ')

#Rename column to "Datetime" for easier access
df_sw.rename(columns = {'EPOCH_TIME_yyyy-mm-ddThh:mm:ss.sssZ':"Datetime"}, inplace = True)

#Remove columns with frequent bad values
print("Initial sw shape: ", df_sw.shape)
df_sw = df_sw.drop("BZ__GSE_nT", axis = 1)
df_sw = df_sw.drop("VX_VELOCITY__GSE_km/s", axis = 1)
df_sw = df_sw.drop("FLOW_SPEED__GSE_km/s", axis = 1)
df_sw = df_sw.drop("PROTON_DENSITY_n/cc", axis = 1)
df_sw = df_sw.drop("TEMPERATURE_K", axis = 1)
df_sw = df_sw.drop("FLOW_PRESSURE_nPa", axis = 1)
df_sw = df_sw.drop("ELECTRIC_FIELD_mV/m", axis = 1)

#Remove rows with bad data values
"""
df_sw = df_sw[df_sw["BZ__GSE_nT"] < 9000.99]
df_sw = df_sw[df_sw["FLOW_SPEED__GSE_km/s"] < 90000.9]
df_sw = df_sw[df_sw["VX_VELOCITY__GSE_km/s"] < 90000.9]
df_sw = df_sw[df_sw["PROTON_DENSITY_n/cc"] < 900.99]
df_sw = df_sw[df_sw["TEMPERATURE_K"] < 9000000.0]
df_sw = df_sw[df_sw["FLOW_PRESSURE_nPa"] < 90.99]
df_sw = df_sw[df_sw["ELECTRIC_FIELD_mV/m"] < 900.99]


#Replace bad values with NaN
df_sw = df_sw.replace([999.99], [np.nan])
df_sw = df_sw.replace([9999.99], [np.nan])
df_sw = df_sw.replace([99999.9], [np.nan])
df_sw = df_sw.replace([99.99], [np.nan])
df_sw = df_sw.replace([1.00000e+07], [np.nan])
"""

print("After remove columns: ", df_sw.shape)

#
#
###  READ IN GRACE DENSITY DATA  ###
#
#

#Specifies columns widths in document
colspecs = colspecs=[(0,2), (3,6), (7,15), (16,19), (20,29), (30, 40), (41, 48), (49, 56), (57, 66), (67, 77), (78, 85), (86, 98), (99, 111), (112, 124), (125, 137), (138, 150), (151, 153), (154, 156), (157, 162)]

#Creates filepath to folder with files
file_path = Path("/Users/jayden/Downloads/GRACE_B_data_files")

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

#plt.plot(df["datetime"], df["Density"], label = "pre")
#plt.scatter(df["datetime"], df["Density"], label = "pre", s = 0.75)
#plt.xlim(df["datetime"].iloc[35000], df["datetime"].iloc[39000])

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

#plt.plot(df["datetime"], df["Density"], label = "post", c = "orange")
#plt.legend(loc = "upper right")
#plt.show()

#Add on numerical indices
df.reset_index(inplace = True)
#Set first column name to "Datetime"
df = df.rename(columns = {"index":"Datetime"})
df = df[df.Density <= 1e-11]
df = df.drop("datetime", axis = 1)


#
#
###  COMBINE SOLAR WIND AND DENSITY DATA INTO ONE DATAFRAME  ###
#
#

merged_df = pd.merge(df_sw, df, on = "Datetime", how = "outer")

#Extract individual date and time values from datetime data

merged_df["year"] = merged_df["Datetime"].dt.year
merged_df["month"] = merged_df["Datetime"].dt.month#.strftime("%m"))
merged_df["day"] = merged_df["Datetime"].dt.day#.strftime("%d"))
merged_df["hour"] = merged_df["Datetime"].dt.hour#.strftime("%H"))
merged_df["minute"] = merged_df["Datetime"].dt.minute#.strftime("%M"))
merged_df["second"] = merged_df["Datetime"].dt.second#.strftime("%S"))


#df['datetime'] = df['datetime'].map(dt.datetime.toordinal)

#Drop datetime column to avoid datetime type error
merged_df = merged_df.sort_values(by = ["Datetime"])
merged_df = merged_df.drop("Datetime", axis = 1)
print("merged df shape: ", merged_df.shape)

#Remove any rows with NaN values
merged_df = merged_df.dropna(axis = 0, how = "any")
print("after nan dropped: ", merged_df.shape)

#plt.plot(df["datetime"], df["Density"], label = "post", c = "orange")
#plt.legend(loc = "upper right")
#plt.show()
#
#
### Random Forest Regressor ###
#
#

#Set target value and features
target = np.array(merged_df["Density"])
merged_df = merged_df.drop("Density", axis = 1)

features_list = list(merged_df.columns)

#df = np.array(merged_df)

#Set training and testing groups
train_features, test_features, train_target, test_target = train_test_split(merged_df, target, test_size = 0.2, random_state = 19)


#Train model

rf = RandomForestRegressor(n_estimators = 150, random_state = 19)
rf.fit(train_features, train_target)

print(rf)
print(train_features)
print(train_target)

#Make predictions and calculate error
predictions = rf.predict(test_features)
print(predictions)
errors = abs(predictions - test_target)
mean_absolute_error = np.mean(errors)
score = r2_score(test_target, predictions)

print("Mean Absolute Error: " + str(mean_absolute_error) + " kg/m^3.")
print("Score: ", score)

#Accuracy calculation
mape = 100 * (errors / test_target)
accuracy = round(100 - np.mean(mape), 3)

print("Accuracy: " + str(accuracy) + "%")

#Examine feature importances
importances = list(rf.feature_importances_)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(features_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

#
#
#New random forest using only more used features
#
#
new_rf = RandomForestRegressor(n_estimators  = 150, random_state = 19)

used_features = [features_list.index("SYM/H_INDEX_nT"), features_list.index("STime"), features_list.index("SLat"), features_list.index("Height"), features_list.index("month"), features_list.index("day"), features_list.index("hour"), features_list.index("minute"), features_list.index("second")]

#Set new training and testing features
train_important = train_features.iloc[0:, used_features]
test_important = test_features.iloc[0:, used_features]


#Fit new features
new_rf.fit(train_important, train_target)

#Make new predictions
predictions = new_rf.predict(test_important)

#New errors
error = abs(predictions - test_target)
mape = np.mean(100 * (error / test_target))
accuracy = 100 - mape
score = r2_score(test_target, predictions)

print("Mean Absolute Error: ",np.mean(error), " kg/m^3.")
print("Score: ", score)
print('Accuracy:', round(accuracy, 2), '%.')


importances = list(new_rf.feature_importances_)
feature_importances = [(features_list[feature], round(importance, 2)) for feature, importance in zip(used_features, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

#
#
#Plot Data
#
#

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

#Create dataframe using 
true_data = pd.DataFrame(data = {'date': dates, 'actual': target})


months = test_features.iloc[:, features_list.index('month')]
days = test_features.iloc[:, features_list.index('day')]
years = test_features.iloc[:, features_list.index('year')]
hours = test_features.iloc[:, features_list.index('hour')]
minutes = test_features.iloc[:, features_list.index('minute')]
seconds = test_features.iloc[:, features_list.index('second')]

test_dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) + " " + str(int(hour)) + ":" + str(int(minute)) + ":" + str(int(second)) for year, month, day, hour, minute, second in zip(years, months, days, hours, minutes, seconds)]
test_dates = [dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in test_dates]

print(true_data.shape)
prediction_data = pd.DataFrame(data = {"dates": test_dates, "predictions": predictions})

plt.plot(true_data["date"], true_data["actual"], "b-", label = "actual", markersize = 0.5)

plt.plot(prediction_data["dates"], prediction_data["predictions"], "mo", label = "predicted", markersize = 3)


#plt.xlim(true_data["date"].iloc[25000], true_data["date"].iloc[26500])
plt.xticks(rotation = 60)
plt.legend()

























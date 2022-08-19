#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:29:57 2022

@author: vivianliu
"""
from read_omni_function import *
from read_GRACE_CHAMP_function import *
from combine_function import *
from run_random_forest_function import *
from read_OMNI_1HR import *
from read_FISM import *
from read_mgii import *
from gradient import *
from read_MSIS import *
from gradient_booster import *
import sklearn

grace_data_filepath = "/Users/vivianliu/Documents/NASA_data/GRACE_B_data_files"
omni_data_filepath = "/Users/vivianliu/Documents/NASA_data/OMNI_data_files"
OMNI_1HR_filepath = "/Users/vivianliu/Documents/NASA_data/OMNI_1HR_data_files"
mgii_input_path = "/Users/vivianliu/Documents/NASA_data/composite_mg_index.csv"
fism_input_path = "/Users/vivianliu/Documents/NASA_data/fism_daily_hr.csv"
msis_input_path = "/Users/vivianliu/Documents/NASA_data/MSIS_data_files"

omni_output_filepath = "/Users/vivianliu/Documents/NASA_data/random_forest_files/modified_omni_all.csv"
grace_output_filepath = "/Users/vivianliu/Documents/NASA_data/random_forest_files/modified_grace_all.csv"
OMNI_1HR_output_filepath = "/Users/vivianliu/Documents/NASA_data/random_forest_files/modified_OMNI_1HR_all.csv"
mgii_output_filepath = "/Users/vivianliu/Documents/NASA_data/random_forest_files/modified_mgii.csv"
fism_output_filepath = "/Users/vivianliu/Documents/NASA_data/random_forest_files/fism_cleaned.csv"
msis_output_filepath = "/Users/vivianliu/Documents/NASA_data/random_forest_files/msis_cleaned_all.csv"

combined_output_filepath = "/Users/vivianliu/Documents/NASA_data/random_forest_files/combined_data_all.csv"

#using_features = ["irradiance (W/m^2/nm)", "STime", "MagTime", "SYM/H_INDEX_nT", "Height", "DAILY_F10.7_", "3-H_AP_nT", "3-H_KP*10_", "mg_index (core to wing ratio (unitless))", \
#                  "SOLAR_LYMAN-ALPHA_W/m^2", "SLat", "AveDragCoef"]

using_features = ["irradiance (W/m^2/nm)", "MagTime","SLat", "SYM/H_INDEX_nT", "1-M_AE_nT", "3-H_KP*10_"]

dropping = ["year", "hour", "minute", "second"]
"""
df1 = read_omni_index(omni_data_filepath, omni_output_filepath)

df2 = read_grace_champ(grace_data_filepath, grace_output_filepath)

df2 = df2.drop(["Density", "410kmDensity"], axis = 1)

df3 = read_OMNI_1HR(OMNI_1HR_filepath, OMNI_1HR_output_filepath)

df4 = read_mgii(mgii_input_path, mgii_output_filepath)

df5 = read_fism(fism_input_path, fism_output_filepath)

df6 = read_MSIS(msis_input_path, msis_output_filepath)

combined_df = combine(combined_output_filepath, df1, df2, df3, df4, df5, df6)
""" 
#combined_df = create_gradient(combined_df, "400kmDensity", features = using_features)
#combined_df["constant"] = 1

run_random_forest("/Users/vivianliu/Documents/NASA_data/random_forest_files/combined_data_all_reduced_omni.csv", "400kmDensity", features = using_features, drop_features = dropping, test_portion = 0.25, plot = True)

#run_gradient_boost("/Users/vivianliu/Documents/NASA_data/random_forest_files/combined_data_all_reduced_omni.csv", "400kmDensity", features = using_features, drop_features = dropping, test_portion = 0.25, plot = True)
















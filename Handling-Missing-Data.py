#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 09:47:32 2024

@author: abhikvinod
"""
#Importing relevant modules
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
#Inspecting the df
df = pd.read_csv('developer_dataset.csv')
#print(df.head())
print(df.info())
print(df.describe())
#Removing Variables with more than 60% of Data Missing
df_len = len(df)
missing_d = (1-(df.count()/df_len)) * 100
#print(missing_d)
df.drop(['NEWJobHunt', 'NEWJobHuntResearch', 'NEWLearn'], axis = 1, inplace = True)
#print(df)
#Looking at Employement and Developer Type from Country Perspecrtive
Country_counts = df[['RespondentID', 'Country']].groupby('Country').count()
print(Country_counts)
#List of countries with UK and US abreviations
country_list = []
def rename(x):
    if x  == 'United Kingdom':
        x = 'UK'
    elif x  == 'United States':
        x = 'UK'
    else:
        x = x
    return x
df['Country'] = df.Country.apply(lambda x: rename(x))
missing_d_countries = df[['Employment','DevType']].isnull().groupby(df['Country']).sum().reset_index()
#print(missing_d_countries)
fig = plt.figure(figsize = (13, 8))
ax = plt.subplot(1,2,1)
plt.bar(data = missing_d_countries, x= 'Country', height = 'Employment')
plt.xticks(rotation = 35)
ax.set_xticklabels(country_list)
plt.ylabel('Count of Missing Employment Data')
plt.xlabel('Country')
ax = plt.subplot(1,2,2)
plt.bar(data = missing_d_countries, x= 'Country', height = 'DevType')
plt.subplots_adjust(wspace = 0.5)
plt.xticks(rotation = 35)
plt.ylabel('Count of Missing DevType Data')
plt.xlabel('Country')
plt.suptitle('Missing Data for Both DevType and Employment')
plt.show()
plt.clf()
#From Graphs above and the table of variable counts, it is clear that missing data scales with data inputs of country so data is is presumed to be MCAR.
#remove null values from Columns
df.dropna(subset = ['DevType', 'Employment'], inplace = True, how = 'any')
print(df['Employment'].value_counts())
#Renaming Observations in Employment Variable
def reduce_words(x):
    lower = x.lower()
    if 'full' in lower:
        x = 'Full'
    elif 'part' in lower:
        x = 'Part'
    elif 'self' in lower:
        x = 'Self'
    elif 'but' in lower:
        x = 'NE & L'
    elif 'and' in lower:
        x = 'NE 7 NL'
    else:
        x = 'Retired'
    return x

df['Employment'] = df.Employment.apply(lambda x: reduce_words(x))
#Creating Seperate Employment Data Frames
Employmentdf_Dict = {}
Employments = df['Employment'].value_counts().index
for i in Employments:
    dummy = df[df.Employment == i]
    Employmentdf_Dict[i] = dummy

#Employment_counts = df[['Employment', 'Country']].groupby('Country').count()
def multiplot(dictionary):
    count = 1
    fig = plt.figure(figsize = (40, 20))
    for i, j in dictionary.items():
        Employment_counts = j[['Employment', 'Country']].groupby('Country').count()
        ax = plt.subplot(1, len(dictionary), count)
        plt.bar(x = Employment_counts.index, height = Employment_counts.Employment)
        plt.title(f'Employment Type: {i}')
        plt.xlabel('Country')
        plt.ylabel('Count of Employment Type')
        plt.xticks(rotation = 35)
        count += 1
    plt.subplots_adjust(wspace = 1)
    plt.suptitle('The Variation in Different Types of Employment Across a few Various Countries')
    plt.show()
plt.clf()
#Plotting Employment for various different countries
multiplot(Employmentdf_Dict)
#Repeat Process Above for DevType
DevType_df_Dict = {}
DevTypes = df['DevType'].value_counts().index
for i in DevTypes:
    dummy = df[df.DevType == i]
    DevType_df_Dict[i] = dummy

#Employment_counts = df[['Employment', 'Country']].groupby('Country').count()
def multiplot2(dictionary):
    count = 1
    fig = plt.figure(figsize = (40, 20))
    for i, j in dictionary.items():
        DevType_counts = j[['DevType', 'Country']].groupby('Country').count()
        plt.subplot(1, len(dictionary), count)
        plt.bar(x = DevType_counts.index, height = DevType_counts.DevType)
        plt.title(f'Dev Type: {i}')
        plt.xlabel('Country')
        plt.ylabel('Count of Dev Type')
        plt.xticks(rotation = 35)
        count += 1
    plt.subplots_adjust(wspace = 1)
    plt.suptitle('The Variation in Different Types of Developers Across a few Various Countries')
    plt.show()
    plt.clf()
#Plotting, Error with plot but not sure why arising
#multiplot2(DevType_df_Dict)

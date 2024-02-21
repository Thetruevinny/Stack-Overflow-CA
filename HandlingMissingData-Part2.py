#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:38:31 2024

@author: abhikvinod
"""
#Importing relevant modules
import pandas as pd
import matplotlib.pyplot as plt
#Investigating undergrad
#First Look into missing Data
df = pd.read_csv('developer_dataset.csv')
missing_ug = df['UndergradMajor'].isnull().groupby(df['Year']).sum().reset_index()
ax = plt.subplot(1,1,1)
plt.bar(x = missing_ug.Year, height = 'UndergradMajor', data = missing_ug)
ax.set_xticks([2018, 2019, 2020])
plt.show()
plt.clf()
#We can see all the people surveyed answered the major question inb 2020. This seems to indicate we can backfill the data with the 2020 variables.
df = df.sort_values(['RespondentID', 'Year'])
df['UndergradMajor'].bfill(axis=0, inplace = True)
def clean_up(x):
    lower = x.lower()
    if ('computer' in lower) or ('development' in lower) or ('engineering' in lower) or ('information' in lower):
        x = 'Eng/CompSci'
    elif 'mathematics' in lower:
        x = 'Maths'
    elif 'natural' in lower:
        x = 'Natural Science'
    elif ('social' in lower) or ('health' in lower):
        x = 'Social/Health Science'
    elif ('humanities' in lower) or ('arts' in lower):
        x = 'Humanities/Arts'
    elif 'business' in lower:
        x = 'Business'
    elif 'never' in lower:
        x = 'Not Declared'
    return x
df.dropna(subset = ['UndergradMajor'], inplace = True)
df['UndergradMajor'] = df['UndergradMajor'].apply(lambda x: clean_up(x))
Majors = df.UndergradMajor.value_counts().index 
print(Majors)
def multiplot(List):
    count = 1
    fig = plt.figure(figsize = (40,12))
    for i in List:
        sub_df = df[df['UndergradMajor'] == i]
        sub_df = sub_df[['Year', 'UndergradMajor']].groupby('Year').count()
        plt.subplot(1, len(List), count)
        plt.bar(x= sub_df.index, height = sub_df.UndergradMajor)
        plt.xlabel('Years')
        plt.ylabel('Count')
        plt.title(i)
        count += 1
    plt.subplots_adjust(wspace = 1)
    plt.suptitle('How Undergrad Major changes through the Years')
    plt.show()
    plt.clf()
multiplot(Majors)
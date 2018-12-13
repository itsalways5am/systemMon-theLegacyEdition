#######################################################################################################################
## batteryTypecast.py
## purpose : to get .csv data into workable format for EDA and analysis
## last updated: 2018-12-03
## used Jupyter Lab for visual and will likely use for analysis with numpy, matplotlib etc.
## author: luckyducky
#######################################################################################################################

import pandas as pd
import csv
import datetime
import re

d=pd.read_csv('batteryLog.csv')

# drop column "Unnamed:0" # rename d to df for proper "holding" of the drop change
df=d.drop(columns=['Unnamed: 0'])

# add column names # add column names  { }[ ]
df.rename(columns={'0':'Log ID','1':'Log time','2':'Battery supported','3':'Battery detected','4':'Current charge','5':'Battery remaining','6':'Charging status',
             '7':'Plugged in'}, inplace=True)

# type cast log time to datetime # create day of week
s=df['Log time']
df['Log time']= pd.to_datetime(s)

# df['new column name']=df['Log Time'].dt.dayof week
df['Day of Week']=df['Log time'].dt.dayofweek

# Changing values of 'yes','no' and others to a format that is easy to analyse.
# Legend: yes = 1, no = 0, 9999 = full battery, Day of Week: 0=Sun, 1=Mon etc

valuestochange=['yes', 'no', 'unlimited', 'fully charged', 'charging', 'discharging'
                                                                       'BatteryTime.POWER_TIME_UNKNOWN']

# regex replacing items in values to change
for items in valuestochange:
    df=df.replace('yes', "1", regex=True)
    df=df.replace('no', "0", regex=True)
    df=df.replace('unlimited', "9999", regex=True)
    df=df.replace('BatteryTime.POWER_TIME_UNKNOWN', "0", regex=True)

    df=df.replace('fully charged', "+++", regex=True)
    df=df.replace('charging', "++", regex=True)
    df=df.replace('discharging', "+", regex=True)

# more typecasting
# Battery suppoorted, Battery detected,Charging Status, Battery remaining, Plugged to int64 # Current charge to float
df['Battery supported']=df['Battery supported'].astype(int)
df['Battery detected']=df['Battery detected'].astype(int)
df['Current charge']=df['Current charge'].astype(float)
df['Battery remaining']=df['Battery remaining'].astype(int)
df['Plugged in']=df['Plugged in'].astype(int)

# rearrange columns # needs to occur as a "final step" for values to hold changes and rename into new df1
new_index=['Log ID','Log time','Day of Week','Battery supported','Battery detected','Current charge','Battery remaining','Charging status','Plugged in']
df1=df.reindex(new_index, axis=1)

print(df1)
print(df1.dtypes)

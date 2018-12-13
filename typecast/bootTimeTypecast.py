#######################################################################################################################
## disksTypecast.py
## purpose : to get .csv data into workable format for EDA and analysis
## last updated: 2018-12-03
## used Jupyter Lab for visual and will likely use for analysis with numpy, matplotlib etc.
## author: luckyducky
#######################################################################################################################

import pandas as pd
import csv
import datetime

d=pd.read_csv('bootTimeLog.csv')
# drop column "Unnamed:0" # rename d to df for proper "holding" of the drop change
df=d.drop(columns=['Unnamed: 0'])

# change/add header names
df.rename(columns={'0':'Log ID','1':'Log time','2':'OS Details','3':'OS Family','4':'OS Version','5':'OS Release','6':'Boot time'
             }, inplace=True)

# type cast log time to datetime # create day of week
s=df['Log time']
df['Log time']= pd.to_datetime(s)

# generate day of week df['new column name']=df['Log Time'].dt.dayofweek
df['Day of Week']=df['Log time'].dt.dayofweek

# typecast 'Boot time' to datetime
s1=df['Boot time']
df['Boot time']= pd.to_datetime(s1)

# rearrange columns # needs to occur as a "final step" for values to hold changes and rename into new df1
new_index=['Log ID','Log time','Day of Week','Boot time','OS Family','OS Version','OS Release','OS Details']
df1=df.reindex(new_index, axis=1)

# df1.style (optional as this is a new feature of pd and stated as unstable at the moment

print(df1)
print(df1.dtypes)
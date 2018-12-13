#######################################################################################################################
## processesTypecast.py
## purpose : to get .csv data into workable format for EDA and analysis
## last updated: 2018-12-03
## used Jupyter Lab for visual and will likely use for analysis with numpy, matplotlib etc.
## author: luckyducky
#######################################################################################################################

import pandas as pd
import csv
import datetime

d=pd.read_csv('processesLog.csv')
# drop column "Unnamed:0" # rename d to df for proper "holding" of the drop change
df=d.drop(columns=['Unnamed: 0'])

# change/add header names
df.rename(columns={'0':'Log ID','1':'Log time','2':'PID','3':'Parent PID','4':'Process name','5':'% CPU','6':'Priority','7':'% Mem Used','8':'VMS','9':'RSS',
             '10':'User','11':'Path'}, inplace=True)

# type cast log time to datetime # create day of week
s=df['Log time']
df['Log time']= pd.to_datetime(s)
#df['new column name']=df['Log Time'].dt.dayof week
df['Day of Week']=df['Log time'].dt.dayofweek

# rearrange columns # needs to occur as a "final step" for values to hold changes and rename into new df1
new_index=['Log ID','Log time','Day of Week','PID','Parent PID','Process name','% CPU','Priority','% Mem Used','VMS','RSS','User','Path']
df1=df.reindex(new_index, axis=1)

print(df1)
print(df1.dtypes)
print('Now enjoy data analysis time! This is a core aspect!')

# do not use df1.style - it will eat up your computer power! stay away! ahhhh!


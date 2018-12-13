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

d=pd.read_csv('disksLog.csv')
# drop column "Unnamed:0" # rename d to df for proper "holding" of the drop change
df=d.drop(columns=['Unnamed: 0'])

# change header names
df.rename(columns={'0':'Log ID','1':'Log time','2':'Disk name','3':'Disk size','4':'Used memory','5':'Free memory','6':'% Mem used',
             '7':'FileSys','8':'Mount point'}, inplace=True)

# typecast log time to datetime # create day of week
s=df['Log time']
df['Log time']= pd.to_datetime(s)
#df['new column name']=df['Log Time'].dt.dayofweek
df['Day of Week']=df['Log time'].dt.dayofweek

df['% Mem used']=df['% Mem used'].astype(float)

# rearrange columns # needs to occur as a "final step" for values to hold changes and rename into new df1
new_index=['Log ID','Log time','Day of Week','Disk name','Disk size','Used memory','Free memory','% Mem used','FileSys','Mount point']
df1=df.reindex(new_index, axis=1)

print(df1)
print(df1.dtypes)
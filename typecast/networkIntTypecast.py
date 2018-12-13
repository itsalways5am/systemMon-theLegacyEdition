## pnetworkIntTypecast.py (INCOMPLETE)
## purpose : to get .csv data into workable format for EDA and analysis
## last updated: 2018-12-03
## used Jupyter Lab for visual and will likely use for analysis with numpy, matplotlib etc.
## author: luckyducky
#######################################################################################################################

# use df.head() or df.dtypes anytime to check on things

import pandas as pd
import csv
import datetime

d=pd.read_csv('networkIntLogs.csv')
# drop column "Unnamed:0" # rename d to df for proper "holding" of the drop change
df=d.drop(columns=['Unnamed: 0'])

# change/add header names
df.rename(columns={'0':'Log ID','1':'Log time','2':'Interface','3':'Active','4':'Speed(MB)','5':'Duplex','6':'MTU','7':'IncomingBytes',
                   '8':'IncomingPackets','9':'IncomingErrors','10':'IncomingDrops','11':'OutgoingBytes','12':'OutgoingPackets','13':'OutgoingErrors',
                    '14':'OutgoingDrops','15':'IPv4','16':'IPv4_netmask','17':'IPv4_broadcast','18':'IPv4_p2p','19':'IPv6','20':'IPv6_netmask',
                    '21':'IPv6_broadcast', '22':'IPv6_p2p'}, inplace=True)

# type cast log time to datetime # create day of week
s=df['Log time']
df['Log time']= pd.to_datetime(s)
#df['new column name']=df['Log Time'].dt.dayof week
df['Day of Week']=df['Log time'].dt.dayofweek

# 'half - full - unknown' are duplex outputs -> half : 0.5, full : 1.0, unknown : 0.0
# duplex isn't properly changing so will hold off on that for now
valuestochange=['yes', 'no', 'MB', 'unk0wn', 'half', 'full']

# regex replacing items in values to change
for items in valuestochange:
    df=df.replace('yes', "1", regex=True)
    df=df.replace('no', "0", regex=True)
    df=df.replace('MB', "", regex=True)
    df=df.replace('unk0wn', "0.0", regex=True)  # 'unknown' changes to unk0wn during typecasting # may need to modify as I test with duplex data

# typecast from object to float
df['Speed(MB)']=df['Speed(MB)'].astype(float)

## In regards to NaN, I am leavning them alone for now as NaN naturally propogate through arithmetic operations between pandas objects! ##

# rearrange columns # needs to occur as a "final step" for values to hold changes and rename into new df1
new_index=['Log ID','Log time','Day of Week','Interface','Active','Speed(MB)','Duplex','MTU','IncomingBytes','IncomingPackets','IncomingErrors','IncomingDrops',
          'OutgoingBytes','OutgoingPackets','OutgoingErrors','OutgoingDrops','IPv4','IPv4_netmask','IPv4_broadcast','IPv4_p2p','IPv6',
          'IPv6_netmask','IPv6_broadcast','IPv6_p2p']
df1=df.reindex(new_index, axis=1)

print(df1)
print(df1.dtypes)

import json
import pandas as pd
from datetime import datetime
import numpy as np
wallet_set_df = pd.read_csv('static/datasets/main_set.csv')  
token_set_df = wallet_set_df.loc[wallet_set_df['address'] == '0xf50aced0016256bc3aee3b4dca2170c9c8cd3abb'] 
wallet_set_json = wallet_set_df.to_json(orient='records')  #Convert DataFrame to JSON
wallet_set_data = json.loads(wallet_set_json) 
 
#Format Decimal Notation of Amount properly
for i in wallet_set_data:
     i['amount'] = np.format_float_positional(i['amount'],trim='-')


wallet_set_df['ts'] = pd.to_datetime(wallet_set_df['ts']) #Convert Timestamp to a proper datetime format
total_teleports = wallet_set_df['tx'].count()
wallet_teleports_df = wallet_set_df.groupby(pd.Grouper(key='token'))['tx'].count().to_json() #Group Teleports by token
wallet_volume_df = wallet_set_df.groupby(pd.Grouper(key='token'))['amount'].sum().to_json() #Group Teleports by token and volume
 
wallet_teleports_json = json.loads(wallet_teleports_df)
wallet_volume_json = json.loads(wallet_volume_df)

wallet_teleports = []
wallet_volume = []

 #Append to a list
for d in list(wallet_teleports_json.keys()):
     wallet_teleports.append(d)

for d in list(wallet_volume_json.keys()):
     wallet_volume.append(d)

wallet_data = {'token':wallet_teleports,'teleports': list(wallet_teleports_json.values())}
volume_data = {'token':wallet_teleports,'volume': list(wallet_volume_json.values())}
 
data = {'wallet_data': wallet_data, 'volume_data':volume_data, 'wallet_teleports' : wallet_set_data, 'total_teleports' : total_teleports}

print(data['volume_data'])
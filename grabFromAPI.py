import requests
from flask import redirect
from datetime import datetime
import csv
from pathlib import Path
import pandas as pd
import json
import numpy as np

try: 
  response = requests.get('0http://207.244.228.250:56781/get',timeout=10)
except Exception:
  f = open('TestData.json','r')
  data = json.load(f)
  f.close()
  #pass
else:
  data = response.json()

mainData = []

#Create a class to save data to CSV file
class SaveToCSV:
  def __init__(self,netID,tokenID,datasetCSV):
    self.netID = netID
    self.tokenID = tokenID
    self.datasetCSV = datasetCSV 

  def save(self):
   pathCSV = Path('static/datasets/{}.csv'.format(self.datasetCSV))
   header = ['tx','ts','address','amount','type','second_net']
   network= {'4':'Rinkeby','5':'Goerli'}
   token={'0':'FMTA','1':'TUSDTw'}    
   txDeposits = data['data']['network'][self.netID]['deposits'][self.tokenID]
   txWithdrawals = data['data']['network'][self.netID]['withdrawals'][self.tokenID]
  
   #If CSV is not found Create new file
   if pathCSV.is_file() == False:
      with open(pathCSV,'x') as new_file:
          csvwriter = csv.writer(new_file)
          csvwriter.writerow(header)
          new_file.close()

   #Save Data to network_token_CSV
   try:
     #Round amount to 2 decimal points and Timestamp to datetime
     for d in txDeposits:
      d['ts'] = datetime.fromtimestamp(d['ts'])
      d['amount'] = np.format_float_positional(d['amount']/10**17,trim = '-')
      d['type'] = 'Deposit'
      d['token'] = token['{}'.format(d['token'])]
      d['first_net'] = network['{}'.format(d['sourceNet'])]
      d['second_net'] = network[self.netID]
        
     for w in txWithdrawals: 
      w['ts'] = datetime.fromtimestamp(w['ts'])
      w['amount'] = np.format_float_positional(w['amount']/10**17,trim = '-')
      w['type'] = 'Withdrawal'
      w['token'] = token['{}'.format(w['token'])]
      w['first_net'] = network[self.netID]
      w['second_net'] = network['{}'.format(w['destNet'])]
    
     #Concatenate two lists to dataSet
     dataSet = txDeposits + txWithdrawals
     mainData.extend(dataSet)

     #Save Dataframe to CSV
     df = pd.DataFrame(dataSet,columns=header)
     df.sort_values(by=['ts'],inplace=True,ascending=False)
     df.drop_duplicates(inplace=True)
     df.to_csv(pathCSV,index=False) 

     del df,txDeposits,txWithdrawals,dataSet
   except Exception:
      raise

#Save Data from Token Datasets to Main Set
def saveMainSet():
  pathCSV = Path('static/datasets/main_set.csv')
  header = ['tx','first_net','second_net','token','ts','address','amount','type']
  
  #If CSV is not found Create new file
  if pathCSV.is_file() == False:
    with open(pathCSV,'x') as new_file:
      csvwriter = csv.writer(new_file)
      csvwriter.writerow(header)
      new_file.close()

  #Save Dataframe to Main Set CSV
  df = pd.DataFrame(mainData,columns=header)
  df.sort_values(by=['ts'],inplace=True,ascending=False)
  df.drop_duplicates(inplace=True)
  df.to_csv(pathCSV,index=False,float_format='%g')

  del df,mainData[:]

rinkebyFMTA = SaveToCSV('4','0','rinkeby_fmta')
rinkebyFMTA.save()

rinkebyTUSDTW = SaveToCSV('4','1','rinkeby_tusdtw')
rinkebyTUSDTW.save()

goerliFMTA = SaveToCSV('5','0','goerli_fmta')
goerliFMTA.save()

goerliTUSDTW = SaveToCSV('5','1','goerli_tusdtw')
goerliTUSDTW.save()

saveMainSet()
data = None







 

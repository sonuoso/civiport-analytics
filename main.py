import flask
from flask import render_template, redirect, url_for
import pandas as pd
import json
from numerize import numerize as numerize
import numpy as np
from datetime import datetime
import requests 

app = flask.Flask(__name__,
            static_folder='static',
            template_folder='template')
app.config["DEBUG"] = True

#Display an API unreachable notification in base.html
if (requests.head('http://207.244.228.250:56781/get').status_code != 200):
    api_down = True
else:
    api_down = False

@app.route("/home")
@app.route("/")
def home():
 main_set_df = pd.read_csv('static/datasets/main_set.csv')  #Read main_set CSV in to DataFrame
 token_set_df = pd.read_csv('static/datasets/token_info.csv')  #Read main_set CSV in to DataFrame
 main_set_json = main_set_df.to_json(orient='records')  #Convert DataFrame to JSON
 main_set_data = json.loads(main_set_json) #Convert JSON to a Python Dictionary 

#Format Decimal Notation of Amount properly
 for i in main_set_data:
     i['amount'] = np.format_float_positional(i['amount'],trim='-')

 main_set_df['ts'] = pd.to_datetime(main_set_df['ts']) #Convert Timestamp to a proper datetime format
 daily_volume_mainset = main_set_df.groupby(main_set_df['ts'].dt.day,sort=False)['amount'].sum().tolist() #Group All Transactions by Day and the sum of Amount and Convert to a list
 
 day_mainset = main_set_df.groupby(pd.Grouper(key='ts',freq="D",axis=0))['tx'].count().to_json() #Group Teleports by Day 
 week_mainset = main_set_df.groupby(pd.Grouper(key='ts',freq="W",axis=0))['tx'].count().to_json() #Group Teleports by Week
 month_mainset = main_set_df.groupby(pd.Grouper(key='ts',freq="M",axis=0))['tx'].count().to_json() #Group Teleports by Month

 day_set = json.loads(day_mainset)
 week_set = json.loads(week_mainset)
 month_set = json.loads(month_mainset)

 day_teleports = []
 week_teleports = []
 month_teleports = []

 #Clean Timestamp of Key Dates and Append to a list
 for d in list(day_set.keys()):
     d = int(d)
     d = datetime.fromtimestamp(d/1000).strftime('%m-%d')
     day_teleports.append(d)

 for w in list(week_set.keys()):
     w = int(w)
     w = datetime.fromtimestamp(w/1000).strftime('%m-%d')
     week_teleports.append(w)    

 for m in list(month_set.keys()):
     m = int(m)
     m = datetime.fromtimestamp(m/1000).strftime('%m-%d')
     month_teleports.append(m)

 day_teleports_data = {'day':day_teleports,'teleports': list(day_set.values())}
 week_teleports_data = {'week':week_teleports,'teleports': list(week_set.values())}
 month_teleports_data = {'month':month_teleports,'teleports': list(month_set.values())}

 day_volume = main_set_df.groupby(pd.Grouper(key='ts',freq="D",axis=0))['amount'].sum().to_json() #Group Volume by Day 
 week_volume = main_set_df.groupby(pd.Grouper(key='ts',freq="W",axis=0))['amount'].sum().to_json() #Group Volume by Week
 month_volume = main_set_df.groupby(pd.Grouper(key='ts',freq="M",axis=0))['amount'].sum().to_json() #Group Volume by Month

 day_volume_set = json.loads(day_volume)
 week_volume_set = json.loads(week_volume)
 month_volume_set = json.loads(month_volume)

 day_vol = []
 week_vol = []
 month_vol = []

 #Clean Timestamp of Key Dates and Append to a list
 for d in list(day_volume_set.keys()):
     d = int(d)
     d = datetime.fromtimestamp(d/1000).strftime('%m-%d')
     day_vol.append(d)

 for w in list(week_volume_set.keys()):
     w = int(w)
     w = datetime.fromtimestamp(w/1000).strftime('%m-%d')
     week_vol.append(w)    

 for m in list(month_volume_set.keys()):
     m = int(m)
     m = datetime.fromtimestamp(m/1000).strftime('%m-%d')
     month_vol.append(m)

 day_volume_data = {'day':day_vol,'volume': list(day_volume_set.values())}
 week_volume_data = {'week':week_vol,'volume': list(week_volume_set.values())}
 month_volume_data = {'month':month_vol,'volume': list(month_volume_set.values())}


 data = {'teleports':len(main_set_df.index),'volume':numerize.numerize(daily_volume_mainset[0]),'transactions': main_set_data, 'day_teleports_data': day_teleports_data, 'week_teleports_data' : week_teleports_data, 'month_teleports_data' : month_teleports_data, 'day_volume_data' : day_volume_data, 'week_volume_data': week_volume_data, 'month_volume_data' : month_volume_data, 'tokens' : len(token_set_df.index)}
 return render_template("home.html",data=data,api_down=api_down)
 
@app.route("/token/<token>")
def token(token):
 main_set_df = pd.read_csv('static/datasets/main_set.csv')  
 token_set_df = main_set_df.loc[main_set_df['token'] == '{}'.format(token)] 
 token_set_json = token_set_df.to_json(orient='records')  #Convert DataFrame to JSON
 token_set_data = json.loads(token_set_json) 

 token_info_df = pd.read_csv('static/datasets/token_info.csv')  
 token_ticker_df = token_info_df.loc[token_info_df['symbol'] == '{}'.format(token)] 
 main_set_json = token_ticker_df.to_json(orient='records')  
 main_set_data = json.loads(main_set_json)  
 
#Format Decimal Notation of Amount properly
 for i in token_set_data:
     i['amount'] = np.format_float_positional(i['amount'],trim='-')

 token_set_df['ts'] = pd.to_datetime(token_set_df['ts']) #Convert Timestamp to a proper datetime format
 token_volume = token_set_df.groupby(token_set_df['token'])['amount'].sum().tolist() #Group All Transactions by token

 day_mainset = token_set_df.groupby(pd.Grouper(key='ts',freq="D",axis=0))['tx'].count().to_json() #Group Teleports by Day 
 week_mainset = token_set_df.groupby(pd.Grouper(key='ts',freq="W",axis=0))['tx'].count().to_json() #Group Teleports by Week
 month_mainset = token_set_df.groupby(pd.Grouper(key='ts',freq="M",axis=0))['tx'].count().to_json() #Group Teleports by Month

 day_set = json.loads(day_mainset)
 week_set = json.loads(week_mainset)
 month_set = json.loads(month_mainset)

 day_teleports = []
 week_teleports = []
 month_teleports = []

 #Clean Timestamp of Key Dates and Append to a list
 for d in list(day_set.keys()):
     d = int(d)
     d = datetime.fromtimestamp(d/1000).strftime('%m-%d')
     day_teleports.append(d)

 for w in list(week_set.keys()):
     w = int(w)
     w = datetime.fromtimestamp(w/1000).strftime('%m-%d')
     week_teleports.append(w)    

 for m in list(month_set.keys()):
     m = int(m)
     m = datetime.fromtimestamp(m/1000).strftime('%m-%d')
     month_teleports.append(m)

 day_teleports_data = {'day':day_teleports,'teleports': list(day_set.values())}
 week_teleports_data = {'week':week_teleports,'teleports': list(week_set.values())}
 month_teleports_data = {'month':month_teleports,'teleports': list(month_set.values())}

 day_volume = token_set_df.groupby(pd.Grouper(key='ts',freq="D",axis=0))['amount'].sum().to_json() #Group Volume by Day 
 week_volume = token_set_df.groupby(pd.Grouper(key='ts',freq="W",axis=0))['amount'].sum().to_json() #Group Volume by Week
 month_volume = token_set_df.groupby(pd.Grouper(key='ts',freq="M",axis=0))['amount'].sum().to_json() #Group Volume by Month

 day_volume_set = json.loads(day_volume)
 week_volume_set = json.loads(week_volume)
 month_volume_set = json.loads(month_volume)

 day_vol = []
 week_vol = []
 month_vol = []

 #Clean Timestamp of Key Dates and Append to a list
 for d in list(day_volume_set.keys()):
     d = int(d)
     d = datetime.fromtimestamp(d/1000).strftime('%m-%d')
     day_vol.append(d)

 for w in list(week_volume_set.keys()):
     w = int(w)
     w = datetime.fromtimestamp(w/1000).strftime('%m-%d')
     week_vol.append(w)    

 for m in list(month_volume_set.keys()):
     m = int(m)
     m = datetime.fromtimestamp(m/1000).strftime('%m-%d')
     month_vol.append(m)

 day_volume_data = {'day':day_vol,'volume': list(day_volume_set.values())}
 week_volume_data = {'week':week_vol,'volume': list(week_volume_set.values())}
 month_volume_data = {'month':month_vol,'volume': list(month_volume_set.values())}

 data = {'teleports':len(token_set_df.index),'volume':numerize.numerize(token_volume[0]),'transactions': token_set_data,'day_teleports_data': day_teleports_data, 'week_teleports_data' : week_teleports_data, 'month_teleports_data' : month_teleports_data, 'day_volume_data' : day_volume_data, 'week_volume_data': week_volume_data, 'month_volume_data' : month_volume_data,'main_set_data':main_set_data}
 return render_template("token.html",data=data,api_down=api_down)

@app.route("/tx/<tx>")
def transactions(tx):
 main_set_df = pd.read_csv('static/datasets/main_set.csv')  #Read CSV in to DataFrame
 transaction_set_df = main_set_df.loc[main_set_df['tx'] == '{}'.format(tx)] 
 transaction_set_json = transaction_set_df.to_json(orient='records')  #Convert DataFrame to JSON
 transaction_set_data = json.loads(transaction_set_json) #Convert JSON to a Python Dictionary

 #Format Decimal Notation of Amount properly
 for i in transaction_set_data:
     i['amount'] = np.format_float_positional(i['amount'],trim='-')

 return render_template("transaction.html",transaction_data=transaction_set_data,api_down=api_down)

@app.route("/tokens")
def tokens():
 tokens_df = pd.read_csv('static/datasets/token_info.csv')  #Read CSV in to DataFrame
 tokens_set_json = tokens_df.to_json(orient='records')  #Convert DataFrame to JSON
 tokens_set_data = json.loads(tokens_set_json) #Convert JSON to a Python Dictionary
 main_set_df = pd.read_csv('static/datasets/main_set.csv')  #Read main_set CSV in to DataFrame
 main_set_json = main_set_df.to_json(orient='records')  #Convert DataFrame to JSON
 main_set_data = json.loads(main_set_json) #Convert JSON to a Python Dictionary 

#Format Decimal Notation of Amount properly
 for i in main_set_data:
     i['amount'] = np.format_float_positional(i['amount'],trim='-')

 main_set_df['ts'] = pd.to_datetime(main_set_df['ts']) #Convert Timestamp to a proper datetime format
 
 volume_mainset = main_set_df.groupby(pd.Grouper(key='token'))['amount'].sum().to_json() #Group Teleports by Day 
 token_mainset = main_set_df.groupby(pd.Grouper(key='token'))['tx'].count().to_json() #Group Teleports by Day 

 token_set = json.loads(token_mainset)
 volume_set = json.loads(volume_mainset)

 token_teleports = []
 volume_teleports = []

 #Append to a list
 for d in list(token_set.keys()):
     token_teleports.append(d)

 for d in list(volume_set.keys()):
     volume_teleports.append(d)

 token_data = {'token':token_teleports,'teleports': list(token_set.values())}
 volume_data = {'token':volume_teleports,'volume': list(volume_set.values())}
 
 data = {'token_data': token_data, 'volume_data':volume_data}

 return render_template("tokens.html",tokens=tokens_set_data,data=data,api_down=api_down)

@app.route("/wallet/<address>")
def wallet(address):
 main_set_df = pd.read_csv('static/datasets/main_set.csv')  
 wallet_set_df = main_set_df.loc[main_set_df['address'] == '{}'.format(address)] 
 wallet_set_json = wallet_set_df.to_json(orient='records')  #Convert DataFrame to JSON
 wallet_set_data = json.loads(wallet_set_json) 
 
#Format Decimal Notation of Amount properly
 for i in wallet_set_data:
     i['amount'] = np.format_float_positional(i['amount'],trim='-')

 wallet_set_df['ts'] = pd.to_datetime(wallet_set_df['ts']) #Convert Timestamp to a proper datetime format
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
 
 data = {'wallet_data': wallet_data, 'volume_data':volume_data, 'wallet_teleports' : wallet_set_data, 'total_teleports' : len(wallet_set_df.index)}
 
 return render_template("wallet.html",data=data,api_down=api_down)

@app.errorhandler(Exception)
def server_error(e):
 err_details = {'img_src':"500.svg",'err_text':"Internal Server Error",'err_desc':"Something seems to be wrong with the Web Server."}
 return render_template("error.html",err_details=err_details)

@app.errorhandler(404)
def not_found_error(e):
 err_details = {'img_src':"404.svg",'err_text':"Not Found",'err_desc':"Data or Web Page trying access is not available."}
 return render_template("error.html",err_details=err_details)

@app.errorhandler(403)
def forbidden_error(e):
 err_details = {'img_src':"403.svg",'err_text':"Forbidden",'err_desc':"Data or Document trying to access is not allowed."}
 return render_template("error.html",err_details=err_details)

@app.errorhandler(400)
def bad_request_error(e):
 err_details = {'img_src':"400.svg",'err_text':"Bad Request",'err_desc':"HTTP Request seems to be corrupted. Try again."}
 return render_template("error.html",err_details=err_details)


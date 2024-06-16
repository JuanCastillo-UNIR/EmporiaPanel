from datetime import datetime  
from dateutil.relativedelta import relativedelta  
from src.api_emporia.emporia_conection import data_extract
import pandas as pd
import time, glob


def checking_data(client):   
    device_name, data = ('', pd.DataFrame(columns=['Time Bucket']))
    current_date = datetime.fromtimestamp(time.time())
    start_date = datetime.fromtimestamp(time.time()) - relativedelta(years=1)
    client_on_db = [i for i in glob.glob('db/*.csv') if client.lower() in i]
    if len(client_on_db)==0:
        data_concat = []
        for i in range(4):
            start_interval = (start_date + relativedelta(months=3*i)).timestamp()
            end_interval = (start_date + relativedelta(months=3*(i+1)) if i<3 else current_date).timestamp()
            data, device_name = data_extract(client, start_interval, end_interval)
            if len(data)!=0: data_concat.append(data)
        if len(data_concat)!=0:
            data = pd.concat(data_concat)
            data.to_csv(f'db/{device_name.lower()}.csv',index=False)
    else:
        try:
            data = pd.read_csv(f"{client_on_db[0].lower()}")      
            data['Time Bucket'] = [pd.to_datetime(t, format='%Y-%m-%d').date() for t in data['Time Bucket']]
            date_obj = data['Time Bucket'].values[-1]
            last_date = datetime(date_obj.year, date_obj.month, date_obj.day)  
            data_concat, device_name = data_extract(cliente=client, 
                                                    start_interval=last_date.timestamp(), 
                                                    end_interval=current_date.timestamp())
            data = pd.concat([data,data_concat]).drop_duplicates(subset='Time Bucket', keep='last')
            data.to_csv(f'db/{device_name.lower()}.csv', index=False)
        except: 
            import os; os.remove(f"{client_on_db[0].lower()}")
    return device_name, data
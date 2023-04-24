import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode
from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka import Consumer, KafkaError 
from io import BytesIO
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
import joblib
from google_drive_downloader import GoogleDriveDownloader as gdd
import numpy as np
import os
from datetime import datetime
import warnings

import subprocess


warnings.filterwarnings("ignore", category=DeprecationWarning) 

st.set_page_config(page_title="Security & Applications", layout="wide") 
st.title("Dashboard - Credit Card Transactions")

conf = {
        'bootstrap.servers': st.secrets["default"]["bootstrap.servers"],
        'sasl.username': st.secrets["default"]["sasl.username"],
        'sasl.password': st.secrets["default"]["sasl.password"],
        'security.protocol': st.secrets["default"]["security.protocol"],
        'sasl.mechanisms': st.secrets["default"]["sasl.mechanisms"],
        'group.id': st.secrets["consumer"]["group.id"],
        'auto.offset.reset': st.secrets["consumer"]["auto.offset.reset"]
    }

df = pd.read_csv("./data/sample.csv")

def download_model():
    gdd.download_file_from_google_drive(file_id='1ThWf_IPAWzdVC3Qeppkm40SIGjPZUkMp',
                                    dest_path='./model/random_forest.joblib',
                                    unzip=False,
                                    overwrite=True)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)

cellstyle_jscode = JsCode("""
        function(params){
            if (params.data.is_fraud == '1') {
                return {
                    'color': 'black', 
                    'backgroundColor': 'Red',
                }
            }    
        }
        """)



gb.configure_columns(df)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()
gridOptions['getRowStyle'] = cellstyle_jscode


def dashboard():
    grid_result = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allow_unsafe_jscode=True,reload_data=True )





    #--------------------------------------------notification end


def predict(df_test):
    
    features = ['transaction_id', 'hour_of_day', 'category', 'amount(usd)', 'merchant', 'job']

    df_test = df_test.rename(columns={"trans_date_trans_time":"transaction_time",
                         "cc_num":"credit_card_number",
                         "amt":"amount(usd)",
                         "trans_num":"transaction_id"}
                        )

    # Apply function utcfromtimestamp and drop column unix_time
    df_test['time'] = df_test['unix_time']

    #  Add cloumn hour of day
    df_test['hour_of_day'] = df_test.time.dt.hour

    df_test = df_test[features].set_index("transaction_id")
    enc = OrdinalEncoder(dtype=np.int64)
    enc.fit(df_test.loc[:, ['category','merchant','job']])

    df_test.loc[:, ['category','merchant','job']] = enc.transform(df_test[['category','merchant','job']])

    rf_random = joblib.load("./model/random_forest.joblib")
    y_pred  = rf_random.predict(df_test)
    return y_pred




if __name__ == '__main__':
    if not os.path.isfile("./model/random_forest.joblib"):
        download_model()
    dashboard()

consumer = Consumer(conf)
topic = 'topic_0'
consumer.subscribe([topic])

if st.button('Refresh'):
    st.experimental_rerun()


while True:
    msg = consumer.poll(10.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached')
        else:
            print('Error while consuming message: {}'.format(msg.error()))
    else:
        try:
            print('Received message:  value={} , offset={}'.format(  msg.value(),   msg.offset()))
            dfmessage = pd.read_json(BytesIO(msg.value()), orient="records")
            #df = df.append(pd.read_json(BytesIO(msg.value()), orient="records"))
            dfmessage = dfmessage.drop(['is_fraud'], axis=1)
            print(dfmessage)
            #apply prediction
            output = predict(dfmessage)
            outputdf = pd.DataFrame(output, columns = ['is_fraud'])
            print(outputdf)
            
            dfmessage = pd.concat([dfmessage, outputdf[['is_fraud']]], axis=1)
            dfmessage = dfmessage[['trans_date_trans_time','cc_num','merchant','category','amt'
                                  ,'first','last','gender','street','city','state','zip',
                                  'lat','long','city_pop','job','dob','trans_num','unix_time','merch_lat','merch_long','is_fraud']]
            #Reload the data from store
            df = pd.read_csv("./data/sample.csv")

            df = df.append(dfmessage) 
            df.to_csv('./data/sample.csv', index=False)
            #grid_result = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allow_unsafe_jscode=True,reload_data=True )
            #st.experimental_rerun()


            #send notification
            if dfmessage.iloc[0]['is_fraud'] == 1:
                message = """Security Alert! Unusual Credit Card activity detected. A transaction of USD """+ str(dfmessage['amt'][0]) +  """ at merchant"""+ str(dfmessage['merchant'][0]) +  """ on """+ str(dfmessage['trans_date_trans_time'][0]) +  """ has been recorded. 
                Please contact bank immediately if you don't recognize this transaction"""
                subprocess.run(['python3', 'telegram.py', message])


        except Exception as e:
            print("An exception occurred: "+ str(e))

 
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode
from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka import Consumer, KafkaError 
from io import BytesIO

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

if __name__ == '__main__':
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
        print('Received message:  value={} , offset={}'.format(  msg.value(),   msg.offset()))
        #df1 = pd.read_json(BytesIO(msg.value()), orient="records")
        df = df.append(pd.read_json(BytesIO(msg.value()), orient="records"))
        print(df)
        df.to_csv('./data/sample.csv', index=False)
        grid_result = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allow_unsafe_jscode=True,reload_data=True )


 
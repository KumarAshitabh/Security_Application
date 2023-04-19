import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_echarts import st_echarts 
st.set_page_config(page_title="Security & Applications", layout="wide") 
st.title("Dashboard - Credit Card Transactions")

df = pd.read_csv("./data/sample.csv")
df.index.rename('Serial No', inplace=True)

def score_style(val):
    '''
    highlight the cell if the value is greater than or equal to 80
    '''
    if val >= 80:
        return 'background-color: yellow'
    else:
        return ''



gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)

gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()

AgGrid(df, columnDefs=[
              {'headerName': 'trans_date_trans_time', 'field': 'trans_date_trans_time'},
              {'headerName': 'merch_long', 'field': 'merch_long'},
              {'headerName': 'is_fraud', 'field': 'is_fraud', 'cellStyle': score_style}
          ])
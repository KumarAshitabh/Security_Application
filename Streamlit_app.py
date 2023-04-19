import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode


# Allow unsafe JavaScript code
st.set_page_config(allow_unsafe_jscode=True)
st.set_page_config(page_title="Security & Applications", layout="wide") 
st.title("Dashboard - Credit Card Transactions")

df = pd.read_csv("./data/sample.csv")
df.index.rename('Serial No', inplace=True)
# add this
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)

cellstyle_jscode = JsCode("""
function(params){
    if (params.value == '1') {
        return {
            'color': 'black', 
            'backgroundColor': 'orange',
        }
    }    
}
""")


gb.configure_pagination(enabled=True)
gb.configure_columns(df, cellStyle= cellstyle_jscode)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
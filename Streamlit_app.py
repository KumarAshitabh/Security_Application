import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode



st.set_page_config(page_title="Security & Applications", layout="wide") 
st.title("Dashboard - Credit Card Transactions")

df = pd.read_csv("./data/sample.csv")

# add this
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

grid_result = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allow_unsafe_jscode=True,reload_data=True)


# add a button to refresh the AgGrid
if st.button('Refresh'):
    df = pd.read_csv("./data/sample.csv").head(10)
    grid_result = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allow_unsafe_jscode=True,reload_data=True)
    st.experimental_rerun()

# display the result
st.write('Selected:', grid_result['selected_rows'])
 
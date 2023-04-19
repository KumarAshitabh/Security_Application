import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode



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



gb.configure_columns(df, cellStyle= cellstyle_jscode)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allow_unsafe_jscode=True)




# Create a sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'Score': [80, 90, 70, 85]
})

# Define a function to apply conditional formatting to an entire row based on the value of the "Score" column
def get_row_style(params):
    score = float(params.data['Score'])
    if score >= 80:
        return {'background-color': 'yellow'}
    else:
        return {}

# Display the AgGrid table with conditional formatting
st.write('<style> .ag-cell { padding: 6px !important; } </style>', unsafe_allow_html=True)
st_aggrid = st.empty()
st_aggrid.write('<div id="myGrid" style="height: 200px" class="ag-theme-alpine"></div>', unsafe_allow_html=True)
st.write(f"""
    <script>
        var gridOptions = {{
            columnDefs: [
                {{headerName: 'Name', field: 'Name'}},
                {{headerName: 'Age', field: 'Age'}},
                {{headerName: 'Score', field: 'Score'}}
            ],
            rowData: {df.to_json(orient='records')},
            getRowStyle: {get_row_style}
        }};
        new agGrid.Grid(document.querySelector('#myGrid'), gridOptions);
    </script>
""", unsafe_allow_html=True)
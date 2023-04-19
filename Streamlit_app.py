import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

# create a sample dataframe
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [25, 30, 35, 40],
    'gender': ['Male', 'Female', 'Male', 'Female']
})

# display the AgGrid component
grid_result = AgGrid(df)

# add a button to update the dataframe in the AgGrid
if st.button('Update DataFrame in AgGrid'):
    # update the dataframe
    df['age'] = [26, 31, 36, 41]
    # rerun the script
    st.experimental_rerun()

    # display the updated AgGrid component
    grid_result = AgGrid(df)

# display the selected rows in the AgGrid component
st.write('Selected Rows:', grid_result['selected_rows'])

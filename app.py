import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool
import numpy as np

# Title of the app
st.title('Pluspetrol Template')

# Add a sidebar
st.sidebar.title('Options')

# Upload the Excel file
file = st.sidebar.file_uploader('Upload your Excel file', type=['xlsx', 'xls', 'xlsm'])

if file is not None:
    # Load the file into a pandas DataFrame
    df = pd.read_excel(file)

    # Create a "blanc" column named "derivative"
    df['derivative'] = np.nan

    # Let the user select the columns for the x and y axes
    x_col = st.sidebar.selectbox('Select the column for the x axis', df.columns, key='x_col')

    if x_col == 'derivative':
        with st.sidebar:
            st.write('### Derivative Options for X Axis')
            # Add additional input fields for derivative calculation
            original_col_x = st.selectbox('Select the original column for the derivative (X axis)', df.columns, key='original_col_x')
            interval_x = st.number_input('Select the interval for derivative calculation (X axis)', min_value=1, value=10, key='interval_x')

        # Let the user select the column for the y axis
        y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    else:
        # Let the user select the column for the y axis
        y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    if y_col == 'derivative':
        with st.sidebar:
            st.write('### Derivative Options for Y Axis')
            # Add additional input fields for derivative calculation
            original_col_y = st.selectbox('Select the original column for the derivative (Y axis)', df.columns, key='original_col_y')
            interval_y = st.number_input('Select the interval for derivative calculation (Y axis)', min_value=1, value=10, key='interval_y')

        # Let the user select the column for the x axis
        x_col = st.sidebar.selectbox('Select the column for the x axis', df.columns, key='x_col_y')

    # Check if the user selected "derivative" for x_col or y_col
    if 'derivative' in [x_col, y_col]:
        if x_col == 'derivative':
            # Calculate the derivative for x_col
            derivative_values = (df[original_col_x].shift(-interval_x) - df[original_col_x]) / (df[y_col].shift(-interval_x) - df[y_col])
            df.loc[1:interval_x, 'derivative'] = np.nan
            df.loc[interval_x + 1:, 'derivative'] = derivative_values

        if y_col == 'derivative':
            # Calculate the derivative for y_col
            derivative_values = (df[x_col].shift(-interval_y) - df[x_col]) / (df[original_col_y].shift(-interval_y) - df[original_col_y])
            df.loc[1:interval_y, 'derivative'] = np.nan
            df.loc[interval_y + 1:, 'derivative'] = derivative_values

    # Create the plot using bokeh
    p = figure(plot_width=600, plot_height=400, tooltips=[(x_col, '@x'), (y_col, '@y')])

    if 'derivative' not in [x_col, y_col]:
        p.scatter(df[x_col], df[y_col], size=5, fill_color='blue', alpha=0.8)
    else:
        p.scatter(df[x_col], df[y_col], size=5, fill_color='blue', alpha=0.8, legend_label='Original')
        p.scatter(df[x_col], df['derivative'], size=5, fill_color='red', alpha=0.8, legend_label='Derivative')

    hover_tool = HoverTool(
        tooltips=[
            (x_col, '@' + x_col),
            (y_col, '@' + y_col)
        ]
    )
    p.add_tools(hover_tool)

    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'

    st.bokeh_chart(p)

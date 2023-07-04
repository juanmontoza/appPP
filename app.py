import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.layouts import row
import numpy as np
import math

# Title of the app
st.title('Pluspetrol Template')

# Add a sidebar
st.sidebar.title('Options')

# Upload the Excel file
file = st.sidebar.file_uploader('Upload your Excel file', type=['xlsx', 'xls', 'xlsm'])

if file is not None:
    # Load the file into a pandas DataFrame
    df = pd.read_excel(file)

    # Create a "blanc" column named "derivative" and "Angle of Attack"
    df['derivative'] = np.nan
    df['Angle of Attack'] = np.nan

    # Let the user select the columns for the x and y axes
    x_col = st.sidebar.selectbox('Select the column for the x axis', df.columns, key='x_col')
    y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    add_additional_plot = st.sidebar.checkbox('Add additional plot')

    # Check if the user selected "derivative" for x_col or y_col
    if 'derivative' in [x_col, y_col]:
        with st.sidebar:
            st.write('### Derivative Options')
            original_col = st.selectbox('Select the original column for the derivative', df.columns, key='original_col')
            interval = st.number_input('Select the interval for derivative calculation', min_value=1, value=10,
                                       key='interval')

    # Check if the user selected "Angle of Attack" for x_col or y_col
    if 'Angle of Attack' in [x_col, y_col]:
        with st.sidebar:
            st.write('### Angle of Attack Options')
            original_col = st.selectbox('Select the original column for the Angle of Attack', df.columns,
                                        key='original_col')
            interval = st.number_input('Select the interval for Angle of Attack calculation', min_value=1, value=10,
                                       key='interval')

    # Calculate the derivative if selected
    if 'derivative' in [x_col, y_col]:
        derivative_values = (df[original_col].shift(-interval) - df[original_col]) / (
                    df[y_col].shift(-interval) - df[y_col])
        df.loc[1:interval, 'derivative'] = np.nan
        df.loc[interval + 1:, 'derivative'] = derivative_values

    # Calculate the Angle of Attack if selected
    if 'Angle of Attack' in [x_col, y_col]:
        um_values = df['UM'].shift(-interval) - df['UM']
        dup_values = df['DUP'].shift(-interval) - df['DUP']
        tvida_values = df[original_col].shift(-interval) - df[original_col]

        angle_of_attack_values = (np.arctan2(um_values + dup_values, interval) - np.arctan2(tvida_values, interval)) * (
                    180 / math.pi)
        df.loc[1:interval, 'Angle of Attack'] = np.nan
        df.loc[interval + 1:, 'Angle of Attack'] = angle_of_attack_values

    # Create the first plot using bokeh
    p1 = figure(plot_width=600, plot_height=400)

    if 'derivative' not in [x_col, y_col] and 'Angle of Attack' not in [x_col, y_col]:
        p1.scatter(df[x_col], df[y_col], size=5, fill_color='blue', alpha=0.8)
    else:
        if 'derivative' in [x_col, y_col]:
            p1.scatter(df[x_col], df[y_col], size=5, fill_color='blue', alpha=0.8, legend_label='Original')
            p1.scatter(df[x_col], df['derivative'], size=5, fill_color='red', alpha=0.8, legend_label='Derivative')

        if 'Angle of Attack' in [x_col, y_col]:
            p1.scatter(df[x_col], df[y_col], size=5, fill_color='blue', alpha=0.8, legend_label='Original')
            p1.scatter(df[x_col], df['Angle of Attack'], size=5, fill_color='green', alpha=0.8,
                       legend_label='Angle of Attack')

    hover_tool = HoverTool(
        tooltips=[
            (x_col, '@' + x_col),
            (y_col, '@' + y_col)
        ]
    )
    p1.add_tools(hover_tool)

    p1.legend.location = 'top_left'
    p1.legend.click_policy = 'hide'

    # Add the second plot if "Add additional plot" is selected
    if add_additional_plot:
        x_col_additional = st.sidebar.selectbox('Select the column for the additional plot (X axis)', df.columns,
                                                key='x_col_additional')
        y_col_additional = st.sidebar.selectbox('Select the column for the additional plot (Y axis)', df.columns,
                                                key='y_col_additional')

        p2 = figure(plot_width=600, plot_height=400)

        p2.scatter(df[x_col_additional], df[y_col_additional], size=5, fill_color='green', alpha=0.8,
                   legend_label='Additional Plot')

        hover_tool_additional = HoverTool(
            tooltips=[
                (x_col_additional, '@' + x_col_additional),
                (y_col_additional, '@' + y_col_additional)
            ]
        )
        p2.add_tools(hover_tool_additional)

        p2.legend.location = 'top_left'
        p2.legend.click_policy = 'hide'

        # Display both plots
        st.bokeh_chart(row(p1, p2))
    else:
        # Display only the first plot
        st.bokeh_chart(p1)

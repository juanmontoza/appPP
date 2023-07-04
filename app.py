import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors
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

    if x_col == 'Angle of Attack':
        with st.sidebar:
            st.write('### Angle of Attack Options for X Axis')
            # Add additional input field for interval
            interval_x = st.number_input('Select the interval for Angle of Attack calculation (X axis)', min_value=1, value=10, key='interval_x')

        # Let the user select the column for the y axis
        y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    else:
        # Let the user select the column for the y axis
        y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    if y_col == 'Angle of Attack':
        with st.sidebar:
            st.write('### Angle of Attack Options for Y Axis')
            # Add additional input field for interval
            interval_y = st.number_input('Select the interval for Angle of Attack calculation (Y axis)', min_value=1, value=10, key='interval_y')

        # Let the user select the column for the x axis
        x_col = st.sidebar.selectbox('Select the column for the x axis', df.columns, key='x_col_y')

    # Check if the user selected "Angle of Attack" for x_col or y_col
    if 'Angle of Attack' in [x_col, y_col]:
        if x_col == 'Angle of Attack':
            # Calculate the Angle of Attack for x_col
            um_values = df['UM'].shift(-interval_x) - df['UM']
            dup_values = df['DUP'].shift(-interval_x) - df['DUP']
            angle_of_attack_values = (np.arctan2(um_values, dup_values) - np.arctan2(interval_x, interval_x)) * (180 / np.pi)
            df.loc[1:interval_x, 'Angle of Attack'] = np.nan
            df.loc[interval_x + 1:, 'Angle of Attack'] = angle_of_attack_values

        if y_col == 'Angle of Attack':
            # Calculate the Angle of Attack for y_col
            um_values = df['UM'].shift(-interval_y) - df['UM']
            tvida_values = df['TVDa'].shift(-interval_y) - df['TVDa']
            angle_of_attack_values = (np.arctan2(interval_y, tvida_values) - np.arctan2(um_values, interval_y)) * (180 / np.pi)
            df.loc[1:interval_y, 'Angle of Attack'] = np.nan
            df.loc[interval_y + 1:, 'Angle of Attack'] = angle_of_attack_values

    # Create the first plot using Seaborn
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    if 'Angle of Attack' not in [x_col, y_col]:
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax1)
    else:
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax1, label='Original')
        sns.scatterplot(data=df, x=x_col, y='Angle of Attack', ax=ax1, label='Angle of Attack')

    points1 = ax1.collections[0]
    cursor1 = mplcursors.cursor(points1)
    cursor1.connect(
        "add",
        lambda sel: sel.annotation.set_text(f"({sel.target[0]:.2f}, {sel.target[1]:.2f})")
    )

    # Create the second plot using Seaborn
    if st.checkbox('Add additional plot'):
        # Let the user select the columns for the x and y axes for the additional plot
        x_col_additional = st.sidebar.selectbox('Select the column for the x axis (Additional Plot)', df.columns, key='x_col_additional')
        y_col_additional = st.sidebar.selectbox('Select the column for the y axis (Additional Plot)', df.columns, key='y_col_additional')

        # Calculate the Angle of Attack for the additional plot
        um_values_additional = df['UM'].shift(-interval_x) - df['UM']
        dup_values_additional = df['DUP'].shift(-interval_x) - df['DUP']
        angle_of_attack_values_additional = (np.arctan2(um_values_additional, dup_values_additional) - np.arctan2(interval_x, interval_x)) * (180 / np.pi)
        df['Angle of Attack Additional'] = np.nan
        df.loc[1:interval_x, 'Angle of Attack Additional'] = angle_of_attack_values_additional

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df, x=x_col_additional, y=y_col_additional, ax=ax2)
        sns.scatterplot(data=df, x=x_col_additional, y='Angle of Attack Additional', ax=ax2, label='Angle of Attack Additional')

        points2 = ax2.collections[0]
        cursor2 = mplcursors.cursor(points2)
        cursor2.connect(
            "add",
            lambda sel: sel.annotation.set_text(f"({sel.target[0]:.2f}, {sel.target[1]:.2f})")
        )

        # Arrange the plots in a 2-column layout
        col1, col2 = st.columns(2)
        col1.pyplot(fig1)
        col2.pyplot(fig2)
    else:
        # Render only the first plot
        st.pyplot(fig1)

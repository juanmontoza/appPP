import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors
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
            angle_of_attack_values = (np.arctan2(um_values, interval_y) - np.arctan2(tvida_values, interval_y)) * (180 / np.pi)
            df.loc[1:interval_y, 'Angle of Attack'] = np.nan
            df.loc[interval_y + 1:, 'Angle of Attack'] = angle_of_attack_values

    # Create the plot using Seaborn
    fig, ax = plt.subplots()
    if 'Angle of Attack' not in [x_col, y_col]:
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    else:
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax, label='Original')
        sns.scatterplot(data=df, x=x_col, y='Angle of Attack', ax=ax, label='Angle of Attack')

    points = ax.collections[0]
    cursor = mplcursors.cursor(points)
    cursor.connect(
        "add",
        lambda sel: sel.annotation.set_text(f"({sel.target[0]:.2f}, {sel.target[1]:.2f})")
    )
    st.pyplot(fig)

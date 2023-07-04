import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
    y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    add_additional_plot = st.sidebar.checkbox('Add additional plot')

    # Check if the user selected "derivative" for x_col or y_col
    if 'derivative' in [x_col, y_col]:
        with st.sidebar:
            st.write('### Derivative Options')
            original_col = st.selectbox('Select the original column for the derivative', df.columns, key='original_col')
            interval = st.number_input('Select the interval for derivative calculation', min_value=1, value=10, key='interval')

    # Check if the user selected "Angle of Attack" for x_col or y_col
    if 'Angle of Attack' in [x_col, y_col]:
        with st.sidebar:
            st.write('### Angle of Attack Options')
            interval = st.number_input('Select the interval for Angle of Attack calculation', min_value=1, value=10, key='interval')

    # Calculate the derivative if selected
    if 'derivative' in [x_col, y_col]:
        derivative_values = (df[original_col].shift(-interval) - df[original_col]) / (df[y_col].shift(-interval) - df[y_col])
        df.loc[1:interval, 'derivative'] = np.nan
        df.loc[interval + 1:, 'derivative'] = derivative_values

    # Calculate the Angle of Attack if selected
    if 'Angle of Attack' in [x_col, y_col]:
        um_values = df['UM'].shift(-interval) + df['DUP'].iloc[0] - (df['UM'] + df['DUP'].iloc[0])
        tvida_values = df['TVDa'].shift(-interval) - df['TVDa'].iloc[0]
        mda_values = df['MDa'].shift(-interval) - df['MDa'].iloc[0]

        angle_of_attack_values = (np.arctan2(um_values, mda_values) - np.arctan2(tvida_values, mda_values)) * (180 / np.pi)
        df.loc[1:interval, 'Angle of Attack'] = np.nan
        df.loc[interval + 1:, 'Angle of Attack'] = angle_of_attack_values

    # Create the first plot using Matplotlib
    fig, ax = plt.subplots()

    if 'derivative' not in [x_col, y_col] and 'Angle of Attack' not in [x_col, y_col]:
        ax.scatter(df[x_col], df[y_col], s=5, color='blue', alpha=0.8)
    else:
        if 'derivative' in [x_col, y_col]:
            ax.scatter(df[x_col], df[y_col], s=5, color='blue', alpha=0.8, label='Original')
            ax.scatter(df[x_col], df['derivative'], s=5, color='red', alpha=0.8, label='Derivative')

        if 'Angle of Attack' in [x_col, y_col]:
            ax.scatter(df[x_col], df[y_col], s=5, color='blue', alpha=0.8, label='Original')
            ax.scatter(df[x_col], df['Angle of Attack'], s=5, color='green', alpha=0.8, label='Angle of Attack')

        ax.legend()

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)

    st.pyplot(fig)

    # Create the second plot if "Add additional plot" is selected
    if add_additional_plot:
        x_col_additional = st.sidebar.selectbox('Select the column for the additional plot (X axis)', df.columns, key='x_col_additional')
        y_col_additional = st.sidebar.selectbox('Select the column for the additional plot (Y axis)', df.columns, key='y_col_additional')

        fig_additional, ax_additional = plt.subplots()
        ax_additional.scatter(df[x_col_additional], df[y_col_additional], s=5, color='green', alpha=0.8)
        ax_additional.set_xlabel(x_col_additional)
        ax_additional.set_ylabel(y_col_additional)

        st.pyplot(fig_additional)

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

    # Create a "derivative" column
    df['derivative'] = np.nan

    # Let the user select the columns for the x and y axes
    x_col = st.sidebar.selectbox('Select the column for the x axis', df.columns, key='x_col')
    y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    add_derivative = st.sidebar.checkbox('Calculate Derivative')

    if add_derivative:
        interval = st.sidebar.number_input('Enter the interval for derivative calculation', min_value=1, value=10)

        if x_col != 'derivative':
            derivative_values = (df[y_col].shift(-interval) - df[y_col]) / (df[x_col].shift(-interval) - df[x_col])
            df.loc[1:interval, 'derivative'] = np.nan
            df.loc[interval + 1:, 'derivative'] = derivative_values

        if y_col != 'derivative':
            derivative_values = (df[x_col].shift(-interval) - df[x_col]) / (df[y_col].shift(-interval) - df[y_col])
            df.loc[1:interval, 'derivative'] = np.nan
            df.loc[interval + 1:, 'derivative'] = derivative_values

    # Create the plot using Matplotlib
    fig, ax = plt.subplots()

    if 'derivative' not in [x_col, y_col]:
        ax.scatter(df[x_col], df[y_col], s=5, color='blue', label='Original')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

    if add_derivative:
        derivative_col = 'derivative' if x_col != 'derivative' else y_col
        ax.scatter(df[x_col], df[derivative_col], s=5, color='red', label='Derivative')

    ax.legend()
    st.pyplot(fig)

    # Show the DataFrame with the calculated derivative
    st.write(df)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
            original_col_x = st.selectbox('Select the original column for the derivative (X axis)', df.columns,
                                          key='original_col_x')
            interval_x = st.number_input('Select the interval for derivative calculation (X axis)', min_value=1,
                                         value=10, key='interval_x')

        # Let the user select the column for the y axis
        y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    else:
        # Let the user select the column for the y axis
        y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns, key='y_col')

    if y_col == 'derivative':
        with st.sidebar:
            st.write('### Derivative Options for Y Axis')
            # Add additional input fields for derivative calculation
            original_col_y = st.selectbox('Select the original column for the derivative (Y axis)', df.columns,
                                          key='original_col_y')
            interval_y = st.number_input('Select the interval for derivative calculation (Y axis)', min_value=1,
                                         value=10, key='interval_y')

        # Let the user select the column for the x axis
        x_col = st.sidebar.selectbox('Select the column for the x axis', df.columns, key='x_col_y')

    # Check if the user selected "derivative" for x_col or y_col
    if 'derivative' in [x_col, y_col]:
        if x_col == 'derivative':
            # Calculate the derivative for x_col
            derivative_values = (df[original_col_x].shift(-interval_x) - df[original_col_x]) / (
                        df[y_col].shift(-interval_x) - df[y_col])
            df.loc[1:interval_x, 'derivative'] = np.nan
            df.loc[interval_x + 1:, 'derivative'] = derivative_values

        if y_col == 'derivative':
            # Calculate the derivative for y_col
            derivative_values = (df[x_col].shift(-interval_y) - df[x_col]) / (
                        df[original_col_y].shift(-interval_y) - df[original_col_y])
            df.loc[1:interval_y, 'derivative'] = np.nan
            df.loc[interval_y + 1:, 'derivative'] = derivative_values

    # Create the plot using Seaborn
    fig, ax = plt.subplots()

    if 'derivative' not in [x_col, y_col]:
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    else:
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax, label='Original')
        sns.scatterplot(data=df, x=x_col, y='derivative', ax=ax, label='Derivative')

    ax.legend(loc='upper left')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)

    # Add hover text using Streamlit's hover functionality
    hover_data = df[[x_col, y_col]]
    if 'derivative' in [x_col, y_col]:
        hover_data['Derivative'] = df['derivative']

    hover_columns = [x_col, y_col] + (['Derivative'] if 'derivative' in [x_col, y_col] else [])

    hover_format = {}
    for column in hover_columns:
        hover_format[column] = '.2f'

    st.pyplot(fig, hover_data=hover_data, hover_columns=hover_columns, hover_format=hover_format)

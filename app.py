import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

    # Create a "derivative" column
    df['derivative'] = np.nan

    # Let the user select the columns for the x and y axes of the first plot
    x_col = st.sidebar.selectbox('Select the column for the x axis of the first plot', df.columns, key='x_col')
    y_col = st.sidebar.selectbox('Select the column for the y axis of the first plot', df.columns, key='y_col')

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

    # Set the axis ranges for the first plot
    x_range_min = st.sidebar.number_input('Set the minimum value for the x-axis of the first plot',
                                          value=df[x_col].min())
    x_range_max = st.sidebar.number_input('Set the maximum value for the x-axis of the first plot',
                                          value=df[x_col].max())
    y_range_min = st.sidebar.number_input('Set the minimum value for the y-axis of the first plot',
                                          value=df[y_col].min())
    y_range_max = st.sidebar.number_input('Set the maximum value for the y-axis of the first plot',
                                          value=df[y_col].max())

    # Create the first plot using Matplotlib
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    if add_derivative:
        derivative_col = 'derivative' if x_col != 'derivative' else y_col
        ax[1].set_xlabel(x_col)
        ax[1].set_ylabel('Derivative of {}'.format(y_col if x_col != 'derivative' else x_col))
        ax[1].scatter(df[x_col], df[derivative_col], s=5, color='red', label='Derivative')
        ax[1].set_xlim([x_range_min, x_range_max])
        ax[1].set_ylim([df[derivative_col].min(), df[derivative_col].max()])
        ax[1].legend()

    # Show the first plot
    st.pyplot(fig)

    # Add a checkbox for the second plot
    add_second_plot = st.sidebar.checkbox('Add Additional Plot')

    if add_second_plot:
        # Let the user select the columns for the x and y axes of the second plot
        x_col_additional = st.sidebar.selectbox('Select the column for the x axis of the second plot', df.columns,
                                                key='x_col_additional')
        y_col_additional = st.sidebar.selectbox('Select the column for the y axis of the second plot', df.columns,
                                                key='y_col_additional')

        # Set the axis ranges for the second plot
        x_range_min_additional = st.sidebar.number_input('Set the minimum value for the x-axis of the second plot',
                                                         value=df[x_col_additional].min())
        x_range_max_additional = st.sidebar.number_input('Set the maximum value for the x-axis of the second plot',
                                                         value=df[x_col_additional].max())
        y_range_min_additional = st.sidebar.number_input('Set the minimum value for the y-axis of the second plot',
                                                         value=df[y_col_additional].min())
        y_range_max_additional = st.sidebar.number_input('Set the maximum value for the y-axis of the second plot',
                                                         value=df[y_col_additional].max())

        # Create the second plot using Matplotlib
        fig_additional, ax_additional = plt.subplots(figsize=(6, 6))

        # Plot the original values
        ax_additional.set_xlabel(x_col_additional)
        ax_additional.set_ylabel(y_col_additional)
        ax_additional.scatter(df[x_col_additional], df[y_col_additional], s=5, color='green', label='Original')
        ax_additional.set_xlim([x_range_min_additional, x_range_max_additional])
        ax_additional.set_ylim([y_range_min_additional, y_range_max_additional])
        ax_additional.legend()

        # Show the second plot
        st.pyplot(fig_additional)

    # Show the DataFrame with the calculated derivative and angle of attack
    st.write(df)

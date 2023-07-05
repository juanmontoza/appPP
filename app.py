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


def calculate_intersection_angle(segment1, segment2):
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    slope1 = (y2 - y1) / (x2 - x1)
    slope2 = (y4 - y3) / (x4 - x3)

    if math.isclose(slope1, slope2):
        return 0  # Lines are parallel, angle of attack is 0

    angle1 = math.atan(slope1)
    angle2 = math.atan(slope2)

    intersection_angle = abs(angle1 - angle2)
    return math.degrees(intersection_angle)


if file is not None:
    # Load the file into a pandas DataFrame
    df = pd.read_excel(file)

    # Create a "derivative" column
    df['derivative'] = np.nan

    # Create an "Angle of Attack" column
    df['Angle of Attack'] = np.nan

    # Let the user select the columns for the x and y axes of the first plot
    x_col = st.sidebar.selectbox('Select the column for the x axis of the first plot', df.columns, key='x_col')
    y_col = st.sidebar.selectbox('Select the column for the y axis of the first plot', df.columns, key='y_col')

    if y_col == 'Angle of Attack':
        segment_length = st.sidebar.number_input('Enter the segment length', min_value=1, value=10)
        segment1 = [(df['UM'][i], df['DUP'][i]) for i in range(segment_length)]
        segment2 = [(df['TVDa'][i], df['MDa'][i]) for i in range(segment_length)]
        angle_of_attack = calculate_intersection_angle(segment1, segment2)
        df.loc[segment_length-1:, 'Angle of Attack'] = angle_of_attack

        # Set the axis range for Angle of attack
        y_range_min = 0
        y_range_max = 90

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
                                          value=np.nanmin(df[y_col]))  # Exclude NaN and Inf values
    y_range_max = st.sidebar.number_input('Set the maximum value for the y-axis of the first plot',
                                          value=np.nanmax(df[y_col]))  # Exclude NaN and Inf values

    # Create the first plot using Matplotlib
    fig, ax = plt.subplots()

    if add_derivative:
        derivative_col = 'derivative' if x_col != 'derivative' else y_col
        ax.scatter(df[x_col], df[derivative_col], s=5, color='red', label='Derivative')
        ax.set_xlabel(x_col)
        ax.set_ylabel('Derivative of {} '.format(y_col if y_col != 'derivative' else x_col))
    elif y_col == 'Angle of Attack':
        ax.set_xlabel(x_col)
        ax.set_ylabel('Angle of Attack (degrees)')
        ax.scatter(df[x_col], df[y_col], s=5, color='green', label='Angle of Attack')
    else:
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.scatter(df[x_col], df[y_col], s=5, color='blue', label=y_col)

    ax.set_xlim([x_range_min, x_range_max])
    ax.set_ylim([y_range_min, y_range_max])
    ax.legend()
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
                                                         value=np.nanmin(df[y_col_additional]))  # Exclude NaN and Inf values
        y_range_max_additional = st.sidebar.number_input('Set the maximum value for the y-axis of the second plot',
                                                         value=np.nanmax(df[y_col_additional]))  # Exclude NaN and Inf values

        # Create the second plot using Matplotlib
        fig_additional, ax_additional = plt.subplots()

        ax_additional.scatter(df[x_col_additional], df[y_col_additional], s=5, color='green', label=y_col_additional)
        ax_additional.set_xlabel(x_col_additional)
        ax_additional.set_ylabel(y_col_additional)

        ax_additional.set_xlim([x_range_min_additional, x_range_max_additional])
        ax_additional.set_ylim([y_range_min_additional, y_range_max_additional])
        ax_additional.legend()
        st.pyplot(fig_additional)

    # Show the DataFrame with the calculated derivative
    st.write(df)

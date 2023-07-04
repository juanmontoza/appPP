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

    # Get user input for interval and variable selection
    interval_start = st.number_input('Interval Start', value=0.0)
    interval_end = st.number_input('Interval End', value=1.0)
    variable_options = list(file.columns)  # Assumes columns contain variable names
    variable = st.selectbox('Variable', variable_options)

    # Filter the data within the specified interval
    filtered_data = file[(file['x'] >= interval_start) & (file['x'] <= interval_end)]

    # Calculate the derivative or rate of change
    x_values = filtered_data['x']
    y_values = filtered_data[variable]
    derivatives = np.gradient(y_values, x_values)

    # Create your plot using matplotlib or any other plotting library
    fig, ax = plt.subplots()
    ax.plot(x_values, derivatives)
    ax.set_xlabel('X')
    ax.set_ylabel('Derivative')
    st.pyplot(fig)  # Display the plot in Streamlit


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
    x_col = st.sidebar.selectbox('Select the column for the x axis', df.columns)
    y_col = st.sidebar.selectbox('Select the column for the y axis', df.columns)

    # Check if the user selected "derivative" for x_col or y_col
    if 'derivative' in [x_col, y_col]:
        # Add additional input fields for derivative calculation
        original_col = st.sidebar.selectbox('Select the original column for the derivative', df.columns)
        interval = st.sidebar.number_input('Select the interval for derivative calculation', min_value=1, value=10)

        # Calculate the derivative
        derivative_values = (df[original_col].shift(-interval) - df[original_col]) / (df[y_col].shift(-interval) - df[y_col])

        # Update the DataFrame with the derivative values
        df['derivative'] = derivative_values

        # Update the y_col selection to include 'derivative'
        y_col_options = list(df.columns)
        y_col = st.sidebar.selectbox('Select the column for the y axis', y_col_options)

    # Create the plot
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    st.pyplot(fig)



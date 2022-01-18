import os
import pandas as pd
import streamlit as st
import plotly.express as px

from traitlets.traitlets import default

from col_type_detector import *
from plots import *
from helpers import *
st.set_option('deprecation.showPyplotGlobalUse', False)

DEFAULT_FILE = 'Iris.csv'

ONE_NUMERIC = ['Histogram', 'Distplot']
ONE_CATEOGIRCAL = ['Donut', 'Pie', 'Histogram']
TWO_NUMERIC = ["Scatter", "Scatter plot with margins", "2D density plot", \
               "Distplot", "Histogram"]
TWO_NUMERIC_SORTED = ['Connected Scatter', "Area plot", "Line plot"]


st.title("Flomaster plot")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv(os.path.join('data_samples',DEFAULT_FILE))

data_types = get_column_types(df, num_unique_categories=2)


st.markdown("## Data Preview")
st.write(df.head(100))

x = st.sidebar.selectbox('Select x axis', ["None"] + list(df.columns))
y = st.sidebar.multiselect("Select columns to use as y axis", ['None'] + list(df.columns), default=["None"])
group_by = st.sidebar.selectbox("Select column representing group", ['None'] + list(df.columns))

x_dtype = get_data_type_for_given_feature(data_types, x)
st.write(f"{x} dtype is {x_dtype}")


if x != "None" and y[0] == 'None':
    if x_dtype == 'numeric':
        plot_type = st.selectbox('Select type of the plot', ONE_NUMERIC)
        fig = one_numeric(df, x, plot_type)
        st.plotly_chart(fig)

    if x_dtype == 'categorical':
        plot_type = st.selectbox('Select type of the plot', ONE_CATEOGIRCAL)
        fig = one_categoric(df, x, plot_type)
        st.plotly_chart(fig)

    if x_dtype == 'texts':
        fig = one_textual(df, x)
        st.pyplot(fig)

if x != "None" and y[0] != 'None':
    if df[x].to_list() == sorted(df[x].to_list()):
        TWO_NUMERIC += TWO_NUMERIC_SORTED
    
    plot_type = st.selectbox('Select type of the plot', TWO_NUMERIC)
    if len(df)>2000 and plot_type in ["Histogram", "Scatter"]:
        st.markdown('**Data has two many rows, we suggest plotting \
            with one on the folowing: "Scatter plot with margins", "2D density plot", "Distplot"**')
    
    if len(df)<2000 and plot_type not in ["Histogram", "Scatter"]:
        st.markdown('**Data has two little rows, we suggest plotting \
            with one on the folowing: "Histogram", "Scatter"**')

            

    fig = two_numeric(df, x, y[0], plot_type)
    st.plotly_chart(fig)


# st.write(get_column_types(df))

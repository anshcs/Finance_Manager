import plots
import invest
import database
from datetime import datetime
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from sklearn import preprocessing
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import torch


def home():
    st.markdown("## Web App to monitor and analyse my personal finance")
    st.markdown("### Working:")
    st.markdown('**The following Web App uses SQL as the backend to store data,** \
                **pyhton has been used to insert data into the database automatically and the plotly library** \
                **has been used to plot interactive plots** \
                **the data set is my real life bank statements which have been downloaded from axis bank website**')
    st.markdown("### Future plans:")
    st.markdown("**I also plan to implement a machine learning model that suggests monthly savings based on current market sentiment and accordingly suggets how much to invest that month**")
    file_month = st.file_uploader(
        label="Insert the current months bank statement", type={"csv"})

    if st.button("Submit csv file"):
        db = database.DataBase(file_month)
        db.CleanData()


st.title('Finance Manager')
st.sidebar.title('Navigation')
opts = st.sidebar.radio(
    'pages', options=['Home', 'PieChart', 'TreeMap', 'BarGraph', 'statistics', 'Saving'])

# have to change to run locally as there is limit on how much data can be added to cloud server
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='financemng',

)
mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM payment_table')
Payment_df = pd.DataFrame(columns=["TranDate", "PARTICULARS",
                                   "PAYMENTS", "Category", "DR", "CR", "BAL", "Month", "tranID"])
for x in mycursor:
    # print(list(x))
    Payment_df.loc[len(Payment_df)] = list(x)

myplot = plots.Plot(Payment_df)
inv = invest.model()


if opts == 'statistics':
    myplot.stats()
elif opts == 'PieChart':
    myplot.PieChart()
elif opts == 'TreeMap':
    myplot.TreeMap()
elif opts == 'BarGraph':
    myplot.bar()
elif opts == 'Home':
    home()
elif opts == 'Saving':
    inv.savings()

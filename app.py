import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def stats(df):
    st.title("Data Statistics:")
    st.write(df.describe())


def PieChart(df):
    st.markdown(
        '### Here we can visualize amount of money spent either based on month or category')

    comparision = st.selectbox(
        'Select comparision based on :', options=['Category', 'Month'])

    labels = {}
    for i in range(len(Payment_df)):
        # print(x)
        if df[f'{comparision}'][i] not in labels.keys():
            labels[df[f'{comparision}'][i]] = 0
        try:
            labels[df[f'{comparision}'][i]] += float(df['DR'][i])
        except:
            labels[df[f'{comparision}'][i]] += 0
    try:
        del labels['Others']
    except:
        pass
    catexp_df = pd.DataFrame({f'{comparision}': list(labels.keys()),
                              'Expense': list(labels.values())})
    fig = px.pie(catexp_df, values='Expense', names=f'{comparision}', hole=.5)
    fig.update_traces(textposition='inside')
    fig.update_layout(title='Expense', uniformtext_minsize=12,
                      uniformtext_mode='hide', width=500, height=900)
    st.plotly_chart(fig, use_container_width=True, height=900, width=500)


def TreeMap(df):

    st.markdown(
        "### Here we can visulaize amount spent on a category for every single month ")
    df = df[df["Category"].str.contains("Others") == False]
    Mon = st.selectbox(
        'Select comparision based on :', options=df['Month'].unique())
    df = df[df["Month"] == f'{Mon}']

    fig = px.treemap(df, path=['Month', 'Category', 'DR'],
                     values='DR', height=900, width=500)
    st.plotly_chart(fig, use_container_width=True, height=900, width=500)


def bar(df):
    month_dict_income = {}
    for i in range(len(df)):
        if df['Month'][i] not in month_dict_income.keys():
            month_dict_income[df['Month'][i]] = 0
        try:
            month_dict_income[df['Month'][i]] += float(df['CR'][i])
        except:
            month_dict_income[df['Month'][i]] += 0
    month_dict_expense = {}
    for i in range(len(df)):
        if df['Month'][i] not in month_dict_expense.keys():
            month_dict_expense[df['Month'][i]] = 0
        try:
            month_dict_expense[df['Month'][i]] += float(df['DR'][i])
        except:
            month_dict_expense[df['Month'][i]] += 0
    inout_df = pd.DataFrame({'Income': list(month_dict_income.values()),
                             'Expense': list(month_dict_expense.values())},
                            index=list(month_dict_income.keys()))
    fig = px.bar(inout_df, x=inout_df.index, y=["Income", "Expense"],
                 title="Income and Expense Monthwise", barmode="group", height=800, width=500)

    st.plotly_chart(fig, use_container_width=True, width=500, height=800)


def home():
    st.markdown("## Web App to monitor and analyse my personal finance")
    st.markdown("### Working:")
    st.markdown('**The following Web App uses SQL as the backend to store data,** \
                **pyhton has been used to insert data into the database automatically and the plotly library** \
                **has been used to plot interactive plots** \
                **the data set is my real life bank statements which have been downloaded from axis bank website**')
    st.markdown("### Future plans:")
    st.markdown("**I also plan to implement a machine learning model that suggests monthly expense based on how much amount can be according to the current market sentiment**")


st.title('Finance Manager')
st.sidebar.title('Navigation')
opts = st.sidebar.radio(
    'pages', options=['Home', 'PieChart', 'TreeMap', 'BarGraph', 'statistics'])


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="financemng"
)
mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM payment_table')
Payment_df = pd.DataFrame(columns=["TranDate", "PARTICULARS",
                                   "PAYMENTS", "Category", "DR", "CR", "BAL", "Month", "tranID"])
for x in mycursor:
    # print(list(x))
    Payment_df.loc[len(Payment_df)] = list(x)


if opts == 'statistics':
    stats(Payment_df)
elif opts == 'PieChart':
    PieChart(Payment_df)
elif opts == 'TreeMap':
    TreeMap(Payment_df)
elif opts == 'BarGraph':
    bar(Payment_df)
elif opts == 'Home':
    home()

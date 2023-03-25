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
import plotly.graph_objects as go
import torch

mont_dict = {1: 'January', 2: 'February', 3: 'march', 4: 'April', 5: 'May', 6: 'June',
             7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November ', 12: 'December'}


items = {"Food": ['ZOMATO', 'Zomato', 'Swiggy', 'SWIGGY', 'Zomato Lt', 'KABAB MEH', 'Kalkata K', 'EatClub', 'MAMATHA M'],
         "Clg canteen": ['BHAGYA M', 'Bhagya', 'Roll magi', 'VINAY KUM', 'Siddharaj', 'Bhagya ', 'TEA COFFE', 'BHAGYA M '],
         'Restraunt': ['CHEF BAKE', 'Kabab Cou', 'C2  Kitch', 'WOW MOMO ', 'Empire Re', 'Plan B - ', 'Dominos P', 'TIPSY BUL''Roll magi', 'DOMINOS P', 'Cookie Ma', 'Theobroma', 'S L V SWE', 'mad over', 'Pizza Hut', 'BOBA TREE', 'THEOBROMA', 'McDonalds', 'TAAZA MIT'],
         'Bills/Phone/internet': ['JioFiber', 'Jio Mobil', 'JIO Mumbai', 'JIOPAY', 'RELIANCE '],
         'Subscription': ['SonyLIV', 'Sony Pict', 'NETFLIX C', 'NETFLIX', 'SPOTIFY'],
         'Amazon/Shopping': ['AMAZON', 'Amazon.in-Gro', 'Amazon Pa', 'Amazon Seller', 'Fossil In', 'Nykaa'],
         'Cab/Auto': ['OLACABS', 'OLA Postp', 'OlaFinanc', 'olamoney1', 'WWW OLACABS C', 'UBER INDI', 'UBER INDIA SY', ],
         'Petrol': ['JRB FUEL ', 'BP Petrol', ' JRB FUEL', 'Indian Oi', 'R R PETRO', 'R R Petro'],
         'Groceries/General': ['Anu Provi', 'Grofers I', 'GROFERS I', 'SWIGGY INSTAM', 'MEGA XPRE', 'JAALAARIS'],
         'Travel/Vacation/Fun': ['IRCTC', 'IRCTC Web', 'MAKEMYTRIP IN', 'airbnb', 'MAKEMYTRIP (I'],
         'clgParking': ['G UMAPATH'],
         'gym': ['THIRUPATH']}

class Plot:
    def __init__(self,df) -> None:
        self.df = df 
    def stats(self):
        st.title("Data Statistics:")
        st.write(self.df.describe())
        st.write("DataBase")
        st.write(self.df)
    def PieChart(self):
        st.markdown(
            '### Here we can visualize amount of money spent either based on month or category')
        year = st.radio("Choose year", ('2022', '2023', 'All'))

        comparision = st.selectbox(
            'Select comparision based on :', options=['Category', 'Month'])

        labels = {}
        
        for i in range(len(self.df)):
            if year == "All":
                
                if self.df[f'{comparision}'][i] not in labels.keys():
                    labels[self.df[f'{comparision}'][i]] = 0
                try:
                    labels[self.df[f'{comparision}'][i]] += float(self.df['DR'][i])
                except:
                    labels[self.df[f'{comparision}'][i]] += 0
            else:
                if (self.df["TranDate"][i].year) == int(year):
                    if self.df[f'{comparision}'][i] not in labels.keys():
                        labels[self.df[f'{comparision}'][i]] = 0
                    try:
                        labels[self.df[f'{comparision}'][i]] += float(self.df['DR'][i])
                    except:
                        labels[self.df[f'{comparision}'][i]] += 0
        try:
            del labels['Others']
        except:
            pass
        catexp_df = pd.DataFrame({f'{comparision}': list(labels.keys()),
                                'Expense': list(labels.values())})
        fig = px.pie(catexp_df, values='Expense',
                    names=f'{comparision}', hole=.5)
        fig.update_traces(textposition='inside')
        fig.update_layout(title='Expense', uniformtext_minsize=12,
                        uniformtext_mode='hide', width=500, height=900)
        st.plotly_chart(fig, use_container_width=True,
                        height=900, width=500)
    def TreeMap(self):
        st.markdown(
            "### Here we can visulaize amount spent on a category for every single month ")
        self.df = self.df[self.df["Category"].str.contains("Others") == False]
        Mon = st.selectbox(
            'Select comparision based on :', options=self.df['Month'].unique())
        self.df = self.df[self.df["Month"] == f'{Mon}']

        fig = px.treemap(self.df, path=['Month', 'Category', 'DR'],
                        values='DR', height=900, width=500)
        st.plotly_chart(fig, use_container_width=True, height=900, width=500)
    def bar(self):
        year = st.radio("Choose year", ('2022', '2023', 'All'))
        month_dict_income = {}
        month_dict_expense = {}
        if year == "All":
            for i in range(len(self.df)):
                if self.df['Month'][i] not in month_dict_income.keys():
                    month_dict_income[self.df['Month'][i]] = 0
                try:
                    month_dict_income[self.df['Month'][i]] += float(self.df['CR'][i])
                except:
                    month_dict_income[self.df['Month'][i]] += 0

            for i in range(len(self.df)):
                if self.df['Month'][i] not in month_dict_expense.keys():
                    month_dict_expense[self.df['Month'][i]] = 0
                try:
                    month_dict_expense[self.df['Month'][i]] += float(self.df['DR'][i])
                except:
                    month_dict_expense[self.df['Month'][i]] += 0
        else:
            for i in range(len(self.df)):
                if self.df['TranDate'][i].year == int(year):
                    if self.df['Month'][i] not in month_dict_income.keys():
                        month_dict_income[self.df['Month'][i]] = 0
                    try:
                        month_dict_income[self.df['Month'][i]] += float(self.df['CR'][i])
                    except:
                        month_dict_income[self.df['Month'][i]] += 0
            # month_dict_expense = {}
            for i in range(len(self.df)):
                if self.df['TranDate'][i].year == int(year):
                    if self.df['Month'][i] not in month_dict_expense.keys():
                        month_dict_expense[self.df['Month'][i]] = 0
                    try:
                        month_dict_expense[self.df['Month'][i]] += float(self.df['DR'][i])
                    except:
                        month_dict_expense[self.df['Month'][i]] += 0

        inout_df = pd.DataFrame({'Income': list(month_dict_income.values()),
                                'Expense': list(month_dict_expense.values())},
                                index=list(month_dict_income.keys()))
        fig = px.bar(inout_df, x=inout_df.index, y=["Income", "Expense"],
                    title="Income and Expense Monthwise", barmode="group", height=800, width=500)

        st.plotly_chart(fig, use_container_width=True, width=500, height=800)
        
        
        
    
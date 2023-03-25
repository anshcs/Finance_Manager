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

class DataBase:
    def __init__(self,filemonth) -> None:
        self.host = "localhost"
        self.user="root"
        self.password=""
        self.database="financemng"
        self.filemonth = filemonth
    def CleanData(self):
        st.write(self.file_month)
        start = False
        count = 0

        for line in self.file_month:
            if start:
                if line == b'\n':
                    break
                else:
                    decLine = line.decode("utf-8")
                    row = decLine.split(",")
                    df.loc[len(df)] = row
                    
                    count += 1
            if not start:
                if count > 17:
                    start = True
                    decLine = line.decode("utf-8")
                    
                    cols = decLine.split(",")
                    df = pd.DataFrame(columns=cols)
                    
                count += 1
        df.insert(7, 'Month', True)
    # adding which month it is ->

        for i in range(len(df['Tran Date'])):
            date = datetime.strptime(df['Tran Date'][i], '%d-%m-%Y').date()

            df['Month'][i] = mont_dict.get(date.month)
        df.insert(3, 'PAYMENTS', True)
        df.insert(4, 'PAYMENT_CAT', True)
        for i in range(len(df['PARTICULARS'])):
            if df['PARTICULARS'][i][0] == 'U':
                s = df['PARTICULARS'][i][21:]
                c = df['PARTICULARS'][i][4:]
                s = s[0:s.rfind('/')]
                df['PAYMENTS'][i] = s[0:s.rfind('/')]
                c = c[0:c.rfind('/')]
                c = c[0:c.rfind('/')]
                c = c[0:c.rfind('/')]
                if c[0:c.rfind('/')] == 'P2A':
                    df['PAYMENT_CAT'][i] = 'Friend/Person'
                else:
                    df['PAYMENT_CAT'][i] = 'Merchant/business'

            elif df['PARTICULARS'][i][0:4] == 'ECOM':
                s = df['PARTICULARS'][i][9:]
                s = s[0:s.rfind('/')]
                s = s[0:s.rfind('/')]
                df['PAYMENTS'][i] = s[0:s.rfind('/')]
            elif df['PARTICULARS'][i][0:3] == 'ATM':
                df['PAYMENTS'][i] = 'ATM transc'
            else:
                df['PAYMENTS'][i] = 'others'
        df.insert(5, 'Category', True)
        for i in range(len(df['PAYMENTS'])):
            if df['PAYMENTS'][i] in items.get('Food'):
                df['Category'][i] = 'Food'
            elif df['PAYMENTS'][i] in items.get("Clg canteen"):
                df['Category'][i] = "Clg canteen"
            elif df['PAYMENTS'][i] in items.get('Restraunt'):
                df['Category'][i] = 'Restraunt'
            elif df['PAYMENTS'][i] in items.get('Bills/Phone/internet'):
                df['Category'][i] = 'Bills/Phone/internet'
            elif df['PAYMENTS'][i] in items.get('Subscription'):
                df['Category'][i] = 'Subscription'
            elif df['PAYMENTS'][i] in items.get('Amazon/Shopping'):
                df['Category'][i] = 'Amazon/Shopping'
            elif df['PAYMENTS'][i] in items.get('Cab/Auto'):
                df['Category'][i] = 'Cab/Auto'
            elif df['PAYMENTS'][i] in items.get('Food'):
                df['Category'][i] = 'Food'
            elif df['PAYMENTS'][i] in items.get('Petrol'):
                df['Category'][i] = 'Petrol'
            elif df['PAYMENTS'][i] in items.get('Groceries/General'):
                df['Category'][i] = 'Groceries/General'
            elif df['PAYMENTS'][i] in items.get('Travel/Vacation/Fun'):
                df['Category'][i] = 'Travel/Vacation/Fun'
            elif df['PAYMENTS'][i] in items.get('clgParking'):
                df['Category'][i] = 'clgParking'
            else:
                df['Category'][i] = 'Others'
        
        self.ConnectDb(df)
        st.write(df)
        
        
    def ConnectDb(self,df):
        mydb = mysql.connector.connect(self.host,self.user,self.password,self.database)
        mycursor = mydb.cursor()
        for i in range(len(df['Tran Date'])):
            df['Tran Date'][i] = datetime.strptime(
                df['Tran Date'][i], '%d-%m-%Y').date()
        # mycursor.execute("CREATE TABLE Payment_Table(TranDate DATE,PARTICULARS VARCHAR(100),PAYMENTS VARCHAR(20),Category VARCHAR(20),DR FLOAT(10,2),CR FLOAT(10,2),BAL FLOAT(10,2),Month VARCHAR(10),tranID int PRIMARY KEY AUTO_INCREMENT)")
        for i in range(len(df['Tran Date'])):
            sql = f"INSERT INTO payment_table(TranDate,PARTICULARS,PAYMENTS,Category,DR,CR,BAL,Month) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            val = [df['Tran Date'][i], df['PARTICULARS'][i], df['PAYMENTS'][i],
                df['Category'][i], df['DR'][i], df['CR'][i], df['BAL'][i], df['Month'][i]]
            mycursor.execute(sql, val)
            mydb.commit()
            
    
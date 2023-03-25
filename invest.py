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
from webdriver_manager.chrome import ChromeDriverManager




class model:
    def __init__(self) -> None:
        self.path =  wd.Chrome(ChromeDriverManager().install())
        self.site = "https://www.reuters.com/site-search/?query=sensex&offset=0"
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.mod = AutoModelForSequenceClassification.from_pretrained(
        "ProsusAI/finbert")
        
    def savings(self):
        st.write("Sentiment analysis of current stock market (nifty/sensex)")
        predictions = self.CalculatePrediction()
        predictions['positive'] = sum(predictions['positive'])
        predictions['negative'] = sum(predictions['negative'])
        predictions['neutral'] = sum(predictions['neutral'])
        pred_df = pd.DataFrame(predictions, index=[0])
        fig = go.Figure()
        for column in pred_df.columns:
            fig.add_trace(go.Bar(
                x=pred_df[column],
                y=pred_df.index,
                name=column,
                orientation='h',

            ))
        fig.update_layout(barmode='relative',
                        height=200,
                        width=700,
                        yaxis_autorange='reversed',
                        bargap=0.01,
                        legend_orientation='h',
                        legend_x=-0.05, legend_y=1.1
                        )
        st.plotly_chart(fig)
        
    
    def CalculatePrediction(self):
        pred_dict = {}
        pred_dict['positive'] = []
        pred_dict['negative'] = []
        pred_dict['neutral'] = []
        data = self.WebScrape()
        for i in data :
            pred = self.Prediciton(i)
            pred_dict['positive'].append(pred[0])
            pred_dict['negative'].append(pred[1])
            pred_dict['neutral'].append(pred[2])
        return pred_dict 
    
    def Prediciton(self,text):
        inputs = self.tokenizer(text,return_tensors="pt")
        with torch.no_grad():
            logits = self.mod(**inputs).logits
        predicted_class_id = logits.argmax().item()
        return preprocessing.normalize(logits)[0]
            
        
    def WebScrape(self):
        driver = self.path
        driver.get(self.site)
        # div = driver.find_elements(by=By.CLASS_NAME,value="text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_6__1qUJ5 heading__base__2T28j heading__heading_6__RtD9P media-story-card__heading__eqhp9")
        div = driver.find_elements(by=By.CSS_SELECTOR, value='span')
        time = driver.find_elements(by=By.CSS_SELECTOR, value='time')
        i = 15
        j = 0
        data = []
        while i < len(div) and j < len(time):
            data.append(div[i].text)
            # print(div[i].text,i,"    ",time[j].text)
            # print("_______________")
            i = i + 4
            j += 1

        driver.quit()
        return data
            
        
        
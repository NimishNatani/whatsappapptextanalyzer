import streamlit as st
import numpy as np
import seaborn as sns
import pandas as pd
import re

def gettimedate(string):
    string = string.split(',')
    date,time = string[0],string[1]
    time=time.split('-')
    time =time[0].strip()
    return date+" "+time

def getString(text):
    return text.split('\n')[0]

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].apply(lambda text: gettimedate(text))
    df.rename(columns={'message_date': 'Date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
      entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
    if len(entry) > 1:
        user = entry[1].strip()
        message_text = entry[2].strip() if len(entry) > 2 else ''
    else:
        user = 'Group Notification'
        message_text = entry[0].strip()

    users.append(user)
    messages.append(message_text)

    # Apply additional string processing if needed
    df['Message'] = df['Message'].apply(lambda text: getString(text))

    df = df.drop(['user_message'], axis=1)
    df = df[['Message', 'Date', 'User']]

    # Convert the 'Date' column to datetime, handling errors by coercing invalid dates to NaT
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows where 'Date' is NaT (if any)
    df = df.dropna(subset=['Date'])

    # Extract date components
    df['Only Date'] = df['Date'].dt.date
    df['Year'] = df['Date'].dt.year
    df['Month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Day_name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    return df


import re
import pandas as pd
import snscrape.modules.twitter as snt
import yfinance as yf
from datetime import date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia
import datetime

# Will be used for cleaning data(tweet.content) s is a string.
def filter(s):
    whitespace = re.compile(r"\s+")
    web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
    user = re.compile(r"(?i)@[a-z0-9_]+")
    
    s = whitespace.sub(' ', s)
    s = web_address.sub('', s)
    s = user.sub('', s)
    return s

def out(ticker,c_name,start_date,end_date):
    tweets=[]
    limit=500
    if ticker in ['GOOG','GOOGL']:
        c_name='Google'
    if ticker=='FB':
        c_name='Meta'
    i_date=start_date

    n=(end_date-start_date).days
    for i in range(n):
        query=f'({c_name[0]} OR {ticker})'+f' lang:en until:{i_date}'
        i_date+=datetime.timedelta(days=1)
        pro_sum_for_day=0
        for tweet in snt.TwitterSearchScraper(query).get_items():
            sentiment_model = sia()
            TEXT=filter(tweet.renderedContent)
            vs = sentiment_model.polarity_scores(TEXT)
            pro_sum_for_day+=vs['compound']
            limit=limit-1
            if(limit<=0):
                break
        if(i_date==end_date):
            break
        i1_date=i_date+datetime.timedelta(days=1)
        tckr=yf.Ticker(ticker)
        tckr_stock=tckr.history(start=i_date.strftime('%Y-%m-%d'),end=i1_date.strftime('%Y-%m-%d'), interval='60m').reset_index()
        nnn=pro_sum_for_day/500
        tweets.append([tweet.date,nnn,tckr_stock['Close'].mean()])
    final_data=pd.DataFrame(tweets,columns=['Date','Probability','Predicter'])
    final_data.to_csv(f'static/{ticker}.csv',index=False)
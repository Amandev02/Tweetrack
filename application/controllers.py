from flask import current_app as app
from flask import render_template,request,redirect
import pandas as pd
from .ml import out
from datetime import date
import snscrape.modules.twitter as snt

date_format="%Y-%m-%d"
td=pd.read_csv('static/tickers.csv')

@app.route('/',methods=['GET','POST'])
def index():
    rows=[]
    ll=[5509,2421,3828,13,1992,330,847,3663]
    for i in ll:
        ti_name=td.iloc[i,2]+' - '+td.iloc[i,1]
        sector=td.iloc[i,3]+' - '+td.iloc[i,4]
        rows.append([ti_name,sector,td.iloc[i,1]])
    if request.method=='GET':
        return render_template('index.html',rows=rows,warning=0)
    
    else:
        query=request.form['query'].upper()
        l2=list(td['Ticker'])
        if query not in l2:
            return render_template('index.html',rows=rows,warning=1)
        if query in l2:
            ticker=query
        return redirect(f'/{ticker}')


@app.route('/<string:ticker>',methods=["GET","POST"])
def det_view(ticker):
    com_name=td[td['Ticker']==ticker].iloc[0,2].strip()
    c_name=com_name.split(' ')
    s_date=date(2022,1,1)
    e_date=date(2022,4,23)
    if request.method=="GET":
        num=out(ticker=ticker,c_name=c_name,start_date=s_date,end_date=e_date)
        return render_template('view.html',ticker=ticker,com_name=com_name+' - '+ticker)
    if request.method=="POST":
        s_date = request.form['start_date'].strftime('%Y-%m-%d')
        e_date = request.form['end_date'].strftime('%Y-%m-%d')
    return render_template('view.html',ticker=ticker,com_name=com_name+' - '+ticker)
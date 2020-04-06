import streamlit as st
import datetime
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px

import pytz
from datetime import datetime, timedelta

#tmz = pytz.timezone('US/Samoa')
#now = datetime.now().astimezone(tmz)

# GET CURRENT AND PAST DATE
cdt = datetime.now()
pdt = cdt - timedelta(days=1)

dt1 = cdt.strftime("%m-%d-%Y")
dt2 = pdt.strftime("%m-%d-%Y")

# DATES ARE NOT CREATE TWO URLS (SOME TIMES LATEST FILE IS FROM YESTERDAY)

DATA_COLUMN = 'Deaths'
DATA_URL1 = str('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/')+str(dt1)+str('.csv')
DATA_URL2 = str('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/')+str(dt2)+str('.csv')
#DATA_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-29-2020.csv'

#print(DATA_URL)

@st.cache
def plotData():

        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
                counties = json.load(response)
        try:
                df = pd.read_csv(DATA_URL1, dtype={"FIPS": str})
        except:
                df = pd.read_csv(DATA_URL2, dtype={"FIPS": str})

        df.rename(columns={"FIPS":"CountyCode", "Admin2":"County", "Province_State":"State", "Lat":"lat", "Long_":"lon", "Confirmed":"Infections", "Recovered":"Recoveries"}, inplace=True)


        dfu = df[df.Country_Region == "US"]
        #dfu = df[(df['CountyCode'] >= 1000) & (df['CountyCode'] <= 99999)]
        dfv = dfu[['CountyCode','County','State','Last_Update','lat','lon','Infections','Deaths','Recoveries']]
        dfw = dfv[dfv.Deaths > 0]

        dfx = dfw.sort_values(by=['Deaths', 'CountyCode'], ascending=False)


        #maxDeaths = dfx['Deaths'].max()
        maxDeaths = 100

        fig = px.choropleth(dfx, geojson=counties, locations='CountyCode', color='Deaths',
                           color_continuous_scale=px.colors.sequential.Reds,
                           range_color=(0, maxDeaths),
                           scope="usa",
                           labels={'Deaths':'Scale'}
                          )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


        return fig, dfx

fig, dfx = plotData()

TITLE = str('Total CoVID Deaths in the US = ')+str(dfx['Deaths'].sum())

st.title(TITLE)
st.plotly_chart(fig, use_container_width=True)
st.write(dfx[['State','County','Infections','Deaths','Recoveries']])
dt2 = pdt.strftime("%m-%d-%Y")
st.text(str('AdelleTech. heat map rendered by Murali Behara on ')+cdt.strftime("%Y-%m-%d %H:%M:%S")+str(', data: Johns Hopkins'))

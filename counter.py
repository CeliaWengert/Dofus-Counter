import pandas as pd
import streamlit as st
from datetime import datetime as dt
import pytz
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


URI_SQLITE_DB = "counter.db"

def get_connection(path: str):
    return sqlite3.connect(path, check_same_thread=False)

def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS inc
            (
                Name TEXT NOT NULL,
                Date TEXT NOT NULL,
                Challenge_name TEXT,
                Challenge_count INT
            );"""
    )
    conn.commit()



st.set_page_config(page_title="Dofus incrément", layout="wide",page_icon = 'ico.png')

st.markdown(
    """<style>
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    .css-10trblm {color : #83C9FF;}
    .css-1yk9tp8 {display: none}
    button[title="View fullscreen"]{visibility: hidden;}
    table
    {
        width: 100%;
        color: #68BEBA;
        text-align:right;
        background-color: #011b32;
    }
    footer {visibility: hidden;}
    </style>""", unsafe_allow_html=True)
col1,col2=st.columns([0.08,2])
with col1:
    st.markdown('')
    st.markdown('')
    st.image('ico.png', use_column_width='auto')
    
with col2:
  st.markdown(f'<p style="color:#83C9FF;font-size:75px;">{"Dofus incrément"}</p>', unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------------------------------------------------------
conn = get_connection(URI_SQLITE_DB)
cur=conn.cursor()
init_db(conn)

select1=st.selectbox('Selection du noob', ('Antoine','Aurélien','Hugo','Maxime'))
df_chall=pd.read_csv('chall.csv') 
select2=st.selectbox('Selection du challenge',df_chall)


if st.button('Incrément !'):
   #"YYYY-MM-DD HH:MM:SS.SSS"
    date=dt.now(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%dT%H:%M:%S")
    request = '''INSERT INTO inc(Name,Date,Challenge_Name,Challenge_count) VALUES("'''+select1+'''","'''+date+'''","'''+select2+'''",1)'''
    
    conn.execute(request)
    conn.commit()
    
chart_data = pd.read_sql_query("SELECT Count(*) as Noob_Counter, Name from inc group by Name ", conn)
st.bar_chart(chart_data,x="Name",y="Noob_Counter")

pie_data=pd.read_sql_query("SELECT Count(*) as Chall_Counter, Name from inc group by Challenge_name ", conn)
fig = px.pie(pie_data, values='Chall_Counter', names='Challenge_name')
st.plotly_chart(fig,use_container_width=True)

df=pd.read_sql_query("SELECT * from inc ", conn)
st.dataframe(df)

    


    

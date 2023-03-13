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
csvfile = "bdd.csv"

def get_connection(path: str):
    return sqlite3.connect(path, check_same_thread=False)

def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS inc
            (   ROWID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Date TEXT NOT NULL,
                Challenge_name TEXT
                
            );"""
    )
    conn.commit()
    #df=pd.read_csv(csvfile,delimiter=";")
    #st.dataframe(df,use_container_width=1)
    
    df.to_sql("inc", conn, if_exists='append', index=False)
    conn.commit()
    



st.set_page_config(page_title="Dofus incrément", layout="wide",page_icon = 'ico.png')
#83C9FF
st.markdown(
    """<style>
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    .css-10trblm {color : #0E853F;}
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
  st.markdown(f'<p style="color:#0E853F;font-size:75px;">{"Dofus incrément"}</p>', unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------------------------------------------------------
conn = get_connection(URI_SQLITE_DB)
cur=conn.cursor()
init_db(conn)

select1=st.selectbox('Selection du noob', ('Antoine','Aurélien','Hugo','Maxime'))
df_chall=pd.read_csv('chall.csv') 
select2=st.selectbox('Selection du challenge',df_chall)


if st.button('Incrément !'):
   #"YYYY-MM-DD HH:MM:SS.SSS"
    date=dt.now(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%d %H:%M:%S")
    request = '''INSERT INTO inc(Name,Date,Challenge_Name) VALUES("'''+select1+'''","'''+date+'''","'''+select2+'''")'''
    
    conn.execute(request)
    conn.commit()
    
chart_data = pd.read_sql_query("SELECT Count(*) as Noob_Counter, Name from inc group by Name ", conn)
st.bar_chart(chart_data,x="Name",y="Noob_Counter")

pie_data=pd.read_sql_query("""SELECT Count(*) as Chall_Counter, Challenge_name from inc Where Challenge_name <> \'-\' group by Challenge_name""", conn)
fig = px.pie(pie_data, values='Chall_Counter', names='Challenge_name')
st.plotly_chart(fig,use_container_width=True)

inp = st.text_input('Entrer le numéro d\'une ligne à supprimer (ROWID)', '')
if st.button('Supprimer'):
    request = '''DELETE FROM INC WHERE ROWID = ''' + inp
    conn.execute(request)
    conn.commit()

df=pd.read_sql_query("SELECT * from inc order by ROWID DESC", conn)

st.dataframe(df,use_container_width=1)

    


    

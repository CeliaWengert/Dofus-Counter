import pandas as pd
import streamlit as st
from datetime import datetime as dt
import pytz
from pathlib import Path
import sqlite3
from sqlite3 import Connection


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


def build_sidebar(conn: Connection):
    st.sidebar.header("Configuration")
    input1 = st.sidebar.slider("Input 1", 0, 100)
    input2 = st.sidebar.slider("Input 2", 0, 100)
    if st.sidebar.button("Save to database"):
        conn.execute(f"INSERT INTO inc(Name,Date,Challenge_Name,Challenge_count) VALUES ('Hugo',dt.now(pytz.timezone(\'Europe/Paris\')),'Nomade',1);")
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
init_db(conn)

st.selectbox1('Selection du noob', ('Antoine','Aurélien','Hugo','Maxime'))
df=pd.read_csv('chall.csv') 
st.selectbox2('Selection du challenge',df)

#build_sidebar(conn)

if st.button('Incrément'):
    request = 'INSERT INTO inc(Name,Date,Challenge_Name,Challenge_count) VALUES("Hugo",dt.now(pytz.timezone(\'Europe/Paris\')),"Nomade",1);'
    conn.execute(request)
    conn.commit()
else:
    st.write('coinc')


    

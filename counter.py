import pandas as pd
import streamlit as st
import time

import sqlite3
conn = sqlite3.connect('counter.db')
c = conn.cursor()

request='CREATE TABLE [IF NOT EXISTS] [counter.db].inc(Name TEXT NOT NULL, Date TEXT NOT NULL, Challenge_name TEXT, challenge_count INTEGER, table_constraints) [WITHOUT ROWID]'

c.execute(request)

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


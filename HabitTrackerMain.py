import pandas as pd, pandas_datareader as web, numpy as np, seaborn as sns, streamlit as st,os,re, random, datetime
from streamlit import session_state as ss
from PIL import Image
st.set_page_config(layout='wide',page_title='Habit & Goal Tracker')#,page_icon='icon.png')

#%% Sidebar
page = st.sidebar.radio("Select page",['Setup','Daily entry','Dashboard'],index=1)

st.write("Hello")
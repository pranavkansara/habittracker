import pandas as pd, pandas_datareader as web, numpy as np, seaborn as sns, streamlit as st,os,re, random, datetime
from streamlit import session_state as ss
from PIL import Image
st.set_page_config(layout='wide',page_title='Habit & Goal Tracker')#,page_icon='icon.png')

#%% Sidebar
page = st.sidebar.radio("Select page",['Setup','Daily entry','Dashboard'],index=1)

st.write("Hello")

if os.path.exists('goaldf.pkl'):
    goaldf  = pd.read_pickle('goaldf.pkl')
    goaldf['Category'] = 'Physical'
    goaldf = goaldf[['Date','Goal','Category','Target Unit','Target','Timeline']]
    goaldf.to_pickle('goaldf.pkl')
else:
    goaldf = pd.DataFrame({'Date':np.datetime64, 'Goal':'str','Category':'str','Target Unit':np.number,'Target':'str','Timeline':np.datetime64},index=[])
# only specify non-text types below
goaldisptypes = {'Date':'date', 'Category':['Physical','Mental','Emotional','Spiritual','Financial','Family'],'Target':'number','Timeline':'date'}

st.write(goaldf)
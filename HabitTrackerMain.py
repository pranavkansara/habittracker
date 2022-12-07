import pandas as pd,numpy as np, streamlit as st,os,re, random, datetime
from streamlit import session_state as ss
from PIL import Image
import ufn_importdata as imp
from Authenticate import ufn_Authenticate,authenticateactions
from WriteHomePage import WriteHomePage 
from streamlit import session_state as ss
from streamlit_option_menu import option_menu
from custom_style_streamlit import style
from Setup import Setup
from DailyEntry import DailyEntry
from Dashboard import Dashboard
sty = style()

st.set_page_config(layout='wide',page_title='Habit & Goal Tracker')#,page_icon='icon.png')
st.markdown(sty.STYLE,unsafe_allow_html=True)

authenticator,config = ufn_Authenticate()
#%% Sidebar
#page = st.sidebar.radio("Select page",['Setup','Daily entry','Dashboard'],index=1)
c1,c2 = st.columns(2)

if ss.authentication_status:
    c1,c2,c3 = st.columns([5,5,1])
    with c3:
        authenticator.logout('Logout', 'main')
    action = option_menu(None, ["Home","Setup", "Daily Entry","Dashboard","Settings"], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa","border-color":"black"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "navy"},
    }
    )
    goaldf,goaldisptypes,habitdf,habitdisptypes,habitdailydf = imp.DataPrep()
    if action=='Home':
        WriteHomePage(goaldf,habitdf,habitdailydf)
    elif action =='Setup':
        Setup(goaldf,goaldisptypes,habitdf,habitdisptypes,habitdailydf)
    elif action == 'Daily Entry':
        DailyEntry(habitdf,habitdailydf)
    elif action == 'Dashboard':
        Dashboard(goaldf,goaldisptypes,habitdf,habitdisptypes,habitdailydf)

elif ss.authentication_status == False:
    c1.error('Username/password is incorrect')
elif ss.authentication_status == None:
    c1.warning('Please enter your username and password')

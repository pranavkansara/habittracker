# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:28:15 2022

@author: PRANA
"""
import pandas as pd,numpy as np, streamlit as st,os,re, random, datetime
from streamlit import session_state as ss

import ufn_importdata as imp

def DailyEntry(habitdf,habitdailydf):
    # st.write(habitdailydf.tail(5))

    st.subheader("Daily entries")
    dt = st.date_input("Enter date")
        
    with st.form('Enter todays values',clear_on_submit=True):
        c = st.columns(4)
        try:
            currentries = habitdailydf.loc[dt]
            currentries[currentries.isnull()] = ''
        except:
            currentries = []
        st.write('**Achievement for the day**')
        c = st.columns(4)
        j=0
        finalvals = []
        for i,v in habitdf.iterrows():
            txt = v['Habit']+': ('+ str(v['Target'])+' '+v['Target Unit']+' '+v['Frequency']+')'
            if len(currentries)>0:
                val = currentries[v['Habit']]
            else:
                val = ''
            finalvals.extend([c[(j+1)-1].text_input(txt,key='ach'+str(i),value=val)])
            if (i+1)%4==0:
                j=0
            else:
                j+=1
            
        st.write('---')
        st.write('**Additional comments**')
        c = st.columns(4)
        def getval(field):
            try:
                val = currentries[field]
            except:
                val = ''
            return val
            if currentries == []:
                return ''
            else:
                return currentries[field].iloc[0]

        finalvals.extend([c[0].text_input('Books read:',value=getval('Books'))])
        finalvals.extend([c[1].text_input('Articles read:',value=getval('Articles'))])
        finalvals.extend([c[2].text_input('Food:',value=getval('Food'))])
        finalvals.extend([c[3].text_input('Spiritual activites:',value=getval('Spiritual'))])
        finalvals.extend([c[0].text_input('Hobby related:',value=getval('Hobby'))])
        finalvals.extend([c[1].text_input('Family time:',value=getval('Family'))])
        finalvals.extend([c[2].text_input('Key Projects',value=getval('Projects'))])
        finalvals.extend([c[3].text_input('Miscellenous',value=getval('Miscellenous'))])
        st.write('---')
        finalvals.extend([st.text_input('Summary of the day',value=getval('Summary'))])
        st.write('---')
        submit = st.form_submit_button()
        if submit:
            st.write('Success!!')
            habitdailydf.loc[dt] = finalvals
            habitdailydf.to_pickle('./Data/habitdailydf.pkl')


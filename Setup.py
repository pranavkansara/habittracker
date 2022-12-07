# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:13:18 2022

@author: PRANA
"""
import pandas as pd,numpy as np, streamlit as st,os,re, random, datetime
from streamlit import session_state as ss

import ufn_importdata as imp

def Setup(goaldf,goaldisptypes,habitdf,habitdisptypes,habitdailydf):

    def DisplayNCreateTable(df,disptypes,exportname,mandatorycolname):
        with st.form('userentry'):
            c = st.columns(6)
            finalvals = []
            currentries = len(df[df[mandatorycolname]!=''])
            defaultentries = 10 if currentries==0 else currentries
            numentries = st.sidebar.number_input("# of entries",currentries,30,defaultentries)
            for i in range(numentries):
                # populate previously entered values
                if i<len(df):
                    vals = df.loc[i].values
                else:
                    vals = ['' for x in df.columns]
                # Get new values and update dataframe again
                columns = df.columns.tolist()
                # for each row, gather the value of columns in a list
                interimvals = []
                for j,x in enumerate(df.columns):
                    x_disptype = disptypes.get(x,'text')
                
                    if x_disptype == 'date':
                        if vals[j]=='':
                            val = c[j].date_input(x,key=x+str(i))
                        else:
                            val = c[j].date_input(x,key=x+str(i),value=vals[j])
                    elif x_disptype == 'number':
                        if vals[j]=='':
                            val = c[j].number_input(x,key=x+str(i))
                        else:
                            val = c[j].number_input(x,key=x+str(i),value=vals[j])
                        
                    elif type(x_disptype) == list:
                        if vals[j]!='':
                            val = c[j].selectbox(x,x_disptype,key=x+str(i),index=x_disptype.index(vals[j]))
                        else:
                            val = c[j].selectbox(x,x_disptype,key=x+str(i))
                    else:
                        val = c[j].text_input(x,key=x+str(i),value=vals[j])
                    interimvals.extend([val])
                        
                # if the first value is non-null then append it in the finalvals
                mandatorycolidx = columns.index(mandatorycolname)
                if interimvals[mandatorycolidx]!='':
                    finalvals.append(interimvals)
            submit = st.form_submit_button()
            if submit:
                finaldf = pd.DataFrame(finalvals,columns=columns)
                finaldf.to_pickle(exportname)
                st.write('Success!!')
                return finaldf
            
    subpage = st.selectbox('Select subpage',['Goals','Habits'])
    if subpage=='Goals':
        goaldf = DisplayNCreateTable(goaldf,goaldisptypes,'goaldf.pkl',mandatorycolname='Goal')
        
    elif subpage == 'Habits':
        habitdf = DisplayNCreateTable(habitdf,habitdisptypes,'habitdf.pkl',mandatorycolname='Habit')
        st.write(habitdf)
            
        if sum(habitdf['Weightage'])>100:
            st.write('Sum of weightage exceeds 100%, hence weights will be normalized to sum up to 100% in same ratio.')
            habitdf['Weightage'] = habitdf['Weightage']*100/sum(habitdf['Weightage'])
            habitdf.to_pickle('habitdf.pkl')
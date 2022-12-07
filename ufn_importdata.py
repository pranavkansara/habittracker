# -*- coding: utf-8 -*-
import pandas as pd,numpy as np, streamlit as st,os,re, random, datetime
def DataPrep():
    if os.path.exists('./Data/goaldf.pkl'):
        goaldf  = pd.read_pickle('./Data/goaldf.pkl')
        goaldf['Category'] = 'Physical'
        goaldf = goaldf[['Date','Goal','Category','Target Unit','Target','Timeline']]
        goaldf.to_pickle('./Data/goaldf.pkl')
    else:
        goaldf = pd.DataFrame({'Date':np.datetime64, 'Goal':'str','Category':'str','Target Unit':np.number,'Target':'str','Timeline':np.datetime64},index=[])
    # only specify non-text types below
    goaldisptypes = {'Date':'date', 'Category':['Physical','Mental','Emotional','Spiritual','Financial','Family'],'Target':'number','Timeline':'date'}
    
    if os.path.exists('./Data/habitdf.pkl'):
        habitdf  = pd.read_pickle('./Data/habitdf.pkl')
    else:
        habitdf = pd.DataFrame({'Habit':'str','Related Goal':'str','Target Unit':'str','Target':np.number,'Frequency':'str','Weightage':np.number},index=[])
    # only specify non-text types below
    habitdisptypes = {'Related Goal':['None']+goaldf['Goal'].unique().tolist(),'Target':'number','Frequency':['Daily','Weekly','Monthly'],'Weightage':'number'}
        
    if os.path.exists('./Data/habitdailydf.pkl'):
        habitdailydf  = pd.read_pickle('./Data/habitdailydf.pkl')
    else:
        if os.path.exists('./Data/habitdf.pkl'):
            cols = habitdf['Habit'].values.tolist()
            cols.extend(['Books','Articles','Food','Spiritual','Hobby','Family','Projects','Miscellenous','Summary'])
            cols.insert(0,'Date')
            habitdailydf = pd.DataFrame(columns=cols)
            habitdailydf.set_index('Date',inplace=True)
    
        
    return goaldf,goaldisptypes,habitdf,habitdisptypes,habitdailydf
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:29:40 2022

@author: PRANA
"""
import pandas as pd,numpy as np, streamlit as st,os,re, random, datetime, pendulum
from streamlit import session_state as ss
import ufn_importdata as imp
import plotly.graph_objects as go,plotly.express as px, pandas as pd, numpy as np
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

# st.write(habitdailydf)
# st.write(habitdf)
def Dashboard(goaldf,goaldisptypes,habitdf,habitdisptypes,habitdailydf):    
    import pandas as pd
    # subpage = st.selectbox('Select subpage',['Goal tracking','Activity tracking'],index=1)
    subpage = option_menu(None, ["Goal tracking","Activity tracking"], 
    icons=['house', 'cloud-upload'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa","border-color":"black"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "navy"},
    }
    )
    if subpage == 'Goal tracking':
        a=1
    elif subpage == 'Activity tracking':
        # selhabit = st.selectbox("Select activity",habitdf['Habit'],key='habits')
        # selhabitvals = habitdailydf[selhabit]
        # st.write(selhabitvals)
        # n = st.number_input("Number of days",5,100,30)
        # st.bar_chart(habitdailydf[selhabit][:n])

        # c1,c2,c3 = st.columns([5,1,5])
        # for i,habit in enumerate(habitdf['Habit']):
        #     c = c1 if (i+1)%2 == 0 else c3
        #     c.subheader(habit)
        #     c.bar_chart(habitdailydf[habit][:n])
        st.write(habitdailydf)
        kpi = {}
        kpisummarypl = st.empty()
        kpisummarypl1 = st.empty()
        for i,row in habitdf[['Habit','Frequency','Target Unit','Target']].iterrows():
            habit,freq,unit,target = row
            st.subheader(habit+' ('+freq+' '+str(target)+' '+unit+')')

            dailyhist = habitdailydf[habit].reset_index()
            dailyhist[habit] = daillyhist[habit].astype(float)
            dailyhist['Date']= pd.to_datetime(dailyhist['Date'])
            dailyhist['Startofweek'] = dailyhist['Date'].apply(lambda x: pendulum.date(x.year,x.month,x.day).start_of('week'))
            dailyhist['Month'] = dailyhist['Date'].dt.strftime('%Y-%m')
            
            if freq == 'Weekly':
                hist = dailyhist.groupby('Startofweek')[habit].sum().reset_index()
                hist.rename(columns={'Startofweek':'Date',habit:'Actual'},inplace=True)
            elif freq == 'Monthly':
                hist = dailyhist.groupby('Month')[habit].sum().reset_index()
                hist.rename(columns={'Month':'Date'},inplace=True)
            else:
                hist = dailyhist
            hist.rename(columns={habit:'Actual'},inplace=True)
            hist['Date'] = pd.to_datetime(hist['Date']).dt.date
            hist.set_index('Date',inplace=True)
            hist['Target'] = target
            
            l1 = go.Layout(height=300, width=500,
                title_text=habit,
                plot_bgcolor='white',
                showlegend=True,
                xaxis=dict(title='xyz',titlefont=dict(size=10),tickangle=60,tickfont=dict(size=9),tickformat="%d-%b"),
                yaxis=dict(title='XYZ',titlefont=dict(size=10),tickformat=".0f",tickfont=dict(size=9)),
                margin = dict(t=30, l=0, r=0, b=0),
                legend=dict(orientation='h',yanchor="bottom",y=-0.5,xanchor="left",x=0)
                )
            fig=go.Figure()
            fig.add_traces(go.Bar(x=hist.index, y = hist['Actual'])) #alternate x & y to convert to horizontal bar
            fig.add_trace(go.Scatter(x=hist['Target'],y=hist.index))
            fig.layout=l1
            
            import plotly.express as px
            fig = px.bar(hist, x=hist.index, y='Actual')
            fig.add_traces(go.Scatter(y=hist['Target'],x=hist.index))
            fig.layout=l1

            hist = hist[hist['Actual']!='']
            if len(hist)>0:
                hist['Actual'] = hist['Actual'].astype(float)
                consistency = len(hist[hist['Actual']>=hist['Target']])/len(hist)
                consistency = str(consistency * 100) + '%'
                average = np.average(hist['Actual'])
                achievement = str(round(average*100/target,0))+ ' %'
                average = str(int(average))+' '+unit
                kpi[habit] = {'Consistency':consistency,'Average':average,'Achievement':achievement}
                c1,c2 = st.columns([3,7])
                for k,v in kpi[habit].items():
                    c1.metric(k,v)
                c2.plotly_chart(fig)
            else:
                st.write('Habit not tracked yet. Please record your performance regularly!')
        
        kpisummarypl.subheader("Summary of all habits:")
        kpisummarypl1.write(pd.DataFrame(kpi).T)
    
    
# https://plotly.com/python/bullet-charts/
# https://plotly.com/python/v3/bullet-charts/
# Test region
# habitdailydf.to_csv('habitdailydf.csv')
# habitdailydf = pd.read_csv('habitdailydf.csv')
# habitdailydf.set_index('Date',inplace=True)
# habitdailydf.to_pickle('habitdailydf.pkl')
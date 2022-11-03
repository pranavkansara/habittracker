import pandas as pd,numpy as np, seaborn as sns, streamlit as st,os,re, random, datetime
from streamlit import session_state as ss
from PIL import Image
st.set_page_config(layout='wide',page_title='Habit & Goal Tracker')#,page_icon='icon.png')

#%% Sidebar
page = st.sidebar.radio("Select page",['Setup','Daily entry','Dashboard'],index=1)

if os.path.exists('goaldf.pkl'):
    goaldf  = pd.read_pickle('goaldf.pkl')
    goaldf['Category'] = 'Physical'
    goaldf = goaldf[['Date','Goal','Category','Target Unit','Target','Timeline']]
    goaldf.to_pickle('goaldf.pkl')
else:
    goaldf = pd.DataFrame({'Date':np.datetime64, 'Goal':'str','Category':'str','Target Unit':np.number,'Target':'str','Timeline':np.datetime64},index=[])
# only specify non-text types below
goaldisptypes = {'Date':'date', 'Category':['Physical','Mental','Emotional','Spiritual','Financial','Family'],'Target':'number','Timeline':'date'}

if os.path.exists('habitdf.pkl'):
    habitdf  = pd.read_pickle('habitdf.pkl')
else:
    habitdf = pd.DataFrame({'Habit':'str','Related Goal':'str','Target Unit':'str','Target':np.number,'Frequency':'str','Weightage':np.number},index=[])
# only specify non-text types below
habitdisptypes = {'Related Goal':['None']+goaldf['Goal'].unique().tolist(),'Target':'number','Frequency':['Daily','Weekly','Monthly'],'Weightage':'number'}
    
if os.path.exists('habitdailydf.pkl'):
    habitdailydf  = pd.read_pickle('habitdailydf.pkl')
else:
    if os.path.exists('habitdf.pkl'):
        cols = habitdf['Habit'].values.tolist()
        cols.extend(['Books','Articles','Food','Spiritual','Hobby','Family','Projects','Miscellenous','Summary'])
        cols.insert(0,'Date')
        habitdailydf = pd.DataFrame(columns=cols)

#%% Setup page


#%%% Enter habits to track
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
    
def DailyEntry(habitdf,habitdailydf):
    st.subheader("Daily entries")
    dt = st.sidebar.date_input("Enter date")
        
    with st.form('Enter todays values',clear_on_submit=True):
        c = st.columns(4)
        currentries = habitdailydf[habitdailydf['Date']==dt]
        st.write('**Achievement for the day**')
        c = st.columns(4)
        j=0
        finalvals = [dt]
        for i,v in habitdf.iterrows():
            txt = v['Habit']+': ('+ str(v['Target'])+' '+v['Target Unit']+' '+v['Frequency']+')'
            if len(currentries)>0:
                val = currentries[v['Habit']].iloc[0]
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
        finalvals.extend([c[0].text_input('Books read:')])
        finalvals.extend([c[1].text_input('Articles read:')])
        finalvals.extend([c[2].text_input('Food:')])
        finalvals.extend([c[3].text_input('Spiritual activites:')])
        finalvals.extend([c[0].text_input('Hobby related:')])
        finalvals.extend([c[1].text_input('Family time:')])
        finalvals.extend([c[2].text_input('Key Projects')])
        finalvals.extend([c[3].text_input('Miscellenous')])
        st.write('---')
        finalvals.extend([st.text_input('Summary of the day')])
        st.write('---')
        submit = st.form_submit_button()
        if submit:
            st.write('Success!!')
            habitdailydf.loc[len(habitdailydf)] = finalvals
            habitdailydf.to_pickle('habitdailydf.pkl')
            habitdailydf.to_csv('habitdailydf.csv')

def GoalDashboard():
    a=1

def ActivityDashboard(habitdailydf):
    a=1
   
#%% Main section
if page == 'Setup':   
    subpage = st.sidebar.selectbox('Select subpage',['Goals','Habits'])
    if subpage=='Goals':
        goaldf = DisplayNCreateTable(goaldf,goaldisptypes,'goaldf.pkl',mandatorycolname='Goal')
        
    elif subpage == 'Habits':
        habitdf = DisplayNCreateTable(habitdf,habitdisptypes,'habitdf.pkl',mandatorycolname='Habit')
        st.write(habitdf)
            
        if sum(habitdf['Weightage'])>100:
            st.write('Sum of weightage exceeds 100%, hence weights will be normalized to sum up to 100% in same ratio.')
            habitdf['Weightage'] = habitdf['Weightage']*100/sum(habitdf['Weightage'])
            habitdf.to_pickle('habitdf.pkl')
elif page == 'Daily entry':
    DailyEntry(habitdf,habitdailydf)
    

elif page == 'Dashboard':
    subpage = st.sidebar.selectbox('Select subpage',['Goal tracking','Activity tracking'])
    if subpage == 'Goal tracking':
        a=1
    elif subpage == 'Activity tracking':
        ActivityDashboard(habitdailydf)
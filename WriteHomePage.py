import pandas as pd,numpy as np, streamlit as st,os,re, random, datetime
from streamlit import session_state as ss

def WriteHomePage(goaldf,habitdf,habitdailydf):
    st.subheader(f"Welcome {ss.name}!!")
    st.write("""
    We are so proud that you recognize the importance of being a 'BETTER YOU!'

    In order to live a fulfilling life, it is important to have goals addressing 5 important aspects of your life:
    1. Body
    2. Mind
    3. Spirit
    4. Family
    5. Finances

    And hence it is recommended that you have goals, inculcate habits to achieve those goals, and have a mechanism to track the progress towards those goals.

    As James Clear has brilliantly articulated in his book 'Atomic Habits', you need to create those small habits which put together will have a profound impact on your life.

    This app is an attempt to give you a medium to be able to track your goals and habits and help you towards becoming a 'BETTER YOU!'
    """)

    if len(goaldf)>0:
        st.write('-----')
        st.write(f"""
        You have {len(goaldf)} goals set up currently. Please visit Setup page to create new goals or edit existing goals.\n
        You have {len(habitdf)} habits set up currently. Please visit Setup page to create new habits to track or edit existing habits.\n
        You last entered your activities on {max(habitdailydf.index)}.
        """)

        st.write('-----')
        st.write("Here are the goals you are tracking. Please visit Setup page to edit.")
        st.dataframe(goaldf,use_container_width=True)

        st.write('-----')
        st.write("Here are the habits you are tracking. Please visit Setup page to edit.")
        st.dataframe(habitdf,use_container_width=True)

    else:
        st.write('-----')
        st.write("You have not set up any goals or activities currently. Please visit Setup page to create new goals and activities to track")
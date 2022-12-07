import pandas as pd, numpy as np, streamlit as st,os,re, random
from streamlit import session_state as ss
import streamlit_authenticator as stauth

"""
Initial authentication file setup
names = ['Pranav Kansara','Jiya Kansara','Misri Kansara','Shlok Kansara','Hetvi Kansara','Prakhar Kansara','Prerak Kansara']
usernames = ['pranavk','jiyak','misrik','shlokk','hetvik','prakhark','prerakk']
passwords = ['pranavk','jiyak','misrik','shlokk','hetvik','prakhark','prerakk']
hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)
"""
def ufn_Authenticate():
    #%% Authentication
    with open('./credentials.yaml') as file:
        config = stauth.yaml.load(file, Loader=stauth.SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    c1,c2 = st.columns(2)
    with c1:
        name, authentication_status, username = authenticator.login('Existing User', 'main')

    if not authentication_status:
        with c2:
            try:
                if authenticator.register_user('New User', preauthorization=False):
                    st.success('User registered successfully. Please login using your credentials.')
                    with open('credentials.yaml', 'w') as file:
                        stauth.yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)    
            
    return authenticator,config

def authenticateactions(authenticator,config):
    mgtaction = st.sidebar.radio('Select action',['Reset password','Forgot password','Forgot username','Update details'])
    if mgtaction == 'Reset password':
        try:
            if authenticator.reset_password(ss.username, 'Reset password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

    if mgtaction == 'Forgot password':
        try:
            username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
            if username_forgot_pw:
                st.success('New password sent securely')
                # Random password to be transferred to user securely
            elif username_forgot_pw == False:
                st.error('Username not found')
        except Exception as e:
            st.error(e)
        
    if mgtaction == 'Forgot username':
        try:
            username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
            if username_forgot_username:
                st.success('Username sent securely')
                # Username to be transferred to user securely
            elif username_forgot_username == False:
                st.error('Email not found')
        except Exception as e:
            st.error(e)
            
    if mgtaction == 'Update details':
        try:
            if authenticator.update_user_details(ss.username, 'Update user details'):
                st.success('Entries updated successfully')
        except Exception as e:
            st.error(e)
            
    with open('./credentials.yaml', 'w') as file:
        stauth.yaml.dump(config, file, default_flow_style=False)
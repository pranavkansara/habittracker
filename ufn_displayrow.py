# -*- coding: utf-8 -*-
import pandas as pd,numpy as np, streamlit as st,os,re, random, datetime
def DispRowStreamlit(rowdict):
    """
    disptypes takes values of : 
    input is a dictionary with 
        key = column header and 
        value = dictionary of 3 values:
            {columntype= number, date, text, textarea, dropdown, radio
             defaultvalue=''
             listofvalues=[] 
            }
    """
    for colheader,val in rowdict.items():
        columntype = val.get('columntype','text')
        defaultvalue = val.get('defaultvalue','')
        listofvalues = val.get('listofvalues',[])

        if typ=='number':
            st.number_input(header,value=val,key=header)
        elif typ=='date':
            st.date_input(header,value=val,key=header)
        elif typ=='text':
            st.text_input(header,value=val,key=header)
        elif typ=='textarea':
            st.text_area(header,value=val,key=header)
        elif typ=='dropdown':
            st.selectbox()
        elif typ=='radio':
            st.radio()



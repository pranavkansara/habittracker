class style:
    def __init__(self):
        self.STYLE = """
        <style>
        /*To change sidebar margins both in case of expanded view and contracted view*/
        /*[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 250px;
            font-size:11px;
        }
        
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 250px;
            margin-left: -250px;
            font-size:11px;
        }*/
        
        /* to change margins of main body*/
        .css-18e3th9 {
            padding-top: 0rem;
            padding-bottom: 10rem;
            padding-left: 2.5rem;
            padding-right: 5rem;
        }
        /* Sidebar top margin*/
        .css-1vq4p4l {
            padding-top: 3.5rem;
        }
        /* to change sidebar top padding, color. To get css code, right click on the side bar area and click on inspect*/
        .css-zbg2rx{
            padding-top: 1rem;
            /*background-image: linear-gradient(#8993ab,#8993ab);*/
        }
        
        /* to change side bar text size */
        /* div.st-bf{flex-direction:column;} div.st-ag{font-size:11px;} 
        
        /* to hide made by streamlit label */
        .reportview-container .css-1vbd788 {{ 
                            padding-top: 3px;
                        }}
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        </style>
        """
    

    def writehtml(self,url,bg='transparent',c='transparent',fs=20,style='h1',align='center'):
        import streamlit as st
        if c=='transparent':
            st.markdown(f'<{style} style="background-color:{bg};font-size:{fs}px;padding:1px"><{align}>{url}</{align}></style>', unsafe_allow_html=True)
        else:
            st.markdown(f'<{style} style="background-color:{bg};color:{c};font-size:{fs}px;padding:1px"><{align}>{url}</{align}></style>', unsafe_allow_html=True)


    def StyleTable(self,df,bgsubset=[],percformsubset=[],numformsubset=[],floatsubset=[],hideidx=False):
        cell_hover = {  # for row hover use <tr> instead of <td>
                                'selector': 'td:hover',
                                'props': 'background-color: #ffffb3;color: black;font-size: 11pt;'
                            }
        index_names = {
            'selector': '.index_name',
            'props': 'font-style: italic; color: darkgrey; font-weight: normal; font-size: 11pt;text-align: left;'
        }
        headers = {
            'selector': 'th:not(.index_name)',
            'props': 'background-color: #000066; color: white;font-size: 11pt;text-align: left;'
        }
        tdprops = {
            'selector':'td',
            'props': 'text-align: right; font-size: 11pt;'
                   }
        dfstyle = (df.style
                .set_properties(**{'background-color':'','border-color': 'black','border-width':10})
                # .set_properties(**{'width': '70px'},subset=self.ReturnFld4Disp)
                .set_table_styles([index_names, headers, cell_hover])
                .background_gradient(cmap='BuGn',axis=0,subset=bgsubset)
                .format('{:.1%}', na_rep="-",subset=percformsubset)
                .format('{:,.0f}', na_rep="-",subset=numformsubset)
                .format('{:,.2f}',na_rep='-',subset=floatsubset)
                # .set_caption('abcdefg')
                )
        
        if hideidx:
            dfstyle = dfstyle.hide_index()
            
        return dfstyle

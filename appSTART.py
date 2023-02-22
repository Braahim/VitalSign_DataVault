import streamlit as st 
import os

from pages import About,config,vitalSigns_generator,patient_generator


st.set_page_config(page_title= "Data Vault Demo", page_icon= ':vault')


class multipage:  
    def __init__(self):
        self.pages = []
    def add_page(self,title,func): 
        self.pages.append({
            'title': title,
            'function': func
        })  
    def run(self):
        page = st.sidebar.radio(
            'Menu',
            self.pages,
            format_func = lambda page : page['title'])
        st.session_state.app_pagename = page['title']
        page['function']()

page = multipage() 

################################################################################
###################### SETUP : BEGINNING #######################################
################################################################################
# sidebar titles management
st.sidebar.title('Snowflake Data vault config')
# add all your application here
page.add_page('Patients generator', patient_generator.page)
page.add_page('Vital Signs generator', vitalSigns_generator.page)
page.add_page('Config - Setup', config.page)
page.add_page('About', About.page)
 
# general path management
st.session_state.path_root = os.getcwd()
st.session_state.path_this = os.path.dirname(os.path.realpath(__file__))
st.session_state.path_data = '/'.join(st.session_state.path_this.split('/')[:-1])
# the main app  
page.run()

################################################################################
###################### SETUP : ENDING ##########################################
################################################################################ 



import streamlit as st
import pandas as pd
import numpy as np
import faker
import time
import utils.generation_utils as gen_utils
import utils.app_utils as app_utils
import logging


def page():    
    # Define the Streamlit app
    
    st.title("Patient Data Generator 🚑")
    st.write("Welcome to the Patient Data Generator! Use the sliders below to choose the number of patients and the number of seconds to generate data for.")

    if 'conn' not in st.session_state:
        st.warning("Please switch to config file to connect to Snowflake")
    else:
        
        # Create a Faker object to generate fake patient data
        fake = faker.Faker()
        # Create sliders to allow user to choose the number of patients and the number of seconds
        num_patients = st.slider("Number of patients", min_value=1, max_value=100, value=10, step=1)
        num_seconds = st.slider("Number of seconds", min_value=1, max_value=60, value=10, step=1)

        # Generate patient data and display in a table
        st.write(f"Generating data for {num_patients} patients every {num_seconds} seconds... 🏥")
        if st.button("generate"):
            for i in range(num_seconds):
                st.write("⏳ Please wait...")
                time.sleep(1)

        st.write("🎉 Data generation complete! You can now export the data to a file.")
        try:
            # Create a button to export the data to a CSV file
            if st.button("Export to Snowflake"):
                data = gen_utils.generate_patient_data(num_patients)
                hub_data = pd.DataFrame(data['patient_key'])
                #data = pd.DataFrame(data.drop(['patient_key'],axis = 1))
                #logging.info(hub_data)
        
                app_utils.write_csv_toSnowflake(st.session_state.conn,hub_data,'s_patient_hub')
                id_list = pd.DataFrame(app_utils.query_snowflake(st.session_state.conn,'select * from s_patient_hub')).rename(columns={'PATIENT_KEY' : 'patient_key'})

              
                #st.write(id_list.dtypes)
                data = pd.merge(pd.DataFrame(id_list),data, on="patient_key")
                logging.info(data)
                app_utils.write_csv_toSnowflake(st.session_state.conn,data.drop(['patient_key'],axis = 1),'s_patient_sat')

                st.success("### Data Generated and added succesfully ! ")
                st.balloons()

                st.write("Patient data generated recently : ")
                st.dataframe(data)

        except Exception as e:
            st.error(f"Error: {str(e)}")

     

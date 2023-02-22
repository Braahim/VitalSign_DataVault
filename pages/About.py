import streamlit as st

def page():
    # Set page title

    # Add header
    st.header(":chart_with_upwards_trend: Patient Data Generation & Data Vault")

    # Add some fun emojis and wording
    st.write("Welcome to our super cool and totally awesome patient data generation app and data vault! :sunglasses: ")
    st.write("Our mission is to help you easily generate patient data so you can test your apps and models with realistic data, all while keeping it safe and sound in our super secure data vault! :shield:")

    # Add description of patient data generation
    st.subheader(":computer: Patient Data Generation")
    st.write("With our patient data generation feature, you can easily generate patient data for testing purposes. Simply choose the number of patients, how many seconds you want the data to be generated for, and how many files you want to create. :file_folder: We take care of the rest!")

    # Add description of data vault
    st.subheader(":lock: Data Vault")
    st.write("Our data vault is the perfect place to store all of your patient data, keeping it secure and organized. :key: We use the latest in security technology to ensure that your data is safe and sound. Plus, our user-friendly interface makes it easy to access and manage your data with ease. :smile:")

    # Add call-to-action for getting started
    st.write("Ready to get started? Let's generate some patient data and store it in our data vault! :rocket:")

import streamlit as st
import random
import datetime
import faker
import logging
import pandas as pd
import numpy as np
fake = faker.Faker()

def generate_vital_signs():
    temperature = round(random.uniform(35.0, 40), .5)
    heart_rate = random.randint(40, 180)
    respiratory_rate = random.randint(8, 40)
    systolic_bp = random.randint(90, 200)
    diastolic_bp = random.randint(60, 120)
    oxygen_saturation = random.randint(80, 100)
    record_time = datetime.now()
    return temperature, heart_rate, respiratory_rate, systolic_bp, diastolic_bp, oxygen_saturation,record_time
 

#### Patient : 

## Generate Patient natural key ( a combination between gender, name and birth date)
def create_natural_key(name, date_of_birth, gender):
    # Extract the first two letters of the name
    name_initials = name[:2].lower()
    
    # Extract the month and year of birth
    birth_month = date_of_birth.strftime('%m')
    birth_year = date_of_birth.strftime('%y')
    
    # Determine the gender code based on the provided gender
    gender_code = 'f' if gender.lower() == 'f' else 'm'
    
    # Combine the components to create the natural key
    natural_key = f'{gender_code}{name_initials}{birth_month}{birth_year}'
    
    return natural_key

# Define function to generate patient data
def generate_patient_data(num_patients):
    
    data = []
    for i in range(num_patients):
        gender = random.choice('MF')
        name = fake.first_name_male() if gender =="M" else fake.first_name_female()
        address = fake.address()
        email = fake.email()
        phone_number = fake.phone_number()
        birth_date = datetime.datetime.strptime( fake.date(), '%Y-%m-%d')
        natural_key = create_natural_key(name,birth_date,gender)
        recorded_at = datetime.datetime.now()
        logging.info(data)
        data.append({'patient_key': natural_key,'patient_name': name, 'adress': address, 
                     'email': email, 'birth_date': str(birth_date), 'phone': phone_number, 'recorded_at': recorded_at, 'gender' : gender})
    return pd.DataFrame(data)


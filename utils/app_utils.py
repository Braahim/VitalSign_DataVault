import streamlit as st
import snowflake.connector
import json
import pandas as pd
import numpy as np
import logging
def connect_to_snowflake(user,password,account,role,warehouse,database,schema):
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            role = role,
            warehouse=warehouse,
            database=database,
            schema=schema,
        )

        # Get a cursor
        cursor = conn.cursor()

        st.success('Connected to Snowflake')

        return cursor

    except snowflake.connector.errors.DatabaseError as e:
        st.error(f'Error connecting to Snowflake: {e.msg}')

    except Exception as e:
        st.error(f'Error connecting to Snowflake: {e}')

def show_snowflake_info(cursor):
    # Create a cursor object to execute SQL queries
    

    # Get the list of databases


    # Get the list of schemas
    cursor.execute("SHOW SCHEMAS")
    schemas = [schema[1] for schema in cursor.fetchall()]

    # Get the list of UDFs
    cursor.execute("SHOW USER FUNCTIONS")
    udfs = [udf[1] for udf in cursor.fetchall()]

    # Create a table to display the information
    data = {"Schemas": schemas, "UDFs": udfs}
    
    return data

def write_csv_toSnowflake(cur, df, table_name):
    """ 
    Write the DataFrame to Snowflake
    
    """

    #cur = conn.cursor()
    try:
 
        
        df = df.astype(str)
        q = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES "

        logging.info(f"{', '.join(c for c in df.columns)}")
        cur.executemany(f"INSERT INTO {table_name} ({','.join(c for c in df.columns)}) VALUES ({','.join(['%s']*len(df.columns))})",
                        df.values.tolist())
        
        
    except Exception as e:
        print(f"Error inserting data: {e}")
      # cur.close()
        #conn.close()
        return
    
    # Commit the changes and close the connection
    try:
        cur.execute('commit;')
    except Exception as e:
        print(f"Error committing changes: {e}")
    finally:
        st.warning(f"Yess 🎉 !Data added succesfully to {table_name} on SNOWFLAKE")
        

        #st.markdown("### Data Generated : ")
     #   cur.close()
      #  conn.close()

def query_snowflake(cursor, query):
    try:
       

        # Execute query and retrieve results as pandas DataFrame
        cursor.execute(query)
        df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        # Close the cursor
        #cursor.close()

        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

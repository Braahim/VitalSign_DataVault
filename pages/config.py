import streamlit as st
import snowflake.connector
import utils.app_utils as app_utils

def page():
    if 'conn' not in st.session_state:
        st.session_state.conn = app_utils.connect_to_snowflake(st.secrets['snowflake']['username'],st.secrets['snowflake']['password'],st.secrets['snowflake']['account'],st.secrets['snowflake']['role'],
                                          st.secrets['snowflake']['warehouse'], st.secrets['snowflake']['database'],st.secrets['snowflake']['schema'])
    else : 
        st.success("Connected to snowflake")
        st.table(app_utils.show_snowflake_info(st.session_state.conn))
































































    """
    # Set up Snowflake connection
    account = st.text_input("Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    conn = snowflake.connector.connect(
        account=account,
        user=username,
        password=password
    )
    cursor = conn.cursor()

    # Fetch list of roles and warehouses
    cursor.execute("SHOW ROLES")
    roles = [role[1] for role in cursor.fetchall()]
    cursor.execute("SHOW WAREHOUSES")
    warehouses = [wh[0] for wh in cursor.fetchall()]

    # Select role and warehouse
    selected_role = st.selectbox("Select Role", roles)
    selected_warehouse = st.selectbox("Select Warehouse", warehouses, index=warehouses.index("XSMALL_WH"))

    # Fetch list of accessible databases for selected role
    cursor.execute(f"USE ROLE {selected_role}")
    cursor.execute("SHOW DATABASES")
    accessible_dbs = [db[1] for db in cursor.fetchall()]

    # Select database and schema
    selected_db = st.selectbox("Select Database", accessible_dbs)
    if selected_db : cursor.execute(f"use warehouse {selected_warehouse}")
    cursor.execute(f"USE DATABASE {selected_db}")
    cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA")
    schemas = [schema[0] for schema in cursor.fetchall()]
    selected_schema = st.selectbox("Select Schema", schemas)

    # Fetch list of tables in selected schema
    cursor.execute(f"USE SCHEMA {selected_schema}")
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables = [table[0] for table in cursor.fetchall()]

    # Select table and display its columns
    selected_table = st.selectbox("Select Table", tables)
    cursor.execute(f"SELECT * FROM {selected_table} LIMIT 1")
    columns = [col[0] for col in cursor.description]
    st.write("Columns:", columns)

    # Add a new row to the selected table
    if st.button("Add Row"):
        new_row = []
        for col in columns:
            new_val = st.text_input(f"{col}")
            new_row.append(new_val)
        new_row_str = ", ".join(f"'{val}'" for val in new_row)
        cursor.execute(f"INSERT INTO {selected_table} VALUES ({new_row_str})")
        conn.commit()
        st.success("Row added!")

    # Delete a row from the selected table
    if st.button("Delete Row"):
        delete_id = st.text_input("Enter ID of Row to Delete")
        cursor.execute(f"DELETE FROM {selected_table} WHERE id='{delete_id}'")
        conn.commit()
        st.success("Row deleted!")

    # Display fun elements
    st.write(":smile: Welcome to the Snowflake Management App!")
    st.write("This app allows you to manage your Snowflake account and databases with ease.")
    st.write("We also offer the best jokes and memes to brighten up your day!")"""
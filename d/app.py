import streamlit as st
import snowflake.connector

# Set default values
default_account = "gfiinformatiquepartner.west-europe.azure"
default_username = "bsmaoui"
default_password = "your_password"
default_warehouse = "XSMALL_WH"
default_role = "accountadmin"
# Create a form for the user to enter their credentials
with st.form("login_form"):
    account = st.text_input("Account", default_account)
    username = st.text_input("Username", default_username)
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button(label="Log In")
# Connect to Snowflake with default values
conn = snowflake.connector.connect(
    user=username,
    password=password,
    account=account,
    warehouse=default_warehouse,
    role=default_role,
    database = "BSMAOUI_DB"
)

# Get list of warehouses, roles, and databases

st.session_state.warehouse_list = [x[0] for x in conn.cursor().execute("SHOW WAREHOUSES").fetchall()]
st.session_state.role_list = [x[0] for x in conn.cursor().execute("select role_name from information_schema.enabled_roles;").fetchall()]
st.session_state.db_list = [x[0] for x in conn.cursor().execute("SELECT DATABASE_NAME FROM INFORMATION_SCHEMA.DATABASES").fetchall()]



# Create a sidebar for the user to select options
st.sidebar.title("Snowflake Management")
new_role = st.sidebar.selectbox("Select Role", st.session_state.role_list)
new_warehouse = st.sidebar.selectbox("Select Warehouse", st.session_state.warehouse_list)
new_db = st.sidebar.selectbox("Select Database", st.session_state.db_list)

# Get list of schemas in selected database
st.session_state.schema_list = [x[0] for x in conn.cursor().execute(f"select schema_name from  {new_db}.information_schema.schemata where schema_name not like 'INFORMATION_SCHEMA'").fetchall()]
new_schema = st.sidebar.selectbox("Select Schema", st.session_state.schema_list)

if new_warehouse : 
    conn.cursor().execute(f"use warehouse {new_warehouse}")
if new_role : 
    conn.cursor().execute(f"use role {new_role};")
    st.session_state.warehouse_list = [x[0] for x in conn.cursor().execute("SHOW WAREHOUSES").fetchall()]
    st.session_state.db_list = [x[0] for x in conn.cursor().execute("SELECT DATABASE_NAME FROM INFORMATION_SCHEMA.DATABASES;").fetchall()]
    st.session_state.schema_list = [x[0] for x in conn.cursor().execute(f"select schema_name from  {new_db}.information_schema.schemata where schema_name not like 'INFORMATION_SCHEMA';").fetchall()]
if new_db :
    conn.cursor().execute(f"use database {new_db}")
    st.session_state.schema_list = [x[0] for x in conn.cursor().execute(f"select schema_name from  {new_db}.information_schema.schemata where schema_name not like 'INFORMATION_SCHEMA';").fetchall()]

   







# Show a table of the selected database's tables
table_list = [x[0] for x in conn.cursor().execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema like '{new_schema}'").fetchall()]
selected_table = st.selectbox("Select Table", table_list)
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {new_db}.{new_schema}.{selected_table}")
columns = [col[0] for col in cursor.description]
rows = cursor.fetchall()
st.write(f"## {selected_table}")
st.write(f"### Rows: {len(rows)}")
if len(rows) > 0:
    st.write(f"### Columns: {len(columns)}")
    st.write(f"#### {', '.join(columns)}")
    for row in rows:
        st.write(row)

# Add a new row to the selected table
if st.button("Add Row"):
    new_row = []
    for col in columns:
        new_val = st.text_input(f"{col}")
        new_row.append(new_val)
    new_row_str = ", ".join(f"'{val}'" for val in new_row)
    cursor.execute(f"INSERT INTO {new_db}.{new_schema}.{selected_table} VALUES ({new_row_str})")
    conn.commit()
    st.success("Row added!")

# Delete a row from the selected table
if st.button("Delete Row"):
    delete_id = st.text_input("Enter ID of Row to Delete")
    cursor.execute(f"DELETE FROM {new_db}.{new_schema}.{selected_table} WHERE id='{delete_id}'")
    conn.commit()
    st.success("Row deleted!")

# Display fun elements
st.write(":smile: Welcome to the Snowflake Management App!")
st.write("This app allows you to manage your Snowflake account and databases with ease.")
st.write("We also offer the best jokes and memes to brighten up your day!")

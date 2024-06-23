import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from langchain.chat_models import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase

# Function to save DataFrame to SQLite
def save_to_sqlite(df, sqlite_db_path, table_name):
    os.makedirs(os.path.dirname(sqlite_db_path), exist_ok=True)
    engine = create_engine(f"sqlite:///{sqlite_db_path}")
    df.to_sql(table_name, engine, index=False, if_exists='replace')
    st.success(f"Data has been saved to the {table_name} table in {sqlite_db_path} database.")

# Function to set up OpenAI agent
def setup_openai_agent(sqlite_db_path, api_key, model_name):
    db = SQLDatabase.from_uri(f"sqlite:///{sqlite_db_path}")
    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name=model_name,
        temperature=0.0
    )
    agent_executor = create_sql_agent(llm, db=db, verbose=True)
    return agent_executor

# Streamlit app
def main():
    st.title("SimpliQuery ⚡️ ")
    st.sidebar.title("Settings")

    # API Key input and save button in sidebar
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    if st.sidebar.button("Save API Key"):
        st.session_state.api_key = api_key
        st.sidebar.success("API Key saved successfully!")

    # Retrieve saved API key from session state
    api_key = st.session_state.get("api_key", "")

    # Default values
    OpenAIModel = "gpt-3.5-turbo-16k"
    sqlite_db_path = "temp_data/database.db"

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Initialize variables
    table_name = st.text_input("Enter table name", "table_name")
    agent_executor = None

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        st.write("Data Preview:")
        st.write(df.head())

        if st.button("Save to SQLite"):
            if sqlite_db_path and table_name:
                save_to_sqlite(df, sqlite_db_path, table_name)
                st.success(f"Data has been saved to SQLite: {sqlite_db_path}/{table_name}")
                
            else:
                st.error("Please provide both SQLite database path and table name.")

    # Interaction with OpenAI agent
    if api_key and sqlite_db_path:
        st.subheader("Interact with Data")
        query_input = st.text_input("Enter your query", "Tell me more about the data in the table")

        if st.button("Run Query"):
            try:
                agent_executor = setup_openai_agent(sqlite_db_path, api_key, OpenAIModel)
                response = agent_executor.invoke({"input": query_input})
                st.write("Response from OpenAI:")
                st.write(response['output'])
            except Exception as e:
                st.error(f"Error running query: {e}")

if __name__ == "__main__":
    main()

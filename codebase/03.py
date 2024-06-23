import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain_community.utilities import SQLDatabase

# Load environment variables
api_key = ""
OpenAIModel = "gpt-3.5-turbo-16k"
db_path = "chinook.db"

def main():
    # Set up the OpenAI API key
    os.environ["OPENAI_API_KEY"] = api_key

    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name=OpenAIModel,
        temperature=0.0
    )

    # Assume `db` is a properly initialized database connection or client
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")


    # Create the SQL agent
    agent_executor = create_sql_agent(llm, db=db, verbose=True)

    # Prepare the input for the agent
    input_data = {
        "input": "Can you tell me average of treacks for each artist"
    }

    # Invoke the agent with the input data
    response = agent_executor.invoke(input_data)

    # Print the response
    print(response)

if __name__ == "__main__":
    main()

import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Load environment variables
api_key = ""
OpenAIModel = "gpt-3.5-turbo-16k"
db_path = "chinook.db"

def main():
    # Set up OpenAI API key
    openai.api_key = api_key

    # Define the messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
    ]

    # Send the chat message to OpenAI
    response = openai.ChatCompletion.create(
        model=OpenAIModel,
        messages=messages
    )

    # Print the response
    print(response['choices'][0]['message']['content'])
    
    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name=OpenAIModel,
        temperature=0.0
    )
    print(llm)
    
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    # ex 1
    # chain = create_sql_query_chain(llm, db)
    # response = chain.invoke({"question": "How many albums are there"})
    # print(response)
    # print(chain.get_prompts()[0].pretty_print())
    
    #  ex 2
    # write_query = create_sql_query_chain(llm, db)
    # execute_query = QuerySQLDataBaseTool(db=db)
    # chain = write_query | execute_query
    # response = chain.invoke({"question": "How many employees are there"})
    # print(response)
    
    # ex 3
    # write_query = create_sql_query_chain(llm, db)
    # execute_query = QuerySQLDataBaseTool(db=db)
    # chain = write_query | execute_query
    # answer_prompt = PromptTemplate.from_template(
    # """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

    #     Question: {question}
    #     SQL Query: {query}
    #     SQL Result: {result}
    #     Answer: """
    #     )

    # answer = answer_prompt | llm | StrOutputParser()
    # chain = (
    #     RunnablePassthrough.assign(query=write_query).assign(
    #         result=itemgetter("query") | execute_query
    #     )
    #     | answer
    # )

    # response = chain.invoke({"question": "How many albums are there"})
    # print(response)
    

    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    response = agent_executor.invoke(
        {
            "input": "List the total sales per country. Which country's customers spent the most?"
        }
    )
    print(response)
        


if __name__ == "__main__":
    main()

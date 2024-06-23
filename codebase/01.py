from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, inspect

db_path = "chinook.db"

def read_data():
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    print(db.dialect)
    print(db.get_usable_table_names())
    print(db.run("SELECT * FROM albums LIMIT 10;"))
    
read_data()


def inspect_db():

    # Create an engine that connects to the test.db SQLite database
    engine = create_engine(f"sqlite:///{db_path}")

    # Connect to the database
    connection = engine.connect()

    # Create an inspector object
    inspector = inspect(engine)

    # Retrieve the names of all the tables in the database
    table_names = inspector.get_table_names()
    print("Tables:", table_names)

    # Loop over each table to get detailed information like schema, columns, etc.
    for table_name in table_names:
        print(f"Information for table: {table_name}")
        
        # Get the schema of the table (for SQLite, schema is often None)
        print(f"Schema: {inspector.get_schema_names()}")
        
        # Get the columns and their attributes for each table
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(f"Column: {column['name']} Type: {column['type']}")
        
        # Additionally, you can use get_pk_constraint and get_foreign_keys 
        # methods to retrieve information about primary and foreign keys respectively
        pk_constraint = inspector.get_pk_constraint(table_name)
        print(f"Primary Key Constraint: {pk_constraint}")

        foreign_keys = inspector.get_foreign_keys(table_name)
        print(f"Foreign Keys: {foreign_keys}")
        
        

    # Do not forget to close the connection when done
    connection.close()
    
    
inspect_db()
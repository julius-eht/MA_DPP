import psycopg2
from psycopg2 import sql

def connect_to_db():
    # Define your connection details
    conn = psycopg2.connect(
        dbname="lca_database",
        user="postgres",
        password="123456789",
        host="localhost",  # or your database server address
        port="5432"        # default port for PostgreSQL
    )
    return conn

def create_table(conn):
    # Create a cursor object using the connection
    cursor = conn.cursor()
    
    # Define the SQL query to create a new table in the public schema
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS products (
        id VARCHAR(255) PRIMARY KEY,
        product_name VARCHAR(255),
        description TEXT,
        id_short VARCHAR(100),
        impact_category VARCHAR(255),
        impact_amount NUMERIC,
        impact_unit VARCHAR(50)
    );
    '''
    
    # Execute the SQL query
    cursor.execute(create_table_query)
    
    # Commit the transaction
    conn.commit()

def insert_data(conn, id, product_name, description, id_short, impact_category, impact_amount, impact_unit):
    cursor = conn.cursor()
    
    # Define the SQL query to insert data into the public schema
    insert_query = sql.SQL('''
    INSERT INTO public.products (id, product_name, description, id_short, impact_category, impact_amount, impact_unit)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;  -- Avoid inserting duplicate IDs
    ''')
    
    # Execute the query with the provided data
    cursor.execute(insert_query, (id, product_name, description, id_short, impact_category, impact_amount, impact_unit))
    
    # Commit the transaction
    conn.commit()

def fetch_first_row(conn):
    cursor = conn.cursor()
    
    # Define the SQL query to fetch the first row from the products table
    fetch_query = '''
    SELECT * FROM public.products LIMIT 1;
    '''
    
    # Execute the query
    cursor.execute(fetch_query)
    
    # Fetch the result
    first_row = cursor.fetchone()
    
    # Print the result
    print("First row:", first_row)

    # Optionally return the first row for further processing
    return first_row

if __name__ == "__main__":
    # Connect to the database
    connection = connect_to_db()
    
    # Create the table in the public schema
    create_table(connection)
    
    # Insert sample data into the public schema
    insert_data(connection, 1, "Bosch ACH2 Stellmotor", "Stellmotor", "p_01", "Global warming (GWP100a)", 23.3, "kg CO2 eq")
    
    print("Sample data inserted successfully.")
    
    # Fetch and print the first row from the table
    first_row = fetch_first_row(connection)
    
    # Close the connection
    connection.close()
import psycopg2
from psycopg2 import sql

def connect_to_db():
    # Define your connection details
    conn = psycopg2.connect(
        dbname="lca_database",
        user="lca_user",
        password="123456789",
        host="localhost",  # or your database server address
        port="5432"        # default port for PostgreSQL
    )
    return conn

def create_table(conn):
    # Create a cursor object using the connection
    cursor = conn.cursor()
    
    # Define the SQL query to create a new table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS lca_schema.products (
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
    
    # Define the SQL query to insert data
    insert_query = sql.SQL('''
    INSERT INTO products (id, product_name, description, id_short, impact_category, impact_amount, impact_unit)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;  -- Avoid inserting duplicate IDs
    ''')
    
    # Execute the query with the provided data
    cursor.execute(insert_query, (id, product_name, description, id_short, impact_category, impact_amount, impact_unit))
    
    # Commit the transaction
    conn.commit()

if __name__ == "__main__":
    # Connect to the database
    connection = connect_to_db()
    
    # Create the table
    create_table(connection)
    
    # Insert sample data
    insert_data(connection, "product_001", "Bosch ACH2 Stellmotor", "Stellmotor", "p_01", "Global warming (GWP100a)", 23.3, "kg CO2 eq")
    
    print("Sample data inserted successfully.")
    
    # Close the connection
    connection.close()
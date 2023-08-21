import pyodbc

# Define the connection string
server = 'Mthokozisi-2\SQLEXPRESS'  # Replace with your SQL Server hostname or IP address
database = 'AgriDrone'
username = 'Mthokozisi-2\mthog'  # Replace with your SQL Server username
password = ''  # Replace with your SQL Server password

# Create a connection string
conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

try:
    # Establish the database connection
    conn = pyodbc.connect(conn_str)

    # Create a cursor for database operations
    cursor = conn.cursor()

    # Now you can perform SQL operations using the 'cursor'

    # For example, you can execute a query
    cursor.execute("SELECT * FROM your_table")

    # Fetch the results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Don't forget to close the cursor and connection when done
    cursor.close()
    conn.close()

except Exception as e:
    print("An error occurred:", e)


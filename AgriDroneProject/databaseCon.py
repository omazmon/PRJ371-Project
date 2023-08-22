import pyodbc
import hashlib
import base64

def hash_password(password):
    # Salt the password (e.g., by appending "123" to it)
    salted_password = (password + "123").encode('utf-8')

    # Compute the SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(salted_password)
    hash_bytes = sha256.digest()

    # Convert the hash to a base64-encoded string
    hash_base64 = base64.b64encode(hash_bytes).decode('utf-8')

    return hash_base64
def validate_credentials(username, password):
    flag = False
    try:
        # Establish a connection to your SQL Server database
        conn_str = (
            r'DRIVER={SQL Server Native Client 11.0};'
            r'SERVER=Mthokozisi-2\SQLEXPRESS;'
            r'DATABASE=AgriDrone;'
            r'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(conn_str)

        # Hash the provided password (you should implement HashPassword function)
        hashed_password = hash_password(password)

        # Prepare and execute the SQL query to retrieve user information
        cursor = conn.cursor()
        query = f"SELECT * FROM farmer WHERE Username = '{username}' AND Password = '{hashed_password}';"
        cursor.execute(query)

    except Exception as ex:
        print(str(ex))
    finally:
        # Close the database connection
        if conn:
            conn.close()

    return flag



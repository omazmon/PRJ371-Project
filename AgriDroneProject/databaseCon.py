import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('../AgriDronDatabase.sql')

cursor = connection.cursor()

# Define the data you want to insert
FarmID = 1
FarmName = 'CowCow Farm'
Location = 'Secunda'
FarmSize = '5000m'
OwnerName = 'Jacob'
ContactNumber = '081 123 1432'

# Insert data into the Farm table
farm_data = (FarmID, FarmName, Location, FarmSize, OwnerName, ContactNumber)
cursor.execute("INSERT INTO Farm VALUES (?, ?, ?, ?, ?, ?)", farm_data)

connection.commit()
connection.close()


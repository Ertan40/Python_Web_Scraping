import pandas as pd
import psycopg2

# Read Excel file into a DataFrame
df = pd.read_excel('SampleData.xlsx')
# print(df.head())

# Establish connection to PostgreSQL
connection = psycopg2.connect(
    dbname="sales_db",
    user="postgres-user",
    password="password",
    host="127.0.0.1",
    port="5432"
)

cursor = connection.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        OrderDate DATE,
        Region VARCHAR(20),
        Rep VARCHAR(30),
        Item VARCHAR(30),
        Units INT,
        Unit_Cost DECIMAL(10, 2),
        Total DECIMAL(10, 2)
    )
''')

# Insert data into the table
for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO sales (OrderDate, Region, Rep, Item, Units, Unit_Cost, Total)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (row['OrderDate'], row['Region'], row['Rep'], row['Item'], row['Units'], row['Unit Cost'], row['Total']))

# Commit the transaction
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()

print("Data imported successfully into PostgreSQL database.")




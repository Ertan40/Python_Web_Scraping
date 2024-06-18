import sqlite3
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

cursor.execute('''
         SELECT * FROM quotes 
           ''')

data = cursor.fetchall()
# print(data)
for d in data:
    print(d)
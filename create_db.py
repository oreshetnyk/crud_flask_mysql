import mysql.connector

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='root',
    port=3307,
    #database='doctors' 
)

my_cursor = mydb.cursor()

# query = 'CREATE DATABASE doctors'
query = 'DROP TABLE doctors'
my_cursor.execute(query)

my_cursor.execute('SHOW DATABASES')

for db in my_cursor:
    print(db)
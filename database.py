import pymysql
 
#server connection, port == 3307
# http://127.0.0.1/phpmyadmin
mydb = pymysql.connect(
  host="127.0.0.1",
  port=3307,
  user="root",
  database="lab45db",
  passwd=""
)
 
mycursor = mydb.cursor() #cursor created

#query = "CREATE TABLE Doctors(id INT PRIMARY KEY AUTO_INCREMENT, name CHAR(45), position CHAR(45), cabinet INT, time CHAR(20), service CHAR(45), salary INT, contract_number INT)"
"""
queries = ['INSERT INTO doctors(name, position, salary) VALUES("Іванов О. О.", "Невролог", 12000);',
    'INSERT INTO doctors(name, position, salary) VALUES("Михайлов М. К.", "Отоларинголог", 9500);',
    'INSERT INTO doctors(name, position, salary) VALUES("Капустін К. Ф.", "Стоматолог", 10000);'
]
for query in queries:
    mycursor.execute(query)
"""
query = "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123';"
mycursor.execute(query)
mydb.commit()
mycursor.close()
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password1234"
)

print(mydb)
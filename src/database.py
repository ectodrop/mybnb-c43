import mysql.connector
import notifications

_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password1234",
  database="mybnb"
)

def get_connection():
    return _connection

def get_new_cursor():
    return _connection.cursor(buffered=True)

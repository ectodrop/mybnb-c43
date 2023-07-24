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
    return _connection.cursor()

def execute(cursor, query, params=None):
    try:
        cursor.execute(query, params)
    except Exception as e:
        notifications.set_notification(str(e))
        return False
    return True

from database import connection
# from mysql.connector.cursor import CursorBase

def create_account():
    questions = [
        "Enter your name",
        "Enter your Social Insurance Number (SIN)",
        "Enter your Birthday (yyyy-mm-dd)",
        "Enter your occupation (leave blank for none)",
        "Enter your address",
    ]
    insert_user = ("INSERT INTO User "
               "(name, sin, birthday, occupation, address)"
               "VALUES (%s, %s, %s, %s, %s)")

    answers = []
    for question in questions:
        print(question + ":")
        answers.append(input(""))
        print("")
    
    connection.cursor.execute(insert_user, tuple(answers))
    

def login():
    pass
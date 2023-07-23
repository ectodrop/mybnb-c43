from database import connection
# from mysql.connector.cursor import CursorBase

def create_account():
    questions = [
        "Enter your name: ",
        "Enter your Social Insurance Number (SIN): ",
        "Enter your password: ",
        "Enter your date of birth (yyyy-mm-dd): ",
        "Enter your occupation (leave blank for none): ",
        "Enter your address: ",
    ]
    insert_user = ("INSERT INTO User "
               "(name, sin, password, birthday, occupation, address)"
               "VALUES (%s, %s, %s, %s, %s, %s)")
    find_user = ("SELECT name FROM User WHERE sin = %s")

    answers = []
    for question in questions:
        print(question)
        answers.append(input(""))
        print("")

    connection.cursor.execute(find_user, tuple(answers[1]))
    result = cursor.fetchone()
    if (result.rowcount != 0):
        print("An account with this SIN already exists.")
        return "", 0

    connection.cursor.execute(insert_user, tuple(answers))
    db.commit()
    return answers[0], answers[1]
    

def login():
    select_user = ("SELECT name FROM User WHERE sin = %s AND password = %s")
    questions = [
            "Enter your Social Insurance Number (SIN): ",
            "Enter your password: ",
        ]
    answers = []
    for question in questions:
        print(question)
        answers.append(input(""))
        print("")

    connection.cursor.execute(select_user, tuple(answers))
    result = cursor.fetchone()
    if (result.rowcount == 0):
        print ("Incorrect username or password.")
        return "", 0
    
    return result[0], answers[0]

def logout():
    return View.WeLCOME

def delete_account(sin):

    # delete bookings, listings, listings availabilities and amenities
    # or make add another field to User and mark as deleted

    delete_user = ("DELETE FROM User WHERE sin = %s")
    connection.cursor.execute(delete_user, (sin,))
    db.commit()
    return View.WELCOME

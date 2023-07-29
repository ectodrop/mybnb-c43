import database as db
from views import View
import notifications
import utils
from decorators import error_notif

@error_notif(default=0)
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

    answers = utils.display_form(questions)

    cursor = db.get_new_cursor()
    cursor.execute(find_user, (answers[1],))

    result = cursor.fetchone()
    if (result != None):
        notifications.set_notification("An account with this SIN already exists.")
        return 0

    # reset cursor
    cursor = db.get_new_cursor()
    cursor.execute(insert_user, tuple(answers))

    # commit
    db.get_connection().commit()
    notifications.set_notification("Hi,"+ answers[0])
    return answers[1]

@error_notif(default=0)
def login():
    select_user = ("SELECT name FROM User WHERE sin = %s AND password = %s")
    questions = [
            "Enter your Social Insurance Number (SIN): ",
            "Enter your password: ",
        ]
    answers = utils.display_form(questions)

    cursor = db.get_new_cursor()
    cursor.execute(select_user, tuple(answers))

    result = cursor.fetchone()
    if (result == None):
        notifications.set_notification("Incorrect username or password.")
        return 0

    notifications.set_notification("Hi,"+ result[0])
    return answers[0]

@error_notif()
def delete_account(sin):

    print("Confirm deletion of account?")
    choice = input("Input (y/n): ")
    if (choice == "n"):
        notifications.set_notification("Did not delete account.")
        return
    elif (choice != "y"):
        notifications.set_notification("Invalid entry.")
        return

    delete_user = ("DELETE FROM User WHERE sin = %s")
    db.get_new_cursor().execute(delete_user, (sin,))
    db.get_connection().commit()
    notifications.set_notification("Account deleted.")

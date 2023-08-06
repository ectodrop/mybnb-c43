import database as db
from views import View
import notifications
import utils
import validators
from decorators import error_notif
from datetime import date
@error_notif(default=0)
def create_account():
    questions = [
        ("Enter your name: ", validators.non_empty),
        ("Enter your Social Insurance Number (SIN): ", validators.is_int),
        ("Enter your password: ", validators.non_empty),
        ("Enter your date of birth (yyyy-mm-dd): ", validators.is_date),
        ("Enter your occupation (leave blank for none): ", validators.is_string),
        ("Enter your address: ", validators.non_empty),
    ]
    insert_user = ("INSERT INTO User "
               "(name, sin, password, birthday, occupation, address)"
               "VALUES (%s, %s, %s, %s, %s, %s)")
    find_user = ("SELECT name FROM User WHERE sin = %s")

    answers = utils.display_form(questions)
    birthdate = answers[3]
    try:
        age = (date.today() - utils.str_to_date(birthdate)).days / 365
    except:
        notifications.set_notification("Invalid birthdate")
        return 0
    
    if age < 18:
        notifications.set_notification("Must be 18 or older to create an account")
        return 0
    
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
            ("Enter your Social Insurance Number (SIN): ", validators.is_string),
            ("Enter your password: ", validators.is_string),
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
def delete_account(sin, curr_view):
    today = utils.date_to_str(date.today())
    bookings = f"SELECT * FROM Booking WHERE sin = {sin} AND end_date >= '{today}' AND status = 'ACTIVE'"
    cursor = db.get_new_cursor()
    cursor.execute(bookings)
    mybookings = cursor.fetchone()
    # all active bookings of listings that SIN owns
    if mybookings != None:
        notifications.set_notification("Cannot delete an account with active future bookings.")
        return curr_view
    listingbookings = f"SELECT * FROM Booking as b INNER JOIN Listing as l ON b.lid = l.lid WHERE l.sin = {sin} AND end_date >= '{today}' AND status = 'ACTIVE'"
    cursor = db.get_new_cursor()
    cursor.execute(listingbookings)
    mylistingbookings = cursor.fetchone()
    if mylistingbookings != None:
        notifications.set_notification("Cannot delete an account with listings that have active bookings.")
        return curr_view
    
    print("Confirm deletion of account?")
    choice = utils.get_answer("Input (y/n): ", validators.yes_or_no)
    if (choice == "n"):
        notifications.set_notification("Did not delete account.")
        return curr_view

    delete_user = ("DELETE FROM User WHERE sin = %s")
    db.get_new_cursor().execute(delete_user, (sin,))
    db.get_connection().commit()
    notifications.set_notification("Account deleted.")
    return View.WELCOME

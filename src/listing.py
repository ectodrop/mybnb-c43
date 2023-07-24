import database as db
import notifications
import random
from utils import display_form
from decorators import error_notif

@error_notif()
def create_listing(sin):
    query = ("INSERT INTO Listing "
               "(longitude,"
               "latitude,"
               "streetnum,"
               "streetname,"
               "city,"
               "country,"
               "zipcode,"
               "type,"
               "sin)"
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    questions = [
        "Enter the street #: ",
        "Enter the street name: ",
        "Enter the city: ",
        "Enter the country: ",
        "Enter the zipcode (A#A#A#): ",
        "Enter the Housing type: ",
    ]
    answers = [str(random.uniform(-90, 90)), str(random.uniform(-180,180))]

    answers += display_form(questions)

    cursor = db.get_new_cursor()
    cursor.execute(query, tuple(answers + [sin]))
    db.get_connection().commit()
    notifications.set_notification("Successfully created a listing")

import database as db
import notifications
import random
import utils
import windows
import datetime
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

    answers += utils.display_form(questions)

    cursor = db.get_new_cursor()
    cursor.execute(query, tuple(answers + [sin]))
    db.get_connection().commit()
    notifications.set_notification("Successfully created a listing")

@error_notif(default=0)
def select_listing(sin):
    get_listings = ("SELECT lid,streetnum,streetname,city,country,zipcode,btype  FROM Listing WHERE sin = %s")
    cursor = db.get_new_cursor()
    cursor.execute(get_listings, (sin,))
    result = cursor.fetchall()
    if result == None:
        notifications.set_notification("you don't have any listings!")
        return
    print("YOUR LISTINGS")
    print(f"{'id':5}{'street#':10}{'streetname':15}{'city':15}{'country':15}{'zipcode':10}{'type':15}")
    valid_ids = set()
    for row in result:
        (lid, streetnum, streetname, city, country, zipcode, btype ) = row
        valid_ids.add(lid)
        print(f"{lid:<5}{streetnum:10}{streetname:15}{city:15}{country:15}{zipcode:10}{btype:15}")
    questions = ["Select an id: "]
    
    lid = 0
    while True:
        [lid] = utils.display_form(questions)
        if int(lid) in valid_ids:
            break
        print("please enter a valid id")
    return lid

@error_notif()
def add_availablity(lid):
    getbookings = ("SELECT start_date, end_date, bid FROM Booking WHERE lid = %s")
    getavailabilities = ("SELECT date FROM Availability WHERE lid = %s ")
    insertavailability = ("INSERT INTO Availability(date, price, lid)"
                          "VALUES (%s,%s,%s)")
    
    
    # bookings
    cursor = db.get_new_cursor()
    cursor.execute(getbookings, (lid,))
    bookings = []
    result = cursor.fetchall()
    for (start, end, id) in result:
        s = utils.str_to_date(start)
        e = utils.str_to_date(end)
        delta = datetime.timedelta(days=1)
        while s <= e:
            bookings.append((utils.date_to_str(s), id))
            s += delta
    
    #availabilities
    cursor = db.get_new_cursor()
    cursor.execute(getavailabilities, (lid,))
    availabilities = [utils.date_to_str(date[0]) for date in cursor.fetchall()]
    
    # insert availability

    (start_date, end_date) = windows.display_calendar(bookings, availabilities)
    delta = datetime.timedelta(days=1)
    if not start_date or not end_date:
        notifications.set_notification("Did not add an availability")
        return
    s = utils.str_to_date(start_date)
    while s <= utils.str_to_date(end_date):
        cursor = db.get_new_cursor()
        # TODO replace 100 'price' with user input
        cursor.execute(insertavailability, (utils.date_to_str(s), 100, lid))
        s += delta
    db.get_connection().commit()
    notifications.set_notification(f"Added an availability from {start_date} to {end_date}")
    return 

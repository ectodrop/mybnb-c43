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
               "btype,"
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
    
    display_listings(sin)

    valid_ids = set(get_listing_ids(sin))
    if len(valid_ids) == 0:
        notifications.set_notification("you don't have any listings!")
        return

    questions = ["Select an id: "]
    
    lid = None
    while True:
        [lid] = utils.display_form(questions)
        if int(lid) in valid_ids:
            break
        print("please enter a valid id")
    return lid

@error_notif()
def update_availablity(lid, remove=False):
    
    # bookings
    bookings = get_bookings_dates(lid)
    
    #availabilities
    availabilities = get_available_dates(lid)
    
    (start_date, end_date) = windows.display_calendar(bookings, availabilities)
    if not start_date or not end_date:
        notifications.set_notification("Did not select any dates")
        return
    s = utils.str_to_date(start_date)
    e = utils.str_to_date(end_date)
    delta = datetime.timedelta(days=1)
    if s > e:
        notifications.set_notification("Cannot have start date greater than end date")
        return
    
    if not remove:
        if exists_availability(lid, start_date, end_date):
            notifications.set_notification("Date range already has an availability")
            return

        print(f"Adding availability from {start_date} to {end_date}...")

        price = input(f"Please set a price for this timeframe: ")
        # insert availability
        insertavailability = ("INSERT IGNORE INTO Availability(date, price, lid)"
                            "VALUES (%s,%s,%s)")

        while s <= e:
            cursor = db.get_new_cursor()
            cursor.execute(insertavailability, (utils.date_to_str(s), price, lid))
            s += delta
        notifications.set_notification(f"Added an availability from {start_date} to {end_date}")
        
    else:
        if not is_available(lid, start_date, end_date) or is_booked(lid, start_date, end_date):
            notifications.set_notification("Cannot remove availability in provided daterange")
            return
        remove_availability = ("DELETE FROM Availability "
                               f"WHERE lid = {lid} AND date >= '{start_date}' AND date <= '{end_date}'")
        cursor = db.get_new_cursor()
        cursor.execute(remove_availability)
        notifications.set_notification(f"Removed availability from {start_date} to {end_date}")

    db.get_connection().commit()
    return 

@error_notif()
def update_price(lid):
    # bookings
    bookings = get_bookings_dates(lid)
    
    #availabilities
    availabilities = get_available_dates(lid)
    (start_date, end_date) = windows.display_calendar(bookings, availabilities)
    if not start_date or not end_date:
        notifications.set_notification("Did not update price")
        return
    
    if utils.str_to_date(start_date) > utils.str_to_date(end_date):
        notifications.set_notification("Cannot have start date greater than end date")
        return

    if is_booked(lid, start_date, end_date):
        notifications.set_notification("Date range cannot include an active booking")
        return
    
    if not is_available(lid, start_date, end_date):
        notifications.set_notification("Date range must contain only available dates")
        return

    price = input(f"Set new price for {start_date} to {end_date}: ")
    update_pricing = (f"UPDATE Availability SET price = {price} "
                      f"WHERE date >= '{start_date}' AND date <= '{end_date}'")
    
    cursor = db.get_new_cursor()
    cursor.execute(update_pricing)
    db.get_connection().commit()
    notifications.set_notification(f"Price from {start_date} to {end_date} set to ${price}")

@error_notif()
def host_cancel_booking(lid):
    display_bookings(lid)
    bookings = (f"SELECT bid FROM Booking WHERE lid = {lid}")
    cursor = db.get_new_cursor()
    cursor.execute(bookings)
    result = cursor.fetchall()
    # flatten list
    booking_ids = {str(row[0]) for row in result}
    
    while True:
        id = input("Input a booking to cancel (type 'exit' to cancel): ")
        if id == 'exit':
            return
        if id in booking_ids:
            break
        print ("Not a valid id")
    
    cancel_booking = f"UPDATE Booking SET status='HOST_CANCELLED' WHERE bid = {id}"
    cursor = db.get_new_cursor()
    cursor.execute(cancel_booking)
    db.get_connection().commit()
    notifications.set_notification(f"Successfully cancelled booking#{id}")

# prints all listings for user SIN
def display_listings(sin):
    get_listings = ("SELECT lid,streetnum,streetname,city,country,zipcode,btype  FROM Listing WHERE sin = %s")
    cursor = db.get_new_cursor()
    cursor.execute(get_listings, (sin,))
    result = cursor.fetchall()
    print("YOUR LISTINGS")
    print(f"{'id':5}{'street#':10}{'streetname':15}{'city':15}{'country':15}{'zipcode':10}{'type':15}")
    for row in result:
        (lid, streetnum, streetname, city, country, zipcode, btype ) = row
        print(f"{lid:<5}{streetnum:10}{streetname:15}{city:15}{country:15}{zipcode:10}{btype:15}")

# prints all bookings for listing LID
def display_bookings(lid):
    bookings = (f"SELECT bid, name, start_date, end_date FROM Booking JOIN User WHERE lid = {lid}")
    cursor = db.get_new_cursor()
    cursor.execute(bookings)
    result = cursor.fetchall()
    print(f"LISTING#{lid} BOOKINGS")
    print(f"{'booking id':15}{'name':20}{'start date':15}{'end date':15}")
    for row in result:
        (bid, name, start, end) = row
        print(f"{bid:<15}{name:20}{utils.date_to_str(start):15}{utils.date_to_str(end):15}")
    
# returns a list of ids for each listing associated with the user
def get_listing_ids(sin):
    listings = ("SELECT lid FROM Listing WHERE sin = %s")
    cursor = db.get_new_cursor()
    cursor.execute(listings, (sin,))
    result = cursor.fetchall()
    return [row[0] for row in result]

# return list of tuples (date,price) where PRICE is the cost for renting on DATE
def get_available_dates(lid):
    getavailabilities = ("SELECT date, price FROM Availability WHERE lid = %s ")
    cursor = db.get_new_cursor()
    cursor.execute(getavailabilities, (lid,))
    result = cursor.fetchall()
    return result

# return a list of tuples (date, bid) where BID occupies date for listing LID
def get_bookings_dates(lid):
    getbookings = ("SELECT start_date, end_date, bid FROM Booking WHERE lid = %s AND status='ACTIVE'")

    bookings = []
    cursor = db.get_new_cursor()
    cursor.execute(getbookings, (lid,))
    bookings = []
    result = cursor.fetchall()
    delta = datetime.timedelta(days=1)
    for (start, end, id) in result:
        s = start
        while s <= end:
            bookings.append((s, id))
            s += delta
    return bookings

# if there is a booking within the specified daterange for the listing
def is_booked(lid, start, end):
    check_dates = (f"SELECT * FROM Booking WHERE lid = {lid} AND "
                    f"((start_date <= '{start}' AND end_date >= '{start}') OR "
                    f"(start_date <= '{end}' AND end_date >= '{end}') OR "
                    f"(start_date >= '{start}' AND end_date <= '{end}') OR "
                    f"(start_date <= '{start}' AND end_date >= '{start}'))")
    cursor = db.get_new_cursor()
    cursor.execute(check_dates)
    result = cursor.fetchone()
    return result != None

# if every date in the daterange has an associated availability for the listing
def is_available(lid, start, end):
    available = (f"SELECT * FROM Availability WHERE lid = {lid} AND "
                 f"date >= '{start}' AND date <= '{end}'")
    diff = utils.str_to_date(end)-utils.str_to_date(start)
    cursor = db.get_new_cursor()
    cursor.execute(available)
    return diff.days+1 == cursor.rowcount

# if there is at least 1 day in the range where listing is available
def exists_availability(lid, start, end):
    exists = (f"SELECT * FROM Availability WHERE lid = {lid} AND "
                 f"date >= '{start}' AND date <= '{end}'")
    cursor = db.get_new_cursor()
    cursor.execute(exists)
    return cursor.fetchone() != None

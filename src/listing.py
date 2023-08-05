import database as db
import notifications
import random
import utils
import windows
import datetime
import validators
from decorators import error_notif
from itertools import zip_longest

from views import View

@error_notif()
def create_listing(sin):
    insert_listing = ("INSERT INTO Listing "
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
        ("Enter the street #: ", validators.is_int),
        ("Enter the street name: ", validators.non_empty),
        ("Enter the city: ", validators.non_empty),
        ("Enter the country: ", validators.non_empty),
        ("Enter the zipcode (A#A#A#): ", validators.is_zipcode),
        ("Enter the Housing type: ", validators.is_contained(get_building_types())),
    ]
    answers = [str(random.uniform(-90, 90)), str(random.uniform(-180,180))]
    answers += utils.display_form(questions)

    building = answers[-1]
    query = "SELECT price FROM Building WHERE btype = %s"
    cursor = db.get_new_cursor()
    cursor.execute(query, (building,))
    price = cursor.fetchone()[0]

    query = "SELECT atype, price, category FROM Amenity"
    cursor = db.get_new_cursor()
    cursor.execute(query)
    remaining = cursor.fetchall()

    query += " WHERE category = %s or category = %s"
    params = ('Essential', 'Safety')
    cursor = db.get_new_cursor()
    cursor.execute(query, params)
    basic = cursor.fetchall()

    stop = "y"
    selected = []
    utils.clear_screen()
    print("[Host Toolkit Listing Price Per Day Estimate] $" + str(price))
    while (stop == "y"):
        print("Enter the amenities that your listing offers")
        remaining = print_remaining_amenities(remaining, selected)
        if not remaining:
            utils.clear_screen()
            print("All available amenities have been added.")
            print("Final: [Host Toolkit Listing Price Per Day Estimate] $" + str(price))
            print("Confirm creation of listing")
            stop = utils.get_answer("Enter (y/n): ", validators.yes_or_no)
            if choice == "n":
                notifications.set_notification("Did not create listing.")
                return
            break

        choice = int(utils.get_answer("Select from available amenities (enter 0 to submit the list): ", validators.in_range(0, len(remaining))))
        while choice > 0 and choice <= len(remaining):
            item = remaining[choice - 1]
            selected.append(item)
            price += item[1]
            if item in basic:
                basic.remove(item)
            choice = int(utils.get_answer("Select from available amenities (enter 0 to submit the list): ", validators.in_range(0, len(remaining))))

        print("\033[92mChanges saved.\033[0m")

        print("Updated: [Host Toolkit Listing Price Per Day Estimate] $" + str(price))

        if basic:
            print("We recommend adding the following essential and safety amenities: ")
            print_remaining_amenities(basic, [])
            print("Continue adding amenities?")
        else:
            print("All essential and safety amenities have been added. Continue adding amenities?")
        stop = utils.get_answer("Enter (y/n): ", validators.yes_or_no)
        utils.clear_screen()
    

    if stop != "y":
        print("Final: [Host Toolkit Listing Price Per Day Estimate] $" + str(price))
        print("Confirm creation of listing")
        choice = utils.get_answer("Enter (y/n): ", validators.yes_or_no)
        if choice == "n":
            notifications.set_notification("Did not create listing.")
            return

    cursor = db.get_new_cursor()
    cursor.execute(insert_listing, tuple(answers + [sin]))
    lid = int(cursor.lastrowid)

    if selected:
        params = []
        insert_amenities = ("INSERT INTO ListingAmenities(lid, atype) VALUES ")
        for item in selected:
            insert_amenities += "(%s, %s),"
            params += [lid, item[0]]
        cursor = db.get_new_cursor()
        cursor.execute(insert_amenities[:-1], tuple(params))
    db.get_connection().commit()

    notifications.set_notification("Listing created successfully.")


def print_remaining_amenities(amenities, selected, price = True):    
    categories = {"Essential":[], "Safety":[], "Standout":[]}
    for row in amenities:
        if row not in selected:
            category = row[2]
            categories[category].append(row)
    
    print(f"\033[94m{'ESSENTIAL':40}{'SAFETY':40}{'STANDOUT':40}\033[0m")
    count1 = 0
    count2 = len(categories["Essential"])
    count3 = count2 + len(categories["Safety"])
    def format_amenity(info, count):
        if info == None:
            return ""
        if price:
            return "{}. {}".format(count+1, info[0])
        return "{}. {} [+${}]".format(count+1, info[0], info[1])

    for c1, c2, c3 in zip_longest(categories["Essential"], categories["Safety"], categories["Standout"]):
        print(f"{format_amenity(c1, count1) :40}{format_amenity(c2, count2):40}{format_amenity(c3, count3):40}")
        count1 += 1
        count2 += 1
        count3 += 1
    remaining = categories["Essential"] + categories["Safety"] + categories["Standout"]


    return remaining


@error_notif(default=0)
def select_listing(sin):
    
    display_listings(sin)

    valid_ids = get_listing_ids(sin)
    if len(valid_ids) == 0:
        notifications.set_notification("No listings found")
        return 0
    
    lid = utils.get_answer("Select an id (enter blank to cancel): ", validators.is_contained(valid_ids).or_blank)
    if lid == "":
        return 0
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

        default_price = get_host_toolkit_pricing(lid)
        print("[Host Toolkit Listing Price Per Day Estimate]: $" + str(default_price))
        price = utils.get_answer(f"Please set a price for this timeframe (leave blank to use estimated price): ", validators.is_float.or_blank)
        if price == "":
            price = str(default_price)
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

    default_price = get_host_toolkit_pricing(lid)
    print("[Host Toolkit Listing Price Per Day Estimate]: $" + str(default_price))
    price = utils.get_answer(f"Set new price for {start_date} to {end_date} (leave blank to use estimated price): ", validators.is_float.or_blank)
    if price == "":
        price = str(default_price)
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
    
    id = utils.get_answer("Input a booking to cancel (blank to cancel nothing): ", validators.is_contained(booking_ids).or_blank)
    
    cancel_booking = f"UPDATE Booking SET status='HOST_CANCELLED' WHERE bid = {id}"
    cursor = db.get_new_cursor()
    cursor.execute(cancel_booking)
    db.get_connection().commit()
    notifications.set_notification(f"Successfully cancelled booking#{id}")

@error_notif()
def add_amenity(lid):
    insert = ("INSERT INTO ListingAmenities(atype, lid) VALUES (%s, %s)")
    
    get_amenities = ("SELECT atype, price, category FROM Amenity ORDER BY category")
    existing_amenities = f"SELECT atype, price, category  From ListingAmenities NATURAL JOIN Amenity WHERE lid = {lid}"
    
    cursor = db.get_new_cursor()
    cursor.execute(get_amenities)
    result = cursor.fetchall()

    cursor = db.get_new_cursor()
    cursor.execute(existing_amenities)
    existing = cursor.fetchall()

    amenities = print_remaining_amenities(result, existing)

    a = utils.get_answer("Choose amenity (Enter nothing to cancel): ", validators.in_range(1, len(amenities)+1).or_blank)
    if a == "":
        notifications.set_notification("Cancelled transaction")
        return
    cursor = db.get_new_cursor()
    cursor.execute(insert, (amenities[a-1], lid))
    db.get_connection().commit()
    notifications.set_notification(f"Added '{a}'")

@error_notif()
def remove_amenity(lid):
    existing_amenities = f"SELECT atype, category From ListingAmenities NATURAL JOIN Amenity WHERE lid = {lid}"
    cursor = db.get_new_cursor()
    cursor.execute(existing_amenities)
    result = cursor.fetchall()
    
    result = print_remaining_amenities(result, [], price = False)

    a = utils.get_answer("Choose an amenity to remove (blank to cancel): ", validators.in_range(1, len(result)+1).or_blank)
    
    delete = "DELETE FROM ListingAmenities WHERE lid = %s AND atype = %s"
    cursor = db.get_new_cursor()
    cursor.execute(delete, (lid, result[a-1]))
    db.get_connection().commit()
    notifications.set_notification(f"Removed '{result[a-1]}'")


@error_notif()
def remove_listing(lid):
    today = datetime.date.today()
    bookings = (f"SELECT bid FROM Booking WHERE lid = {lid} AND end_date >= '{utils.date_to_str(today)}' AND status = 'ACTIVE' ")
    cursor = db.get_new_cursor()
    cursor.execute(bookings)
    result = cursor.fetchall()
    
    if result:
        notifications.set_notification("Cannot delete a listing with active bookings.")
        return View.LISTING
    else:
        print("Confirm deletion of listing: ")
        choice = utils.get_answer("Input (y/n): ", validators.yes_or_no)
        if (choice != "y"):
            notifications.set_notification("Did not remove listing.")
            return View.LISTING
        remove_listing = (f"DELETE FROM Listing WHERE lid = {lid}")
        cursor = db.get_new_cursor()
        cursor.execute(remove_listing)
        db.get_connection().commit()
        notifications.set_notification("Listing removed successfully.")
        return View.HOST_DASH


# prints all listings for user SIN
def display_listings(sin):
    get_listings = ("SELECT lid,streetnum,streetname,city,country,zipcode,btype  FROM Listing WHERE sin = %s")
    cursor = db.get_new_cursor()
    cursor.execute(get_listings, (sin,))
    result = cursor.fetchall()

    print("YOUR LISTINGS")
    if result:
        print(f"{'id':5}{'street#':10}{'streetname':15}{'city':15}{'country':15}{'zipcode':10}{'type':15}")
    else:
        print("......No listings found!......")

    for row in result:
        (lid, streetnum, streetname, city, country, zipcode, btype ) = row
        print(f"{lid:<5}{streetnum:10}{streetname:15}{city:15}{country:15}{zipcode:10}{btype:15}")


# prints all bookings for listing LID
def display_bookings(lid):
    bookings = (f"SELECT bid, name, start_date, end_date FROM Booking NATURAL JOIN User WHERE lid = {lid}")
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


# get the estimated price per day calculated by the host toolkit
def get_host_toolkit_pricing(lid):
    query = (f"SELECT price FROM Building NATURAL JOIN Listing WHERE lid = {lid}")
    cursor = db.get_new_cursor()
    cursor.execute(query)
    price = cursor.fetchone()[0]
    query = (f"SELECT sum(price) FROM ListingAmenities NATURAL JOIN Amenity WHERE lid = {lid}")
    cursor = db.get_new_cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if result:
        price += result
    return price

def get_building_types():
    query = "SELECT btype FROM Building"
    cursor = db.get_new_cursor()
    cursor.execute(query)
    return [b for (b,) in cursor.fetchall()]

@error_notif()
def host_review_renter(lid, bid):
    display_bookings(lid)

    questions = [
        ("Enter a review for the renter (text): ", validators.non_empty),
        ("Enter a rating for the renter (1-5): ", validators.is_rating)
    ]
    review, rating = utils.display_form(questions)

    updatereview = "UPDATE Booking SET host_comment = %s, host_rating = %s WHERE bid = %s"
    cursor = db.get_new_cursor()
    cursor.execute(updatereview, (review, rating, bid))
    notifications.set_notification("Successfully updated review")
import database as db
import notifications
import utils
from decorators import error_notif
from views import View
from datetime import date, timedelta
from listing import get_bookings_dates, get_available_dates, is_booked, is_available
import windows
import validators

@error_notif()
def create_booking(sin, lid):
    bookings = get_bookings_dates(lid)
    availabilities = get_available_dates(lid)
    (start_date, end_date) = windows.display_calendar(bookings, availabilities)

    if not start_date or not end_date:
        notifications.set_notification("The booking was not made.")
        return
    
    if utils.str_to_date(start_date) > utils.str_to_date(end_date):
        notifications.set_notification("The booking start date cannot come after the booking end date.")
        return

    if is_booked(lid, start_date, end_date):
        notifications.set_notification("This listing is already booked on these days. Please create another booking.")
        return
    
    if not is_available(lid, start_date, end_date):
        notifications.set_notification("This listing is not available on one or more of the dates selected. Please create another booking.")
        return
    
    utils.clear_screen()
    get_price = ("SELECT sum(price) FROM Availability WHERE date >= %s AND date <= %s")
    cursor = db.get_new_cursor()
    cursor.execute(get_price, (start_date, end_date))
    (price,) = cursor.fetchone()

    print("Total price of booking: $" + str(price))
    print("Confirm booking of this listing from " + start_date + " to " + end_date + "?")
    choice = utils.get_answer("Enter (y/n): ", validators.yes_or_no)
    if choice == "n":
        notifications.set_notification("Booking failed.")
        return
    elif choice != "y":
        notifications.set_notification("Invalid entry.")
        return

    retrieve_user = ("SELECT creditcard from User WHERE sin = %s")
    cursor = db.get_new_cursor()
    cursor.execute(retrieve_user, (sin,))
    (creditcard,) = cursor.fetchone()
    if not creditcard:
        print("Please enter your 16-digit credit card number: ")
        creditcard = utils.get_answer("Credit Card Number : ", validators.is_valid_cc)

    update_user = ("UPDATE User SET creditcard = %s WHERE sin = %s")
    cursor = db.get_new_cursor()
    cursor.execute(update_user, (int(creditcard), sin))
    db.get_connection().commit()

    insert_booking = ("INSERT INTO Booking(sin, lid, status, start_date, end_date) VALUES(%s, %s, %s, %s, %s)")
    params = (sin, lid, 'ACTIVE', start_date, end_date)
    cursor = db.get_new_cursor()
    cursor.execute(insert_booking, params)
    db.get_connection().commit()

    update_availablity = ("UPDATE Availability SET booked = True WHERE lid = %s AND date >= %s and date <= %s")
    params = (lid, start_date, end_date)
    cursor = db.get_new_cursor ()
    cursor.execute(update_availablity, params)
    db.get_connection().commit()

    notifications.set_notification("Booking created successfully.")


@error_notif(default=[])
def print_amenities_list():
    print("AMENITIES")
    amenities = ["Wifi", "TV", "Kitchen", "Washer", "AC", "Free Parking", "Paid Parking", "Dedicated Workspace", 
                 "Pool", "Hot Tub", "Patio", "Fire Pit", "Grill", "Outdoor dining", "Pool Table", "Indoor Fireplace",
                 "Piano", "Exercise", "Lake Access", "Beach Access", "Smoke Alarm", "First Aid Kit", "Fire Extinguisher", "Carbon Monoxide Alarm"]
    for i in range(len(amenities)):
        print(str(i + 1) + ". " + amenities[i])
    return amenities


@error_notif()
def listing_info(sin, lid):
    print_listing_amenities(lid)

    print("Please select an option: ")
    print("1. Book this listing")
    print("2. Return to browsing listings")
    choice = input("Enter a choice: ")
    if choice == "1":
        create_booking(sin, lid)
    elif choice != "2":
        notifications.set_notification("Invalid entry.")


@error_notif()
def listing_options(sin, valid_ids):
    lid = utils.get_answer("Enter a listing ID (enter blank to cancel): ", validators.is_contained(valid_ids).or_blank)

    if lid == "":
        notifications.set_notification("Cancelled")
    else:
        print("Listing Information")
        listing_info(sin, int(lid))


@error_notif(default={})
def display_listings(get_listings, answers, show_distance):
    cursor = db.get_new_cursor()
    cursor.execute(get_listings, tuple(answers))
    result = cursor.fetchall()
    
    print("AVAILABLE LISTINGS")
    if (result and show_distance):
        print(f"{'ID':5}{'Host Name':15}{'Street #':10}{'Street Name':15}{'City':15}{'Country':15}{'Zipcode':10}{'Type':15}{'Avg Price/Day':15}{'Min Price/Day':15}{'Max Price/Day':15}{'Distance':8}")
    elif (result):
        print(f"{'ID':5}{'Host Name':15}{'Street #':10}{'Street Name':15}{'City':15}{'Country':15}{'Zipcode':10}{'Type':15}{'Avg Price/Day':15}{'Min Price/Day':15}{'Max Price/Day':15}")
    else:
        print("...No available listings found!...")

    valid_ids = set()
    for row in result:
        if (show_distance):
            (lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max, distance) = row
            print(f"{lid:<5}{name:15}{streetnum:10}{streetname:15}{city:15}{country:15}{zipcode:10}{btype:15}{round(avg, 2):<15}{round(min, 2):<15}{round(max, 2):<15}{round(distance, 2):8}")
        else:
            (lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max) = row
            print(f"{lid:<5}{name:15}{streetnum:10}{streetname:15}{city:15}{country:15}{zipcode:10}{btype:15}{round(avg, 2):<15}{round(min, 2):<15}{round(max, 2):<15}")
        valid_ids.add(lid)
    print("")
    return valid_ids


@error_notif(default=("", []))
def filter_search(search_query, original, for_distance):
    additional_query = "date >= %s"
    tmr_date = utils.date_to_str(date.today() + timedelta(1))
    additional_params = [tmr_date]
    choice = utils.get_answer("Filter by availability? Input (y/n): ", validators.yes_or_no)
    if (choice == "y"):
        start, end = windows.display_calendar([],[])
        if start != None and end != None:
            additional_query += " AND date <= %s"
            additional_params = [start, end]

    choice = utils.get_answer("Filter by price? Input (y/n): ", validators.yes_or_no)
    if (choice == "y"):
        questions = [("Enter the minimum price per day: ", validators.is_int), ("Enter the maximum price per day: ", validators.is_int)]
        [min_price, max_price] = utils.display_form(questions)
        additional_query += " AND price >= %s AND price <= %s"
        additional_params += [float(min_price), float(max_price)]
    
    search_query[3] = additional_query
    original[3] = additional_query

    choice = utils.get_answer("Filter by amenities? Input (y/n): ", validators.yes_or_no)
    if (choice == "y"):
        notifications.set_notification("Displaying results with updated filters.")
        amenities = print_amenities_list()
        selected = []
        choice = int(utils.get_answer("Select amenities (enter 0 to submit the list): ", validators.in_range(0, len(amenities))))
        while choice > 0 and choice <= len(amenities):
            selected.append(amenities[choice - 1])
            choice = int(utils.get_answer("Select amenities (enter 0 to submit the list): ", validators.in_range(0, len(amenities))))
        if (choice > len(amenities) or choice < 0):
            print("Invalid entry.")

        if selected:
            print("Amenities selected.")
            division_query = ("SELECT DISTINCT x.lid FROM ListingAmenities AS x WHERE NOT EXISTS "
                              "(SELECT * FROM (SELECT atype from Amenity WHERE atype in " + str(selected).replace("[", "(").replace("]", ")") +
                              ") AS y WHERE NOT EXISTS (SELECT * FROM ListingAmenities AS z "
                              "WHERE (z.lid=x.lid) AND (z.atype=y.atype)))")
            if for_distance:
                search_query = ["SELECT * FROM (" + division_query + ") AS A NATURAL JOIN ("] + original[:-1] + [") AS B"] + original[-1:]
            else:
                search_query = ["SELECT * FROM (" + division_query + ") AS A NATURAL JOIN ("] + original + [") AS B"]
        else:
            print("No amenities selected.")
            return original, additional_params
    notifications.set_notification("Displaying results with updated filters.")
    return search_query, additional_params


@error_notif()
def search_loop(sin, original, original_params, for_distance):
    sorted = for_distance
    search_query = original
    params = original_params
    while(True):
        get_listings = " ".join(search_query)
        valid_ids = display_listings(get_listings, params, for_distance)
        print("Please select an option: ")
        print("1. Return to browsing all listings")
        if (valid_ids):
            print("2. View details of a listing")
            print("3. Filter search results")
            print("4. Order listings by average price")
        choice = input("Enter a choice: ")
        if choice == "2" and valid_ids:
            listing_options(sin, valid_ids)
        elif choice == "1":
            notifications.set_notification("Search completed.")
            return
        elif choice == "3" and valid_ids:
            search_query, more_params = filter_search(search_query, original, for_distance)
            if for_distance:
                params = original_params[:3]
                params += more_params
                params.append(original_params[-1]) 
            else:
                params = original_params[:-1]
                params += more_params
        elif choice == "4" and valid_ids:
            sorted = sort_by_price(search_query, sorted, for_distance)
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


@error_notif()
def search_by_addr(sin):
    utils.clear_screen()
    tmr_date = utils.date_to_str(date.today() + timedelta(1))
    print("Searching by Address")
    questions = [
        ("Enter the street # (leave blank for any): ", validators.is_int.or_blank),
        ("Enter the street name (leave blank for any): ", validators.is_string),
        ("Enter the city (leave blank for any): ", validators.is_string),
        ("Enter the country (leave blank for any): ", validators.is_string),
        ("Enter the zipcode (leave blank for any): ", validators.is_zipcode.or_blank)
    ]
    [streetnum, streetname, city, country, zipcode] = utils.display_form(questions)
    original = ["SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max FROM",
                    "(SELECT * FROM Listing NATURAL JOIN User WHERE sin != " + str(sin) + " AND (streetnum = %s OR %s = '') AND (streetname = %s OR %s = '') AND (city = %s OR %s = '') AND (country = %s OR %s = '') AND (zipcode = %s OR %s = '')) AS S NATURAL JOIN",
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE not booked AND ",
                    "date >= %s",
                    ") AS R GROUP BY lid) AS T",
                ]
    original_params = [streetnum, streetnum, streetname, streetname, city, city, country, country, zipcode, zipcode, tmr_date]
    search_loop(sin, original, original_params, False)


@error_notif()
def search_by_zipcode(sin):
    utils.clear_screen()
    tmr_date = utils.date_to_str(date.today() + timedelta(1))
    print("Searching by Zipcode")
    zipcode = utils.get_answer("Enter a zipcode: ", validators.is_zipcode)
    original = ["SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max FROM",
                    "(SELECT * FROM Listing NATURAL JOIN User WHERE sin != " + str(sin) + ''' AND zipcode like %s"___") AS S NATURAL JOIN''',
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE not booked AND ",
                    "date >= %s",
                    ") AS R GROUP BY lid) AS T"
                ]
    original_params = [zipcode[:3], tmr_date]
    search_loop(sin, original, original_params, False)
        

@error_notif()
def search_by_location(sin):
    utils.clear_screen()
    tmr_date = utils.date_to_str(date.today() + timedelta(1))
    print("Searching by Location")
    questions = [
        ("Enter a longitude: ", validators.in_range(-180, 180)),
        ("Enter a latitude: ", validators.in_range(-90, 90)),
        ("Enter a radius of search (leave blank for a default of 50 km): ", validators.is_float.or_blank)
    ]
    [longi, lati, dist] = utils.display_form(questions)
    dist_params = [float(lati), float(lati), float(longi), float(dist) if dist else 50.0 ]
    original = ["SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max, 12742*temp*sin(SQRT(temp)) AS distance FROM",
                    "(SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, POWER(sin((latitude - %s)/2), 2) + cos(latitude)*cos(%s)*POWER(sin((longitude - %s)/2), 2) AS temp FROM Listing NATURAL JOIN User WHERE sin != " + str(sin) + ") AS S NATURAL JOIN",
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE not booked AND ",
                    "date >= %s",
                    ") AS R GROUP BY lid) AS T",
                    "WHERE 12742*temp*sin(SQRT(temp)) <= %s",
                    "ORDER BY distance ASC"
                ]
    original_params = dist_params[:3]
    original_params += [tmr_date, dist_params[-1]]
    search_loop(sin, original, original_params, True)


@error_notif(default=False)
def sort_by_price(search_query, sorted, for_distance):
    utils.clear_screen()
    print("Please select an option: ")
    print("1. Show highest average price first")
    print("2. Show lowest average price first")
    choice = input("Enter a choice: ")
    if choice == "1":
        order = "DESC"
        if not sorted:
            search_query.append("")
            sorted = True
        notifications.set_notification("Sorting by highest average price first.")
    elif choice == "2":
        order = "ASC"
        if not sorted:
            search_query.append("")
            sorted = True
        notifications.set_notification("Sorting by lowest average price first.")
    else:
        notifications.set_notification("Invalid entry.")
        return sorted

    if for_distance:
        search_query[-1] = ("ORDER BY avg " + order + ", distance ASC")
    else:
        search_query[-1] = ("ORDER BY avg " + order)
        
    return sorted


@error_notif()
def browse_listings(sin):
    utils.clear_screen()
    search_query = ["SELECT DISTINCT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max FROM",
                    "(SELECT * FROM Listing NATURAL JOIN User WHERE sin != " + str(sin) + ") AS S NATURAL JOIN",
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE not booked AND ",
                    "date >= %s",
                    ") AS R GROUP BY lid) AS T",
                ]
    original = search_query
    tmr_date = utils.date_to_str(date.today() + timedelta(1))
    answers = [tmr_date]
    sorted = False
    while (True):
        print("Browse and Book Listings")
        get_listings = " ".join(search_query)
        valid_ids = display_listings(get_listings, answers, False)
        print("Please select an option: ")
        print("1. Return to dashboard")
        if (valid_ids):
            print("2. View details of a listing")
            print("3. Search by longitude/latitude")
            print("4. Search listings with similar zipcodes")
            print("5. Search for listing by address")
            print("6. Filter all listings")
            print("7. Order listings by average price")
        choice = input("Enter a choice: ")
        if choice == "1":
            return
        elif valid_ids:
            if choice == "2":
                listing_options(sin, valid_ids)
            elif choice == "3":
                search_by_location(sin)
            elif choice == "4":
                search_by_zipcode(sin)
            elif choice == "5":
                search_by_addr(sin)
            elif choice == "6":
                search_query, answers = filter_search(search_query, original, False)
            elif choice == "7":
                sorted = sort_by_price(search_query, sorted, False) 
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


@error_notif()
def print_listing_amenities(lid):
    get_listing_amenities = ("SELECT atype FROM Amenity NATURAL JOIN ListingAmenities WHERE lid = %s AND category = %s")
    categories = ("SAFETY", "ESSENTIAL", "STANDOUT")
    for i in range(3):
        print(categories[i], "AMENITIES:")
        cursor = db.get_new_cursor()
        cursor.execute(get_listing_amenities, (lid, categories[i]))
        result = cursor.fetchall()
        if (not result):
            print("......None......")
            continue
        for row in result:
            print("   -  ", row[0])


@error_notif(default={})
def display_bookings(sin, is_past):
    curr_date = utils.date_to_str(date.today())
    get_bookings = ("SELECT bid, start_date, end_date, name, streetnum, streetname, city, country, zipcode, btype" +
                    " from Listing NATURAL JOIN User NATURAL JOIN (SELECT bid, lid, sin AS rsin, start_date, end_date from Booking WHERE sin = %s" +
                    " AND status = 'ACTIVE' AND end_date")
    if (is_past):
        get_bookings += " < %s) AS R"
        timing = "PAST"
    else:
        get_bookings += " >= %s) AS R"
        timing = "FUTURE"

    cursor = db.get_new_cursor()
    cursor.execute(get_bookings, (sin, curr_date))
    result = cursor.fetchall()
    print("YOUR ", timing, " BOOKINGS")

    if (result):
        print(f"{'ID':5}{'Start Date':12}{'End Date':12}{'Host Name':15}{'Street #':10}{'Street Name':15}{'City':15}{'Country':15}{'Zipcode':10}{'Type':15}")
    else:
        print("......No bookings found!......")

    valid_ids = set()
    for row in result:
        (bid, start_date, end_date, name, streetnum, streetname, city, country, zipcode, btype ) = row
        valid_ids.add(bid)
        print(f"{bid:<5}{str(start_date):12}{str(end_date):12}{name:15}{streetnum:10}{streetname:15}{city:15}{country:15}{zipcode:10}{btype:15}")
    print("")
    return valid_ids

@error_notif()
def client_cancel_booking(valid_ids):
    bid = utils.get_answer("Enter a booking ID: ", validators.is_contained(valid_ids))

    if (int(bid) not in valid_ids):
        notifications.set_notification("Invalid booking ID. Please try again.")
        return
    else:
        print("Confirm cancellating of booking: ")
        choice = utils.get_answer("Input (y/n): ", validators.yes_or_no)
        if (choice != "y"):
            notifications.set_notification("Did not cancel booking.")
            return
        cancel_booking = ("UPDATE Booking SET status = %s WHERE bid = %s")
        cursor = db.get_new_cursor()
        cursor.execute(cancel_booking, ('RENTER_CANCELLED', int(bid)))
        db.get_connection().commit()

        get_booking = f"SELECT lid, start_date, end_date FROM Booking WHERE bid = {bid}"
        cursor = db.get_new_cursor()
        cursor.execute(get_booking)
        params = cursor.fetchone()

        update_availablity = ("UPDATE Availability SET booked = False WHERE lid = %s AND date >= %s and date <= %s")
        cursor = db.get_new_cursor ()
        cursor.execute(update_availablity, params)
        db.get_connection().commit()

        notifications.set_notification("Booking cancelled successfully.")


@error_notif()
def future_bookings(sin):
    utils.clear_screen()
    while (True):
        print("Future Bookings")
        valid_ids = display_bookings(sin, False)
        print("Please select an option: ")
        print("1. Return to dashboard")
        if (valid_ids):
            print("2. Cancel a booking")
        choice = input("Enter a choice: ")
        if valid_ids and choice == "2":
            client_cancel_booking(valid_ids)
        elif choice == "1":
            return
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


@error_notif()
def print_existing_reviews(result, bid):
    statements = ["Rating for host: ", "Comment for host: ", "Rating for listing: ", "Comment for listing: "]
    print("Your Existing Reviews for Booking #" + bid)
    for i in range(0, 4):
        print(statements[i], result[i] if result[i] else '-')


@error_notif()
def confirm_responses(responses, bid, existing_review):
    params = []
    types = ("rating", "comment")

    for i in  range(2):
        print("Replace new", types[i], "with previous", types[i] + "?")
        choice = utils.get_answer("Input (y/n): ", validators.yes_or_no)
        if (choice == "y"):
            params.append(responses[i])
        elif (choice == "n"):
            params.append(existing_review[i])
        else:
            notifications.set_notification("Invalid entry.")
            return
    return [int(params[0]) if params[0] else None, params[1] if params[1] else None, int(bid)]


@error_notif()
def post_review(valid_ids):
    bid = utils.get_answer("Enter a booking ID: ", validators.is_contained(valid_ids))

    if (int(bid) not in valid_ids):
        notifications.set_notification("Invalid booking ID. Please try again.")
        return
    else:
        find_booking_reviews = ("SELECT renter_host_rating, renter_host_comment, renter_listing_rating, renter_listing_comment, end_date FROM Booking WHERE bid = %s")
        cursor = db.get_new_cursor()
        cursor.execute(find_booking_reviews, (int(bid),))
        result = cursor.fetchone()

        print_existing_reviews(result, bid)
        (host_rating, host_comment, listing_rating, listing_comment, end_date) = result
    
        curr_date = date.today()
        days_diff = (curr_date - end_date).days
        if (days_diff > 180 or days_diff < 0):
            notifications.set_notification("Cannot update reviews/ratings of stays that have not been completed within the past 180 days.")
            return

        print("Please select an option: ")
        print("1. Update review for host")
        print("2. Update review for listing")
        print("3. Return to all past bookings")
        choice = input("Enter a choice: ")
        if choice == "1":
            update_review = ("UPDATE Booking SET renter_host_rating = %s, renter_host_comment = %s WHERE bid = %s")
            existing_review = (host_rating, host_comment)
        elif choice == "2":
            update_review = ("UPDATE Booking SET renter_listing_rating = %s, renter_listing_comment = %s WHERE bid = %s")
            existing_review = (listing_rating, listing_comment)
        elif choice == "3":
            notifications.set_notification("Back to viewing past bookings.")
            return
        else:
            notifications.set_notification("Invalid entry.")
            return


        rating = utils.get_answer("Enter a rating from 1 to 5 (leave blank for none): ", validators.is_rating.or_blank)
        comment = utils.get_answer("Enter a comment (leave blank for none): ", validators.is_string)

        params = confirm_responses([rating, comment], bid, existing_review)

        cursor = db.get_new_cursor()
        cursor.execute(update_review, params)
        db.get_connection().commit()
        notifications.set_notification("Review updated successfully.")


@error_notif()
def past_bookings(sin):
    utils.clear_screen()
    while (True):
        print("Past Bookings")
        valid_ids = display_bookings(sin, True)
        print("Please select an option: ")
        print("1. Return to dashboard")
        if (valid_ids):
            print("2. Review a booking")
        choice = input("Enter a choice: ")
        if valid_ids and choice == "2":
            post_review(valid_ids)
        elif choice == "1":
            return
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()
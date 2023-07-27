import database as db
import notifications
import utils
from decorators import error_notif
from views import View
from datetime import date, timedelta


@error_notif()
def create_booking(sin, lid):
    # display availabilities
    # book some availabilities
    pass

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
    questions = [
        "Enter a listing ID: "
    ]
    [lid] = utils.display_form(questions)

    if (int(lid) not in valid_ids):
        notifications.set_notification("Listing ID not present in search results. Please try again.")
    else:
        print("Listing Information")
        listing_info(sin, lid)


@error_notif()
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
    return valid_ids


@error_notif()
def filter_search(search_query, answers):
    additional_query = "date >= %s"
    additional_params = answers
    choice = input("Filter by availability? Input (y/n): ")
    if (choice == "y"):
        questions = ["Enter the start date of availabilities (YYYY-MM-DD): ", "Enter the end date of availabilities (YYYY-MM-DD): "]
        dates = utils.display_form(questions)
        additional_query += " AND date <= %s"
        additional_params = dates
    elif (choice != "n"):
        print("Invalid entry.")

    choice = input("Filter by price? Input (y/n): ")
    if (choice == "y"):
        questions = ["Enter the minimum price per day: ", "Enter the maximum price per day: "]
        [min_price, max_price] = utils.display_form(questions)
        additional_query += " AND price >= %s AND price <= %s"
        additional_params += [float(min_price), float(max_price)]
    elif (choice != "n"):
        print("Invalid entry.")

    search_query[3] = additional_query
    return additional_params


@error_notif()
def search_loop(sin, search_query, params, for_distance):
    sorted = False
    while(True):
        get_listings = " ".join(search_query)
        valid_ids = display_listings(get_listings, params, for_distance)
        print("Please select an option: ")
        print("1. Return to browsing all listings")
        if (valid_ids):
            print("2. View details of a listing")
            print("3. Order listings by average price")
        choice = input("Enter a choice: ")
        if choice == "2" and valid_ids:
            listing_options(sin, valid_ids)
        elif choice == "1":
            notifications.set_notification("Search completed.")
            return
        elif choice == "3" and valid_ids:
            sorted = sort_by_price(search_query, sorted)
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


@error_notif()
def search_by_addr(sin, answers):
    utils.clear_screen()
    print("Searching by Address")
    questions = [
        "Enter the street #: ",
        "Enter the street name: ",
        "Enter the city: ",
        "Enter the country: ",
        "Enter the zipcode: "
    ]
    params = utils.display_form(questions)
    search_query = ["SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max FROM",
                    "(SELECT * FROM Listing NATURAL JOIN User WHERE streetnum = %s AND streetname = %s AND city = %s AND country = %s AND zipcode = %s) AS S NATURAL JOIN",
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE",
                    "date >= %s",
                    ") AS R GROUP BY lid) AS T",
                ]
    params += filter_search(search_query, answers)
    search_loop(sin, search_query, params, False)


@error_notif()
def search_by_zipcode(sin, answers):
    utils.clear_screen()
    print("Searching by Zipcode")
    questions = [
        "Enter a zipcode: "
    ]
    [zipcode] = utils.display_form(questions)
    search_query = ["SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max FROM",
                    '''(SELECT * FROM Listing NATURAL JOIN User WHERE zipcode like %s"___") AS S NATURAL JOIN''',
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE",
                    "date >= %s",
                    ") AS R GROUP BY lid) AS T"
                ]
    params = [zipcode[:3]]
    params += filter_search(search_query, answers)
    search_loop(sin, search_query, params, False)
        

@error_notif()
def search_by_location(sin, answers):
    utils.clear_screen()
    print("Searching by Location")
    questions = [
        "Enter a longitude: ",
        "Enter a latitude: ",
        "Enter a radius of search (leave blank for a default of 50 km): "
    ]
    [longi, lati, dist] = utils.display_form(questions)
    dist_params = [float(lati), float(lati), float(longi), float(dist) if dist else 50.0 ]
    search_query = ["SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max, 12742*temp*sin(SQRT(temp)) AS distance FROM",
                    "(SELECT lid, streetnum, streetname, city, country, zipcode, btype, name, POWER(sin((latitude - %s)/2), 2) + cos(latitude)*cos(%s)*POWER(sin((longitude - %s)/2), 2) AS temp FROM Listing NATURAL JOIN User) AS S NATURAL JOIN",
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE",
                    "date >= %s",
                    ") AS R GROUP BY lid) AS T",
                    "WHERE 12742*temp*sin(SQRT(temp)) <= %s"
                ]
    params = dist_params[:3]
    params += filter_search(search_query, answers)
    params.append(dist_params[3])
    search_loop(sin, search_query, params, True)


@error_notif()
def sort_by_price(search_query, sorted):
    utils.clear_screen()
    print("Please select an option: ")
    print("1. Show highest average price first")
    print("2. Show lowest average price first")
    choice = input("Enter a choice: ")
    if choice == "1":
        if not sorted:
            search_query.append("ORDER BY avg DESC")
            sorted = True
        else:
            search_query[-1] = "ORDER BY avg DESC"
            notifications.set_notification("Sorting by highest average price first.")
    elif choice == "2":
        if not sorted:
            search_query.append("ORDER BY avg ASC")
            sorted = True
        else:
            search_query[-1] = "ORDER BY avg ASC"
            notifications.set_notification("Sorting by lowest average price first.")
    else:
        notifications.set_notification("Invalid entry.")
    return sorted

@error_notif()
def browse_listings(sin):
    utils.clear_screen()
    search_query = ["SELECT DISTINCT lid, streetnum, streetname, city, country, zipcode, btype, name, avg, min, max FROM",
                    "(SELECT * FROM Listing NATURAL JOIN User) AS S NATURAL JOIN",
                    "(SELECT lid, avg(price) AS avg, min(price) AS min, max(price) AS max FROM (SELECT * from Availability WHERE date >= %s) AS R GROUP BY lid) AS T",
                ]
    tmr_date = date.today() + timedelta(1)
    sorted = False
    while (True):
        print("Browse and Book Listings")
        get_listings = " ".join(search_query)
        answers = [tmr_date]
        valid_ids = display_listings(get_listings, answers, False)
        print("Please select an option: ")
        print("1. Return to dashboard")
        if (valid_ids):
            print("2. View details of a listing")
            print("3. Search by longitude/latitude")
            print("4. Search listings with similar zipcodes")
            print("5. Search for listing by address")
            print("6. Order listings by average price")
        choice = input("Enter a choice: ")

        if choice == "2" and valid_ids:
            listing_options(sin, valid_ids)
        elif choice == "3" and valid_ids:
            search_by_location(sin, answers)
        elif choice == "4" and valid_ids:
            search_by_zipcode(sin, answers)
        elif choice == "5" and valid_ids:
            search_by_addr(sin, answers)
        elif choice == "6" and valid_ids:
            sorted = sort_by_price(search_query, sorted)
        elif choice == "1":
            return
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


@error_notif()
def display_bookings(sin, is_past):
    curr_date = date.today()
    get_bookings = ("SELECT bid, start_date, end_date, name, streetnum, streetname, city, country, zipcode, btype" +
                    " from Listing NATURAL JOIN User NATURAL JOIN (SELECT bid, lid, sin AS rsin, start_date, end_date from Booking WHERE sin = %s" +
                    " AND status = 'ACTIVE' AND start_date")
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
    return valid_ids


def cancel_booking(valid_ids):
    questions = [
        "Enter a booking id: "
    ]
    [bid] = utils.display_form(questions)

    if (int(bid) not in valid_ids):
        notifications.set_notification("Invalid booking ID. Please try again.")
        return
    else:
        print("Confirm cancellating of booking: ")
        choice = input("Input (y/n): ")
        if (choice != "y"):
            notifications.set_notification("Did not cancel booking.")
            return
        cancel_booking = ("UPDATE Booking SET status = 'RENTER_CANCELLED' WHERE bid = %s")
        cursor = db.get_new_cursor()
        cursor.execute(cancel_booking, (int(bid),))
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
            cancel_booking(valid_ids)
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
        choice = input("Input (y/n): ")
        if (choice == "y"):
            params += responses[i]
        elif (choice == "n"):
            params += existing_review[i]
        else:
            notifications.set_notification("Invalid entry.")
            return

    params += int(bid)
    return params


@error_notif()
def post_review(valid_ids):
    questions = [
        "Enter a booking id: ",
        "Enter a rating from 1 to 5 (leave blank for none): ",
        "Enter a comment (leave blank for none): "
    ]
    [bid] = utils.display_form(questions[:1])
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
        choice = input("Enter a choice: ")
        if choice == "1":
            update_review = ("UPDATE Booking SET renter_host_rating = %s, renter_host_comment = %s WHERE bid = %s")
            existing_review = (listing_rating, lising_comment)
        elif choice == "2":
            update_review = ("UPDATE Booking SET renter_listing_rating = %s, renter_listing_comment = %s WHERE bid = %s")
            existing_review = (host_rating, host_comment)
        else:
            notifications.set_notification("Invalid entry.")
            return

        params = confirm_responses(utils.display_form(questions[1:]), bid, existing_review)

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
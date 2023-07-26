import database as db
import notifications
import utils
from decorators import error_notif
from views import View
from datetime import date


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
        listing_info(sin, lid)


@error_notif()
def display_listings(get_listings, answers):
    cursor = db.get_new_cursor()
    cursor.execute(get_listings, tuple(answers))
    result = cursor.fetchall()

    print("AVAILABLE LISTINGS")
    if (result):
        print(f"{'ID':5}{'Host Name':15}{'Street #':10}{'Street Name':15}{'City':15}{'Country':15}{'Zipcode':10}{'Type':15}")
    else:
        print("...No available listings found!...")

    valid_ids = set()
    for row in result:
        (lid, streetnum, streetname, city, country, zipcode, btype, name) = row
        valid_ids.add(lid)
        print(f"{lid:<5}{name:15}{streetnum:10}{streetname:15}{city:15}{country:15}{zipcode:10}{btype:15}")
    return valid_ids


@error_notif()
def filter_search():
    print("Filter by price range? ")
    choice = input("Input (y/n): ")
    print("Filter by amenities offered? ")
    choice = input("Input (y/n): ")
    print("Filter by availability dates? ")
    choice = input("Input (y/n): ")


@error_notif()
def search_by_addr(sin, get_listings, answers):
    questions = [
        "Enter the street #: ",
        "Enter the street name: ",
        "Enter the city: ",
        "Enter the country: ",
        "Enter the zipcode: "
    ]
    answers += utils.display_form(questions)
    get_listings += " AND streetnum = %s AND streetname = %s AND city = %s AND country = %s AND zipcode = %s"
    #filter_search()

    while(True):
        valid_ids = display_listings(get_listings, answers)
        if (len(valid_ids) == 1):
            listing_info(sin, list(valid_ids)[0])
            notifications.set_notification("Search completed.")
            return
        else:
            print("Please select an option: ")
            print("1. Return to browsing all listings")
            if (valid_ids):
                print("2. View details of a listing")
            choice = input("Enter a choice: ")
            if choice == "2" and valid_ids:
                listing_options(sin, valid_ids)
            elif choice == "1":
                notifications.set_notification("Search completed.")
                return
            else:
                notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


@error_notif()
def search_by_zipcode(sin, get_listings, answers):
    questions = [
        "Enter a zipcode: "
    ]
    [zipcode] = utils.display_form(questions)
    answers.append(zipcode[:3])
    get_listings += ''' AND zipcode LIKE %s"___"'''
    #filter_search()
    while(True):
        valid_ids = display_listings(get_listings, answers)
        print("Please select an option: ")
        print("1. Return to browsing all listings")
        if (valid_ids):
            print("2. View details of a listing")
        choice = input("Enter a choice: ")
        if choice == "2" and valid_ids:
            listing_options(sin, valid_ids)
        elif choice == "1":
            notifications.set_notification("Search completed.")
            return
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()
        

@error_notif()
def search_by_location(sin, answers):
    questions = [
        "Enter a longitude: ",
        "Enter a latitude: ",
        "Enter a radius of search (leave blank for a default of 10): "
    ]
    [longi, lati, dist] = utils.display_form(questions)
    dist_params = [int(longi), int(lati), int(dist) if dist else 10 ]
    get_listings = ("SELECT lid, streetnum, streetname, city, country, zipcode, btype, name FROM "
                    "(SELECT DISTINCT lid, streetnum, streetname, city, country, zipcode, btype, name,"
                    " SQRT(POWER(longitude - %s, 2) + POWER(latitude - %s, 2)) AS distance FROM"
                    " Availability NATURAL JOIN Listing NATURAL JOIN User WHERE date > %s) AS R WHERE distance <= %s"
                    " ORDER BY distance ASC")
    #filter_search
    params = dist_params[:2] + answers + [dist_params[2]]
    # sort by price
    while(True):
        valid_ids = display_listings(get_listings, params)
        print("Please select an option: ")
        print("1. Return to browsing all listings")
        if (valid_ids):
            print("2. View details of a listing")
        choice = input("Enter a choice: ")
        if choice == "2" and valid_ids:
            listing_options(sin, valid_ids)
        elif choice == "1":
            notifications.set_notification("Search completed.")
            return
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


@error_notif()
def browse_listings(sin):
    utils.clear_screen()
    get_listings = ("SELECT DISTINCT lid, streetnum, streetname, city, country, zipcode, btype, name"
                    " FROM Availability NATURAL JOIN Listing NATURAL JOIN User WHERE date > %s")
    curr_date = date.today()
    while (True):
        print("Browse and Book Listings")
        get_listings = ("SELECT DISTINCT lid, streetnum, streetname, city, country, zipcode, btype, name"
                    " FROM Availability NATURAL JOIN Listing NATURAL JOIN User WHERE date > %s")
        answers = [curr_date]
        valid_ids = display_listings(get_listings, answers)
        print("Please select an option: ")
        print("1. Return to dashboard")
        if (valid_ids):
            print("2. View details of a listing")
            print("3. Search by longitude/latitude")
            print("4. Search listings with similar zipcodes")
            print("5. Search for listing by address")
        choice = input("Enter a choice: ")

        if choice == "2" and valid_ids:
            listing_options(sin, valid_ids)
        elif choice == "3" and valid_ids:
            search_by_location(sin, answers)
        elif choice == "4" and valid_ids:
            search_by_zipcode(sin, get_listings, answers)
        elif choice == "5" and valid_ids:
            search_by_addr(sin, get_listings, answers)
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
        for row in cursor.fetchall():
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
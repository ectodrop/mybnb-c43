import database as db
import notifications
import utils
from decorators import error_notif
from views import View
from datetime import date

@error_notif()
def create_booking(sin):
    pass


@error_notif()
def browse_listings(sin):
    pass


@error_notif()
def display_bookings(sin, is_past):
    curr_date = date.today()
    get_bookings = ("SELECT bid, start_date, end_date, name, streetnum, streetname, city, country, zipcode, btype"
                    " from Booking NATURAL JOIN (SELECT lid, sin AS lsin, name, streetnum, streetname,"
                    " city, country, zipcode, btype from (Listing NATURAL JOIN (SELECT sin, name FROM User)"
                    " AS S)) AS R WHERE sin = %s AND status = 'ACTIVE' AND start_date")
    if (is_past):
        get_bookings += " < %s"
        timing = "PAST"
    else:
        get_bookings += " >= %s"
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
        if choice == "2":
            cancel_booking(valid_ids)
        elif choice == "1":
            return
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


def cancel_booking(valid_ids):
    questions = [
        "Enter a booking id: "
    ]
    [bid] = utils.display_form(questions)

    if (int(bid) not in valid_ids):
        notifications.set_notification("Invalid booking ID. Please try again.")
        return
    else:
        cancel_booking = ("UPDATE Booking SET status = 'RENTER_CANCELLED' WHERE bid = %s")
        cursor = db.get_new_cursor()
        cursor.execute(cancel_booking, (int(bid),))
        db.get_connection().commit()
        notifications.set_notification("Booking cancelled successfully.")


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
        if choice == "2":
            post_review(valid_ids)
        elif choice == "1":
            return
        else:
            notifications.set_notification("Invalid entry.")
        utils.clear_screen()
        notifications.display_notification()


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

        print_existing_reviews(result)
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
def print_existing_reviews(result):
    statements = ["Rating for host: ", "Comment for host: ", "Rating for listing: ", "Comment for listing: "]
    print("Your Existing Reviews: ")
    for i in range(0, 4):
        print(statements[i], result[i] if result[i] else '-')


@error_notif()
def confirm_responses(responses, bid, existing_review):
    params = []
    print("Replace new rating with previous rating?")
    choice = input("Input (y/n): ")
    if (choice == "y"):
        params += responses[0]
    elif (choice == "n"):
        params += existing_review[0]
    else:
        notifications.set_notification("Invalid entry.")
        return

    print("Replace new comment with previous comment?")
    choice = input("Input (y/n): ")
    if (choice == "y"):
        params += responses[1]
    elif (choice == "n"):
        params += existing_review[1]
    else:
        notifications.set_notification("Invalid entry.")
        return

    params += int(bid)
    return tuple(params)

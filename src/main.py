import user
import listing
import booking
import reports
import notifications
import utils
from views import View

def welcome():
  print("Please select an option")
  print("1. Create an account")
  print("2. Login")
  print("3. Exit")

  choice = input("Enter a choice: ")
  sin = 0
  if choice == "1":
    sin = user.create_account()
  elif choice == "2":
    sin = user.login()
  elif choice == "3":
    return 0, View.EXIT
  else:
    notifications.set_notification("Invalid entry.")

  if (sin == 0):
    return 0, View.WELCOME
  return sin, View.CLIENT_DASH


def client_dashboard(sin):
  print("RENTER VIEW")
  print("What would you like to do?")
  if sin == "1":
    print("0. View reports")
  print("1. Book a listing")
  print("2. View my future bookings")
  print("3. View my bookings history")
  print("4. Switch to host dashboard")
  print("5. Logout")
  print("10. Delete my account")
  choice = input("Enter a choice: ")

  if choice == "0" and sin == "1":
    return View.REPORTS
  
  if choice == "1":
    booking.browse_listings(sin)
  elif choice == "2":
    booking.future_bookings(sin)
  elif choice == "3":
    booking.past_bookings(sin)
  elif choice == "4":
    return View.HOST_DASH
  elif choice == "5":
    return View.WELCOME
  elif choice == "10":
    user.delete_account(sin)
    return View.WELCOME
  else:
    notifications.set_notification("Invalid entry.")
  
  return View.CLIENT_DASH


def host_dashboard(sin):
  print("HOST VIEW")
  print("What would you like to do?")
  print("1. Create a listing")
  print("2. Manage a listing")
  print("3. Display my listings")
  print("4. Switch to client dashboard")
  print("5. Logout")
  print("10. Delete my account")
  choice = input("Enter a choice: ")

  if choice == "1":
    listing.create_listing(sin)
    return View.HOST_DASH
  elif choice == "2":
    return View.SELECT_LISTING
  elif choice == "3":
    listing.display_listings(sin)
    input("Press 'Enter' to continue")
    return View.HOST_DASH
  elif choice == "4":
    return View.CLIENT_DASH
  elif choice == "5":
    return View.WELCOME
  elif choice == "10":
    user.delete_account(sin)
    return View.WELCOME
  else:
    notifications.set_notification("Invalid entry.")
    return View.HOST_DASH

def manage_listing(lid):
  print("Options for listing#" + lid)
  print("1. Add availablity")
  print("2. Adjust pricing")
  print("3. Remove availability")
  print("4. Manage past bookings")
  print("5. Manage current bookings")
  print("6. Remove listing")
  print("7. Add Amenity")
  print("8. Remove Amenity")
  print("9. Return to host menu")
  choice = input("Enter a choice: ")

  if choice == "1":
    listing.update_availablity(lid, remove=False)
  elif choice == "2":
    listing.update_price(lid)
  elif choice == "3":
    listing.update_availablity(lid, remove=True)
  elif choice == "4":
    return View.LISTING_PAST_BOOKINGS
  elif choice == "5":
    return View.LISTING_CURRENT_BOOKINGS
  elif choice == "6":
    return listing.remove_listing(lid)
  elif choice == "7":
    listing.add_amenity(lid)
  elif choice == "8":
    listing.remove_amenity(lid)
  elif choice == "9":
    return View.HOST_DASH
  else:
    notifications.set_notification("Invalid entry")
  return View.LISTING

def host_manage_past_bookings(lid):
  print(f"PAST BOOKINGS FOR LISTING#{lid}")
  valid_ids = listing.display_bookings(lid, past=True)
  print("\n1. Return to listing options")
  print("2. Display cancelled bookings")
  if valid_ids:
    print("3. Add/Edit a review for a past renter")
  choice = input("Enter a choice: ")

  if choice == "1":
    return View.LISTING
  elif choice == "2":
    listing.display_cancelled_bookings(lid)
  elif valid_ids:
    if choice == "3":
      listing.host_review_renter(valid_ids)
  return View.LISTING_PAST_BOOKINGS

def host_manage_current_bookings(lid):
  print(f"CURRENT BOOKINGS FOR LISTING#{lid}")
  valid_ids = listing.display_bookings(lid, past=False)  
  print("\n1. Return to listing options")
  if valid_ids:
    print("2. Cancel a Booking")
  choice = input("Enter a choice: ")
  
  if choice == "1":
    return View.LISTING
  elif valid_ids:
    if choice == "2":
      listing.host_cancel_booking(valid_ids)
  return View.LISTING_CURRENT_BOOKINGS

def display_reports():
  print("REPORTS")
  print("1. Amount of bookings by city")
  print("2. Amount of listings")
  print("3. Rank Hosts by number of listings")
  print("4. Retrieve Commercial hosts")
  print("5. Rank renters by number of bookings")
  print("6. Rank renters by number of cancellations")
  print("7. Rank hosts by number of cancellations")
  print("8. Generate word cloud for listing")
  print("9. Return to client dashboard")
  choice = input("Enter a choice: ")
  
  if choice == "1":
    reports.bookings_by_city()
  elif choice == "2":
    return View.REPORTS_LISTING
  elif choice == "3":
    reports.rank_host_by_listing()
  elif choice == "4":
    reports.get_commercial_hosts()
  elif choice == "5":
    reports.rank_renter_by_bookings()
  elif choice == "6":
    reports.rank_renter_by_cancel()
  elif choice == "7":
    reports.rank_host_by_cancel()
  elif choice == "8":
    reports.get_popular_listing_nouns()
  elif choice == "9":
    return View.CLIENT_DASH
  return View.REPORTS

def display_reports_listing():
  print("LISTING REPORTS")
  print("1. Count by country")
  print("2. Count by country and city")
  print("3. Count by country, city and zipcode")
  print("4. Return to reports")
  choice = input("Enter a choice: ")
  if choice == "1":
    reports.listings_per_country()
  elif choice == "2":
    reports.listings_per_country_city()
  elif choice == "3":
    reports.listings_per_country_city_zip()
  elif choice == "4":
    return View.REPORTS

  return View.REPORTS_LISTING
  

def main ():
  cur_view = View.WELCOME
  utils.clear_screen()
  notifications.set_notification("Welcome To MyBnB!")
  while True:
    utils.clear_screen()
    notifications.display_notification()
    if cur_view == View.WELCOME:
      sin, cur_view = welcome()

    elif cur_view == View.CLIENT_DASH:
      cur_view = client_dashboard(sin)
    
    elif cur_view == View.HOST_DASH:
      cur_view = host_dashboard(sin)
    
    elif cur_view == View.SELECT_LISTING:
      lid = listing.select_listing(sin)
      if lid == 0:
        cur_view = View.HOST_DASH
      else:
        cur_view = View.LISTING
    
    elif cur_view == View.LISTING:
      cur_view = manage_listing(lid)
    
    elif cur_view == View.LISTING_PAST_BOOKINGS:
      cur_view = host_manage_past_bookings(lid)
    
    elif cur_view == View.LISTING_CURRENT_BOOKINGS:
      cur_view = host_manage_current_bookings(lid)
    
    elif cur_view == View.REPORTS:
      cur_view = display_reports()
    
    elif cur_view == View.REPORTS_LISTING:
      cur_view = display_reports_listing()
    elif cur_view == View.EXIT:
      break
    
    elif cur_view == None:
      break
  print("Goodbye")

if __name__ == "__main__":
  main()
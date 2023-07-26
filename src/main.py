import user
import listing
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
  print("1. Book a listing")
  print("2. Search listings")
  print("3. Switch to host dashboard")
  print("4. Logout")
  print("10. Delete my account")
  choice = input("Enter a choice: ")

  if choice == "1":
    pass
  elif choice == "3":
    return View.HOST_DASH
  elif choice == "4":
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
  print("4. View bookings")
  print("5. Cancel booking")
  print("6. Return to host menu")
  choice = input("Enter a choice: ")

  if choice == "1":
    listing.update_availablity(lid, remove=False)
  elif choice == "2":
    listing.update_price(lid)
  elif choice == "3":
    listing.update_availablity(lid, remove=True)
  elif choice == "4":
    listing.display_bookings(lid)
    input("Press Enter to continue ")
  elif choice == "5":
    listing.host_cancel_booking(lid)
  elif choice == "6":
    return View.HOST_DASH
  else:
    notifications.set_notification("Invalid entry")
  return View.LISTING

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
    
    elif cur_view == View.EXIT:
      break

    elif cur_view == None:
      break
  print("Goodbye")

if __name__ == "__main__":
  main()
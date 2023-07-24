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

  if choice == "1":
    name, sin = user.create_account()
  elif choice == "2":
    name, sin = user.login()
  elif choice == "3":
    return 0, View.EXIT
  else:
    notifications.set_notification("Invalid entry.")
    return 0, View.WELCOME

  if (sin == 0):
    return 0, View.WELCOME
  notifications.set_notification("Hi, "+ name)
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
    return user.logout(sin)
  elif choice == "10":
    return user.delete_account(sin)
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
    listing
  elif choice == "4":
    return View.CLIENT_DASH
  elif choice == "5":
    return user.logout(sin)
  elif choice == "10":
    return user.delete_account(sin)
  else:
    notifications.set_notification("Invalid entry.")
    return View.HOST_DASH


def main ():
  cur_view = View.WELCOME
  utils.clear_screen()
  print("Welcome to MyBnB")
  while True:
    notifications.display_notification()
    if cur_view == View.WELCOME:
      sin, cur_view = welcome()
    elif cur_view == View.CLIENT_DASH:
      cur_view = client_dashboard(sin)
    elif cur_view == View.HOST_DASH:
      cur_view = host_dashboard(sin)
    elif cur_view == View.EXIT:
      break
    elif cur_view == None:
      break
    utils.clear_screen()


if __name__ == "__main__":
  main()
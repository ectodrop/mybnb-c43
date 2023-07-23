from user import *
import os
from enum import Enum

class View(Enum):
  WELCOME = 1
  CLIENT_DASH = 2
  HOST_DASH = 3
  EXIT = 4


def clear_screen():
  os.system("cls")


def welcome():
  print("Please select an option")
  print("1. Create an account")
  print("2. Login")
  print("3. Exit")

  choice = input("Enter a choice: ")

  sin = 0
  if choice == "1":
    sin = create_account(connection.cursor())
  elif choice == "2":
    sin = login(connection.cursor())
  elif choice == "3":
    return sin, View.EXIT
  else:
    print("Invalid entry.")

  if (sin == 0):
    return 0, View.WELCOME
  return sin, View.CLIENT_DASH


def client_dashboard(sin):
  print("What would you like to do?")
  print("1. Book a listing")
  print("2. Search listings")
  print("3. Switch to host dashboard")
  print("4. Logout")
  print("10. Delete my account")
  choice = input("")

  if choice == "1":
    pass
  elif choice == "3":
    return View.HOST_DASH
  elif choice == "4":
    return View.WELCOME
  elif choice == "10":
    return delete_account(sin)
  else:
    print("Invalid entry.")
    return View.CLIENT_DASH


def host_dashboard(sin):
  print("What would you like to do?")
  print("1. Create a listing")
  print("2. Manage a listing")
  print("3. Display my listings")
  print("4. Switch to client dashboard")
  print("5. Logout")
  print("10. Delete my account")
  choice = input("")

  if choice == "1":
    pass
  elif choice == "4":
    return View.CLIENT_DASH
  elif choice == "5":
    return View.WELCOME
  elif choice == "10":
    return delete_account(sin)
  else:
    print("Invalid entry.")
    return View.HOST_DASH


def main ():
  logged_in = False
  cur_view = View.WELCOME
  clear_screen()
  print("Welcome to MyBnB")
  while True:
    if cur_view == View.WELCOME:
      sin, cur_view = welcome()
    elif cur_view == View.CLIENT_DASH:
      cur_view = client_dashboard(sin)
    elif cur_view == View.HOST_DASH:
      cur_view = host_dashboard(sin)
    elif cur_view == View.EXIT:
      break
    clear_screen()


if __name__ == "__main__":
  main()
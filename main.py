from user import *
import os
from enum import Enum

class View(Enum):
  WELCOME = 1
  CLIENT_DASH = 2
  HOST_DASH = 3

def clear_screen():
  os.system("cls")

def welcome():
  print("Please select an option")
  print("1. Create an account")
  print("2. Login\n")

  choice = input("Enter a choice: ")

  if choice == "1":
    create_account (connection.cursor())
  elif choice == "2":
    login()
  
  return View.WELCOME

def client_dashboard():
  print("1. Book a listing")
  print("2. Search listings")
  print("3. Switch to host dashboard")
  choice = input("")
  if choice == "1":
    pass
  elif choice == "3":
    return View.HOST_DASH
  return View.CLIENT_DASH

def host_dashboard():
  print("1. Create a listing")
  print("2. Manage a listing")
  print("3. Display my listings")
  print("4. Switch to client dashboard")

  choice = input("")
  if choice == "1":
    pass
  elif choice == "4":
    return View.CLIENT_DASH
  
  return View.HOST_DASH

def main ():
  logged_in = False
  cur_view = "LOGIN"
  while True:
    clear_screen()
    if cur_view == View.WELCOME:
      cur_view = welcome()
    elif cur_view == View.CLIENT_DASH:
      cur_view = client_dashboard()
    elif cur_view == View.HOST_DASH:
      cur_view = host_dashboard()

if __name__ == "__main__":
  main()
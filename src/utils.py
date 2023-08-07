import os
import datetime
import sys

def clear_screen():
  sys.stdout.flush()
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")


def get_answer(question, validator):
  return display_form([(question, validator)])[0]

def display_form(questions):
  CURSOR_UP_ONE = '\x1b[1A' 
  CURSOR_DOWN_ONE = '\x1b[1B' 
  ERASE_LINE = '\x1b[2K' 
  answers = []
  for question, validator in questions:
    a = input(question)
    # retry question until get valid answer
    wrong_once = False

    if validator != None:
      while not validator(a):
        print(end=CURSOR_UP_ONE)
        print(end=ERASE_LINE)
        print("\033[91m" + validator.err + "\033[0m")
        print(end=ERASE_LINE)
        a = input(question)
        print(end=CURSOR_UP_ONE)
        wrong_once = True
    if wrong_once:
      print(end=ERASE_LINE)
      print(end=CURSOR_UP_ONE)
      print(end=ERASE_LINE)
      print(question + a)
    
    answers.append(a)
  return answers

def date_to_str(date):
  return date.strftime("%Y-%m-%d")

def str_to_date(s):
  return datetime.datetime.strptime(s, "%Y-%m-%d").date()

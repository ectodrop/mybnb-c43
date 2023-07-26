import os
import datetime


def clear_screen():
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")


def display_form(questions):
  answers = []
  for question in questions:
    answers.append(input(question))
  return answers

def date_to_str(date):
  return date.strftime("%Y-%m-%d")

def str_to_date(s):
  return datetime.datetime.strptime(s, "%Y-%m-%d").date()

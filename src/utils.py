import os

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
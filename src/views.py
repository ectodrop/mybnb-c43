from enum import Enum, auto

class View(Enum):
  WELCOME = auto()
  CLIENT_DASH = auto()
  HOST_DASH = auto()
  SELECT_LISTING = auto()
  LISTING = auto()
  EXIT = auto()
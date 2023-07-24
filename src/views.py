from enum import Enum, auto

class View(Enum):
  WELCOME = auto()
  CLIENT_DASH = auto()
  HOST_DASH = auto()
  LISTING = auto()
  EXIT = auto()
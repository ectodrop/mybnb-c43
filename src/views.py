from enum import Enum, auto

class View(Enum):
  WELCOME = auto()
  CLIENT_DASH = auto()
  HOST_DASH = auto()
  SELECT_LISTING = auto()
  LISTING = auto()
  LISTING_CURRENT_BOOKINGS = auto()
  LISTING_PAST_BOOKINGS = auto()
  REPORTS = auto()
  REPORTS_LISTING = auto()
  EXIT = auto()
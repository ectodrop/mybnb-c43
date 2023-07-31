
import tkinter as tk
from tkinter import Tk, Button, Label
from tkcalendar import Calendar
import datetime
import utils
"""
bookings = [...,(date, booking_id),...]
availabilities = [...,date,...]
"""
def display_calendar(bookings, availabilities, limit=True):
    def highlight_booking(_):
        nonlocal previous
        date = utils.str_to_date(cal.get_date())
        if previous:
            cal.tag_config(date_tags[previous], background="red") 
            previous = None
        
        if date in date_tags:   
            previous = date
            cal.tag_config(date_tags[date], background="blue")
    def set_sdate():
        nonlocal start_date
        start_date = cal.get_date()
        sdate.config(text = cal.get_date())
        ebtn["state"] = tk.NORMAL

    def set_edate():
        nonlocal end_date
        end_date = cal.get_date()
        edate.config(text = cal.get_date())
        confirm["state"] = tk.NORMAL
    
    def exit():
        nonlocal start_date, end_date
        start_date = end_date = None
        root.destroy()
    # Create Object
    root = Tk()
    
    # Set geometry
    # root.geometry("300x300")
    root.title("Select Dates")
    root.protocol("WM_DELETE_WINDOW", exit)
    today = datetime.date.today()
    previous = None
    date_tags = {}

    
    # Add Calendar
    cal = Calendar(root,
                   selectmode="day",
                   tooltipdelay=0,
                   date_pattern="y-mm-dd",
                   showothermonthdays=False)
    if limit:
        cal["mindate"] = today
        cal["maxdate"] = today+datetime.timedelta(days=365*2)
    
    for date, bid in bookings:
        date_tags[date] = bid

    for date, price in availabilities:
        cal.calevent_create(date, f"${price}", [])
        if date not in date_tags:
            cal.calevent_create(date, "Available", "free")
            cal.tag_config("free", background="green")
        else:
            cal.calevent_create(date, f"Booking#{bid}", str(bid))
            cal.tag_config(bid, background="red")

    
    cal.bind("<<CalendarSelected>>", highlight_booking)
    cal.pack(pady = 20)
    start_date = end_date = None

    frame = tk.Frame()
    bottom = tk.Frame()
    frame.pack(expand=True)
    bottom.pack(side=tk.RIGHT, padx=10, expand=True)
    # Add Button and Label
    sbtn = Button(frame, text = "Set start date",
        command = set_sdate)
    ebtn = Button(frame, text = "Set end date", state=tk.DISABLED,
        command = set_edate)
    sbtn.grid(column=0,row=0)
    ebtn.grid(column=2,row=0)
    
    sdate = Label(frame, text = "yyyy-mm-dd")
    edate = Label(frame, text = "yyyy-mm-dd")
    sdate.grid(column=0, row=1)
    edate.grid(column=2, row=1)
    
    cancel = Button(bottom, text="Cancel", command=exit)
    confirm = Button(bottom, text="Select", state=tk.DISABLED, command=root.destroy)

    cancel.grid(row=0, column=0)
    confirm.grid(row=0, column=1)
    # Execute Tkinter
    root.mainloop()
    
    return start_date, end_date

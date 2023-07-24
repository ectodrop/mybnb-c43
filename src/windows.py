
import tkinter as tk
from tkinter import Tk, Button, Label
from tkcalendar import Calendar
import datetime
import utils
"""
bookings = [...,(date, booking_id),...]
availabilities = [...,date,...]
"""
def display_calendar(bookings, availabilities):
    
    def highlight_booking(_):
        nonlocal previous
        if previous:
            cal.tag_config(date_tags[previous], background="red") 
            previous = None
        if cal.get_date() in date_tags:   
            previous = cal.get_date()
            cal.tag_config(date_tags[cal.get_date()], background="blue")
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
    root.geometry("300x300")
    root.title("Add availability")
    root.protocol("WM_DELETE_WINDOW", exit)
    today = datetime.date.today()
    previous = None
    date_tags = {}

    
    # Add Calendar
    cal = Calendar(root,
                   selectmode="day",
                   tooltipdelay=0,
                   date_pattern="y-mm-dd",
                   mindate=today,
                   maxdate=today+datetime.timedelta(days=365*2))
    
    for date, bid in bookings:
        date_tags[date] = bid
        cal.calevent_create(utils.str_to_date(date), f"Booking#{bid}", bid)
        cal.tag_config(bid, background="red")

    for date in availabilities:
        cal.calevent_create(utils.str_to_date(date), "Available", "free")
        cal.tag_config("free", background="green")
        
    cal.bind("<<CalendarSelected>>", highlight_booking)
    cal.pack(pady = 20)
    start_date = end_date = None

    frame = tk.Frame()
    bottom = tk.Frame()
    frame.pack()
    bottom.pack(side=tk.RIGHT, padx=10)
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
    confirm = Button(bottom, text="Add", state=tk.DISABLED,
                     command=root.destroy)

    cancel.grid(row=0, column=0)
    confirm.grid(row=0, column=1)
    # Execute Tkinter
    root.mainloop()

    return start_date, end_date

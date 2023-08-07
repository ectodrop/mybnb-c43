import database as db
import utils
import notifications
import windows
import validators
from decorators import error_notif
import nltk

# number of bookings in a daterange in a city (can drill down by zipcode)
@error_notif()
def bookings_by_city():
    city = utils.get_answer("Input a city: ", validators.is_contained(get_all_cities()))
    zipcode = utils.get_answer("Input a zipcode (leave blank for city only): ", validators.is_zipcode.or_blank)
    start, end = windows.display_calendar([], [], limit=False)
    if not start or not end:
        notifications.set_notification("Date not selected")
        return
    
    report = ("SELECT COUNT(*) FROM Booking JOIN Listing ON Booking.lid = Listing.lid "
              "WHERE start_date >= %s AND end_date <= %s AND city = %s AND status = 'ACTIVE'")
    
    args = (start, end, city)
    if zipcode:
        report += " AND zipcode = %s"
        args += (zipcode,)
    
    cursor = db.get_new_cursor()
    cursor.execute(report, args)
    (count, ) = cursor.fetchone()
    print(f"Number of bookings in {city} {zipcode}\nDate range {start} to {end}...\n{count} booking(s) found")
    input("Press Enter to continue: ")

# number of listings per country
@error_notif()
def listings_per_country():
    report = ("SELECT country, COUNT(*) FROM Listing GROUP BY country")
    
    cursor = db.get_new_cursor()
    cursor.execute(report)
    result = cursor.fetchall()
    print("LISTING COUNTS BY COUNTRY")
    for country, count in result:
        print(f"  {country}: {count}")
    input("Press Enter to continue: ")


# number of listings per country, city
@error_notif()
def listings_per_country_city():
    report = ("SELECT country, city, COUNT(*) FROM Listing GROUP BY country, city ORDER BY country")
    
    cursor = db.get_new_cursor()
    cursor.execute(report)
    result = cursor.fetchall()
    print("LISTING COUNTS BY CITY")
    for country, city, count in result:
        print(f"  {country} {city}: {count}")
    input("Press Enter to continue: ")


# number of listings per country, city, zipcode
@error_notif()
def listings_per_country_city_zip():
    report = ("SELECT country, city, zipcode, COUNT(*) FROM Listing GROUP BY country, city, zipcode ORDER BY country, city")
    
    cursor = db.get_new_cursor()
    cursor.execute(report)
    result = cursor.fetchall()
    print("LISTING COUNTS BY ZIPCODE")
    for country, city, zipcode, count in result:
        print(f"  {country} {city} {zipcode}: {count}")
    input("Press Enter to continue: ")


# order hosts by number of listings in a country (can drill down to city)
@error_notif()
def rank_host_by_listing():
    country = utils.get_answer("Enter a country: ", validators.is_contained(get_all_countries()))
    city = utils.get_answer(
        "Enter a city (leave blank for country only): ",
        validators.is_contained(get_all_cities(country=country)).or_blank
    )

    clause = "country = %s"
    args = (country,)
    if city:
        clause += " AND city = %s"
        args += (city,)
    
    report = (f"SELECT sin, name, COUNT(*) FROM Listing NATURAL JOIN User WHERE {clause} GROUP BY sin ORDER BY COUNT(*) DESC")
    cursor = db.get_new_cursor()

    cursor.execute(report, args)
    result = cursor.fetchall()
    print("LISTINGS COUNTS BY HOST")
    for sin, name, count in result:
        print(f"  {sin} {name}: {count}")
    input("Press Enter to continue: ")

# retrieve the "commericial hosts" that own more than 10% of the listings in an area
@error_notif()
def get_commercial_hosts():
    country = utils.get_answer("Enter a country: ", validators.is_contained(get_all_countries()))
    city = utils.get_answer(
        "Enter a city (leave blank for country only): ",
        validators.is_contained(get_all_cities(country=country)).or_blank
    )

    clause = "country = %s"
    args = (country,)
    if city:
        clause += " AND city = %s"
        args += (city,)

    cursor = db.get_new_cursor()
    cursor.execute(f"SELECT COUNT(*) FROM Listing WHERE {clause}", args)
    total = cursor.fetchone()[0]
    if total == 0:
        notifications.set_notification("No Listings found")
        return

    args += (0.1*total,)
    report = (f"SELECT sin, name, COUNT(*) FROM Listing NATURAL JOIN User WHERE {clause} GROUP BY sin HAVING COUNT(*) > %s ORDER BY COUNT(*) DESC")
    cursor = db.get_new_cursor()
    cursor.execute(report, args)
    result = cursor.fetchall()
    print(f"COMMERCIAL HOSTS in {country} {city}")
    print(f"{'sin':5}{'name':20}{'listings':<15}{'percentage of listings':15}")
    for sin, name, count in result:
        print(f"{sin:<5}{name:20}{count:<15}{(count/total)*100:.2f}%")
    input("Press Enter to continue: ")

# rank renters by number of bookings in a time period
@error_notif()
def rank_renter_by_bookings():
    (start, end) = windows.display_calendar([],[], limit=False)
    if not start or not end:
        notifications.set_notification("No date selected")
        return
    
    report = ("SELECT sin, name, COUNT(*) FROM Booking NATURAL JOIN User WHERE start_date >= %s AND end_date <= %s GROUP BY sin ORDER BY COUNT(*) DESC")
    cursor = db.get_new_cursor()
    cursor.execute(report, (start, end))
    result = cursor.fetchall()
    if not result:
        notifications.set_notification("No bookings found")
        return
    
    print(f"BOOKINGS FROM {start} to {end}")
    for sin, name, count in result:
        print(f"  {sin} {name}: {count}")
    input("Press Enter to continue: ")

# print renters by number of bookings cancelled
@error_notif()
def rank_renter_by_cancel():
    report = ("SELECT sin, name, COUNT(*) FROM Booking NATURAL JOIN User WHERE status='RENTER_CANCELLED' GROUP BY sin ORDER BY COUNT(*)")
    cursor = db.get_new_cursor()
    cursor.execute(report)
    result = cursor.fetchall()
    if not result:
        notifications.set_notification("No renter cancellations found!")
        return
    print("RENTERS: #CANCELLED")
    for sin, name, count in result:
        print(f"  {sin} {name}: {count}")
    input("Press Enter to continue: ")

# print renters by number of bookings cancelled
@error_notif()
def rank_host_by_cancel():
    report = ("SELECT l.sin, COUNT(*) FROM Booking as b INNER JOIN Listing as l ON b.lid = l.lid "
              "WHERE status='HOST_CANCELLED' GROUP BY l.sin ORDER BY COUNT(*)")
    cursor = db.get_new_cursor()
    cursor.execute(report)
    result = cursor.fetchall()
    if not result:
        notifications.set_notification("No host cancellations found!")
        return
    print("HOSTS: #CANCELLED")
    for sin, count in result:
        print(f"  {sin}: {count}")
    input("Press Enter to continue: ")

# generate a list of popular nouns used in each listing's reviews
@error_notif()
def get_popular_listing_nouns():
    # concatonate all the listing reviews together
    report = "SELECT l.lid, GROUP_CONCAT(renter_listing_comment) FROM Booking as b RIGHT JOIN Listing as l ON b.lid = l.lid GROUP BY l.lid"

    cursor = db.get_new_cursor()
    cursor.execute(report)
    result = cursor.fetchall()
    for lid, text in result:
        if text == None:
            continue
        print(f"\033[94mListing#{lid}\033[0m")
        tokenized = nltk.word_tokenize(text)
        # get all the nouns in text
        nouns = [word.lower() for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN')]
        counts = dict()
        for n in nouns:
            counts[n] = counts.get(n, 0) + 1
        # print out all the nouns in 1 line
        print(f"All words: {', '.join(sorted(counts.keys()))}")
        print("  Frequent (>1 occurances): ")
        # only print the nouns (with their count) that have more than 1 occurance
        for count, noun in sorted([(v, k) for k,v in counts.items()], reverse=True):
            if count < 2:
                break
            print(f"    {noun}: {count}")
    input("Press Enter to continue: ")

def get_all_countries():
    countries = "SELECT DISTINCT country FROM Listing"
    cursor = db.get_new_cursor()
    cursor.execute(countries)
    result = cursor.fetchall()
    return [row[0] for row in result]

def get_all_cities(country:str =None):
    if country:
        cities = f"SELECT DISTINCT city FROM Listing WHERE country = '{country}'"
    else:
        cities = f"SELECT DISTINCT city FROM Listing"
    cursor = db.get_new_cursor()
    cursor.execute(cities)
    result = cursor.fetchall()
    return [row[0] for row in result]
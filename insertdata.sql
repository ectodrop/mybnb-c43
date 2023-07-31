INSERT INTO Building (btype, price) VALUES ('Apartment', 50.00);
INSERT INTO Building (btype, price) VALUES ('House', 70.00);
INSERT INTO Building (btype, price) VALUES ('Cabin', 70.00);
INSERT INTO Building (btype, price) VALUES ('Bed & Breakfast', 70.00);
INSERT INTO Building (btype, price) VALUES ('Camper/RV', 70.00);
INSERT INTO Building (btype, price) VALUES ('Boat', 70.00);
INSERT INTO Building (btype, price) VALUES ('Mansion', 100.00);

INSERT INTO Amenity (atype, category, price) VALUES ('Wifi', 'Essential', 10.00);
INSERT INTO Amenity (atype, category, price) VALUES ('TV', 'Essential', 10.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Kitchen', 'Essential', 5.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Washer', 'Essential', 10.00);
INSERT INTO Amenity (atype, category, price) VALUES ('AC', 'Essential', 10.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Free Parking', 'Essential', 15.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Paid Parking', 'Essential', 5.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Dedicated Workspace', 'Essential', 10.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Pool', 'Standout', 20.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Hot Tub', 'Standout', 15.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Patio', 'Standout', 12.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Fire Pit', 'Standout', 15.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Grill', 'Standout', 15.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Outdoor dining', 'Standout', 15.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Pool Table', 'Standout', 12.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Indoor Fireplace', 'Standout', 15.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Piano', 'Standout', 12.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Exercise', 'Standout', 15.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Lake Access', 'Standout', 12.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Beach Access', 'Standout', 12.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Smoke Alarm', 'Safety', 1.00);
INSERT INTO Amenity (atype, category, price) VALUES ('First Aid Kit', 'Safety', 1.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Fire Extinguisher', 'Safety', 1.00);
INSERT INTO Amenity (atype, category, price) VALUES ('Carbon Monoxide Alarm', 'Safety', 1.00);

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (1, 'Admin', '1', '1999-12-01', 'Adminstrator', 'Admin Rd.');


INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (123, 'Test Guy', '123', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (124, 'Test Guy2', '124', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (125, 'Test Guy3.com', '125', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (126, 'Test Guy4', '126', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (127, 'Test Guy5', '127', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (128, 'Test Guy6', '128', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (129, 'Test Guy7', '128', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (130, 'Test Guy8', '128', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (1, 100.0, 100.0, '90', 'Street st.', 'Toronto', 'Canada', '123ABC', 'Apartment', 123);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (2, 101.1423, 99.123, '123', 'ABC rd.', 'Toronto', 'Canada', '123DEF', 'House', 123);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (3, 51.1657, 10.4515, '123', 'Street rd.', 'Berlin', 'Germany', 'ABC123', 'House', 124);
-- Commercial host
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (4, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (5, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (6, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (7, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (8, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (9, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'House', 125);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (10, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'Mansion', 126);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (11, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'Mansion', 126);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (12, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'Mansion', 127);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (13, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'Mansion', 127);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (14, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'ABC123', 'Mansion', 128);


INSERT INTO Booking (sin, bid, lid, status, start_date, end_date)
    VALUES (124, 1, 1, 'ACTIVE', '2023-08-21', '2023-08-25');

INSERT INTO Booking (sin, bid, lid, status, start_date, end_date)
    VALUES (124, 2, 1, 'ACTIVE', '2023-08-21', '2023-08-25');

INSERT INTO Booking (sin, bid, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 3, 3, 'ACTIVE', '2022-08-21', '2022-08-25', 'Pets and pool, a dream combo!');

INSERT INTO Booking (sin, bid, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 4, 3, 'ACTIVE', '2022-07-21', '2022-07-25', 'Pets joy, poolside play, fantastic stay!');

INSERT INTO Booking (sin, bid, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 5, 3, 'ACTIVE', '2022-06-21', '2022-06-25', 'A pool paradise for you and pets');

INSERT INTO Booking (sin, bid, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 5, 12, 'ACTIVE', '2022-06-21', '2022-06-25', 'Awful! I found bugs everywhere!');


INSERT INTO Availability (date, lid, price) VALUES ('2023-07-24', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-25', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-26', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-27', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-28', 1, 10.0);

INSERT INTO Booking (sin, lid, start_date, end_date) VALUES (123, 1, '2023-07-26', '2023-07-27');

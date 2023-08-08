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

-- User 123

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (123, 'Test Guy', '123', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (1, 100.0, 100.0, '90', 'Street st.', 'Toronto', 'Canada', 'A1B2C3', 'Apartment', 123);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (2, 101.1423, 99.123, '123', 'ABC rd.', 'Toronto', 'Canada', 'A1B2C3', 'House', 123);

-- User 124

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (124, 'Test Guy2', '124', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (3, 51.1657, 10.4515, '123', 'Street rd.', 'Berlin', 'Germany', 'D1E2F3', 'House', 124);

INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-21', 3, 90.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-22', 3, 100.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-23', 3, 100.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-24', 3, 110.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-25', 3, 110.0, false);


-- Commercial host

-- User 125

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (125, 'Test Guy3.com', '125', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (4, 49.2827, 123.1207, '123', 'Street rd.', 'Vancouver', 'Canada', 'A1B3G2', 'House', 125);

INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-21', 4, 12.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-22', 4, 10.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-23', 4, 10.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-24', 4, 10.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-25', 4, 8.0, false);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (5, 49.2827, 123.1207, '123', 'Street1 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (6, 49.2827, 123.1207, '123', 'Street2 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (7, 49.2827, 123.1207, '123', 'Street3 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (8, 49.2827, 123.1207, '123', 'Street4 rd.', 'Vancouver', 'Canada', 'A1B3G2', 'House', 125);
INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (9, 49.2827, 123.1207, '123', 'Street5 rd.', 'Vancouver', 'Canada', 'A1B2G2', 'House', 125);

INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-21', 9, 14.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-22', 9, 100.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-23', 9, 22.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-24', 9, 133.0, false);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-09-25', 9, 144.0, false);

-- User 127

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (126, 'Test Guy4', '126', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (10, 49.2827, 123.1207, '123', 'Street6 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'Mansion', 126);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (11, 49.2827, 123.1207, '123', 'Street7 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'Mansion', 126);

-- User 127

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (127, 'Test Guy5', '127', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (12, 49.2827, 123.1207, '123', 'Street8 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'Mansion', 127);

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (13, 49.2827, 123.1207, '123', 'Street9 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'Mansion', 127);

-- User 128

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (128, 'Test Guy6', '128', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Listing (lid, longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (14, 49.2827, 123.1207, '123', 'Street10 rd.', 'Vancouver', 'Canada', 'A1C3G2', 'Mansion', 128);


INSERT INTO Booking (sin, lid, status, start_date, end_date)
    VALUES (124, 1, 'ACTIVE', '2023-08-21', '2023-08-25');

UPDATE User SET creditcard = '1234567890123456' WHERE sin = 124;

INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-21', 1, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-22', 1, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-23', 1, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-24', 1, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-25', 1, 10.0, true);

INSERT INTO Booking (sin, lid, status, start_date, end_date)
    VALUES (124, 3, 'ACTIVE', '2023-08-21', '2023-08-25');

INSERT INTO Booking (sin, lid, status, start_date, end_date)
    VALUES (125, 3, 'RENTER_CANCELLED', '2023-08-24', '2023-08-25');

INSERT INTO Booking (sin, lid, status, start_date, end_date)
    VALUES (125, 3, 'HOST_CANCELLED', '2023-08-25', '2023-08-25');

UPDATE User SET creditcard = '1234567890123457' WHERE sin = 125;


INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-21', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-22', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-25', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-24', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-08-23', 3, 10.0, true);

INSERT INTO Booking (sin, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 3, 'ACTIVE', '2023-07-21', '2023-07-25', 'Pets and pool, a dream combo!');

INSERT INTO Booking (sin, lid, status, start_date, end_date)
    VALUES (124, 3, 'HOST_CANCELLED', '2023-07-22', '2023-07-25');

INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-07-21', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-07-22', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-07-25', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-07-24', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2023-07-23', 3, 10.0, true);

INSERT INTO Booking (sin, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 3, 'ACTIVE', '2022-07-21', '2022-07-25', 'Pets joy, poolside play, fantastic stay!');

INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-07-21', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-07-22', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-07-25', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-07-24', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-07-23', 3, 10.0, true);

INSERT INTO Booking (sin, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 3, 'ACTIVE', '2022-06-21', '2022-06-25', 'A pool paradise for you and pets');

INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-21', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-22', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-25', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-24', 3, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-23', 3, 10.0, true);

INSERT INTO Booking (sin, lid, status, start_date, end_date, renter_listing_comment)
    VALUES (124, 12, 'ACTIVE', '2022-06-21', '2022-06-25', 'Awful! I found bugs everywhere!');

INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-21', 12, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-22', 12, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-25', 12, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-24', 12, 10.0, true);
INSERT INTO Availability (date, lid, price, booked) VALUES ('2022-06-23', 12, 10.0, true);


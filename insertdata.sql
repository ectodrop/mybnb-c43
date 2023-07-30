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
    (123, 'Test Guy', '123', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO User (sin, name, password, birthday, occupation, address) VALUES
    (124, 'Test Guy2', '124', '1999-12-01', 'Robot', '123 Sesame Ave.');

INSERT INTO Booking (sin, bid, lid, status, start_date, end_date)
    VALUES (124, 1, 1, 'ACTIVE', '2023-08-21', '2023-08-25');

INSERT INTO Booking (sin, bid, lid, status, start_date, end_date)
    VALUES (124, 2, 1, 'ACTIVE', '2023-08-21', '2023-08-25');

INSERT INTO Listing (longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (100.0, 100.0, '90', 'Street st.', 'Toronto', 'Canada', '123ABC', 'Apartment', 123);
INSERT INTO Listing (longitude, latitude, streetnum, streetname, city, country, zipcode, btype, sin)
    VALUES (101.1423432, 99.123123, '123', 'ABC rd.', 'Toronto', 'Canada', '456DEF', 'House', 123);

INSERT INTO Availability (date, lid, price) VALUES ('2023-07-24', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-25', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-26', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-27', 1, 10.0);
INSERT INTO Availability (date, lid, price) VALUES ('2023-07-28', 1, 10.0);

INSERT INTO Booking (sin, lid, start_date, end_date) VALUES (123, 1, '2023-07-26', '2023-07-27');

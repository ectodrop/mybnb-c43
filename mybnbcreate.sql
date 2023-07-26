DROP TABLE IF EXISTS ListingAmenities, Availability, Listing, Booking, User, Building, Amenity;

create table User(
	sin int primary key,
	name varchar(15) not null,
    password varchar(25) not null,
	birthday date not null,
	occupation varchar(15),
	creditcard varchar(25),
	address varchar(25) not null
);

create table Building(
	btype varchar(15) primary key,
    price float(2) not null
);

create table Listing(
	lid int AUTO_INCREMENT primary key,
    longitude float(5) not null,
    latitude float(5) not null,
    streetnum varchar(10) not null,
    streetname varchar(50) not null,
    city varchar(50) not null,
    country varchar(50) not null,
    zipcode varchar(6) not null,
    btype varchar(15) not null,
    sin int not null,
    FOREIGN KEY (btype) REFERENCES Building(btype) ON DELETE CASCADE,
    FOREIGN KEY (sin) REFERENCES User(sin) ON DELETE CASCADE
);

create table Amenity(
	atype varchar(50) primary key,
	category varchar(15) not null,
    price float(2) not null
);

create table ListingAmenities(
	atype varchar(50),
    lid int not null,
    PRIMARY KEY (atype, lid),
    FOREIGN KEY (lid) REFERENCES Listing(lid) ON DELETE CASCADE
);

create table Availability(
	date date not null,
	lid int not null,
    price float(2) not null,
    PRIMARY KEY (date, lid),
    FOREIGN KEY (lid) REFERENCES Listing(lid) ON DELETE CASCADE
);

create table Booking(
	bid int AUTO_INCREMENT primary key,
	sin int not null,
	lid int not null,
    status ENUM('ACTIVE', 'HOST_CANCELLED', 'RENTER_CANCELLED') not null DEFAULT 'ACTIVE',
    start_date date not null,
    end_date date not null,
    renter_host_rating int CHECK (renter_host_rating >= 1 AND renter_host_rating <= 5),
    renter_host_comment text,
    renter_listing_rating int CHECK (renter_listing_rating >= 1 AND renter_listing_rating <= 5),
    renter_listing_comment text,
    host_comment text,
    host_rating int CHECK (host_rating >= 0 AND host_rating <= 5),
    FOREIGN KEY (sin) REFERENCES User(sin) ON DELETE CASCADE,
    FOREIGN KEY (lid) REFERENCES Listing(lid) ON DELETE CASCADE
);

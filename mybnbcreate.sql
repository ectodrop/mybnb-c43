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
    type varchar(15)
        references Building(type),
    sin varchar(15)
        references User(sin)
);

create table Amenity(
	atype varchar(15) primary key,
	category varchar(15) not null,
    price float(2) not null
);

create table ListingAmenities(
	atype varchar(15)
        references Amenity(atype),
    lid int not null
        references Listing(lid),
    primary key (atype, lid)
);

create table Availability(
	aid int AUTO_INCREMENT primary key,
	date date not null,
    price float(2) not null,
	lid int references Listing(lid)
);

create table Booking(
	bid int AUTO_INCREMENT primary key,
	sin varchar(15)
        references User(sin),
    status ENUM('ACTIVE', 'HOST_CANCELLED', 'RENTER_CANCELLED') not null,
    start_date int
        references Availability(aid),
    end_date int
        references Availability(aid),
    renter_comment text,
    renter_rating int CHECK (renter_rating >= 0 AND renter_rating <= 5),
    host_comment text,
    host_rating int CHECK (host_rating >= 0 AND host_rating <= 5)
);



__author__ = 'tarunkumar'

-- To create the database:
--   CREATE DATABASE seerpod;
--   GRANT ALL PRIVILEGES ON seerpod.* TO 'seerpod'@'localhost' IDENTIFIED BY 'seerpod';
--
-- To reload the tables:
--   mysql --user=seerpod --password=Datadr1ven --database=seerpod < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";


-- Count for business
DROP TABLE IF EXISTS business_contact;
CREATE TABLE business_contact (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    owner_email_id VARCHAR(250) NOT NULL,
    password VARCHAR(150) NOT NULL,
    phone VARCHAR(50),
    first_name  VARCHAR(150) NOT NULL,
    last_name VARCHAR(150)
);


-- I am starting with this, it may require more field for discounts
-- not needed for now
DROP TABLE IF EXISTS business_business;
CREATE TABLE business_business (
   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   type INT NOT NULL,
   owner_email_id VARCHAR(250) NOT NULL,
   name VARCHAR(250) NOT NULL,
   image_path VARCHAR(300),
   lat FLOAT (10, 8) NOT NULL,
   lng FLOAT (10, 8) NOT NULL,
   street_name VARCHAR(250) NOT NULL,
   street_number VARCHAR(250) NOT NULL,
   zipcode  INT NOT NULL,
   city VARCHAR(250) NOT NULL,
   state VARCHAR(50) NOT NULL,
   cuisine VARCHAR(250),
   description VARCHAR(500),
   rating FLOAT (2, 2),
   capacity INT,
   phone VARCHAR(50) NOT NULL,
   latest_review VARCHAR(500),
   operation_time  VARCHAR(250),
   website VARCHAR(250),
   expensive_rating FLOAT(2, 2),
   created_on TIMESTAMP NOT NULL
   open_days VARCHAR(50) NOT NULL,
);



-- business contact information
DROP TABLE IF EXISTS business_counter;
CREATE TABLE business_counter (
    biz_id INT NOT NULL,
    time_stamp TIMESTAMP NOT NULL,
    count INT NOT NULL,
    FOREIGN KEY (biz_id) REFERENCES business_business(id) ON DELETE RESTRICT
);


-- Feedback from users
DROP TABLE IF EXISTS user_feedback;
CREATE TABLE user_feedback (
    biz_id INT NOT NULL,
    user_id VARCHAR(150),
    rating DECIMAL(2, 2),
    created_on TIMESTAMP NOT NULL
);


-- Tracking from users
DROP TABLE IF EXISTS tracking_user_logs;
CREATE TABLE tracking_user_logs (
    biz_id INT NOT NULL,
    search_id VARCHAR(150),
    user_id VARCHAR(150) NOT NULL,
    rating DECIMAL(2, 2),
    distance_from_user DECIMAL(10, 3) NOT NULL,
    lat FLOAT (10, 8) NOT NULL,
    lng FLOAT (10, 8) NOT NULL,
    page_number  INT NOT NULL,
    result_position INT NOT NULL,
    time_left_to_close INT,
    created_on TIMESTAMP NOT NULL,
    FOREIGN KEY (biz_id) REFERENCES business_business(id)
);


-- Tracking from clicks
DROP TABLE IF EXISTS tracking_user_clicks;
CREATE TABLE tracking_user_clicks(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    biz_id INT NOT NULL,
    search_id VARCHAR(150),
    user_id VARCHAR(150) NOT NULL,
    created_on TIMESTAMP NOT NULL,
    FOREIGN KEY (biz_id) REFERENCES business_business(id)
);


--Bootstrap for business_contact

INSERT INTO business_contact VALUES (1, 'tar.iiita@gmail.com', 'password', '412-980-7189', 'Tarun', 'Kumar');


-- Bootstrap for business data

INSERT INTO business_business VALUES (1, 1, 'tar.iiita@gmail.com', 'Chaat Cafe', 'indian-chaat-cafe.jpg', 37.782978, -122.397995, '3rd St', '320', 94133, 'San Francisco', 'CA', 'Indian', '', 4, 300, '412-980-7189', '', '8AM: 12AM', '', 3, '2015-11-04 15:00:10', '012456');
INSERT INTO business_business VALUES (2, 1, 'tar.iiita@gmail.com', 'Curry Up Now', 'curry-up-truck.jpg', 37.762350, -122.421515, 'Valencia St', '659', 94110, 'San Francisco', 'CA', 'Indian', '', 3, 160, '412-980-7189', '', '8AM: 2AM', '', 2, '2015-11-04 15:00:10', '01236');
INSERT INTO business_business VALUES (3, 1, 'tar.iiita@gmail.com', 'Basil Thai Restaurant and Bar', 'basil.jpg', 37.775403, -122.409289, 'Folsom St', '1175', 94103, 'San Francisco', 'CA', 'Indian', '', 5, 80, '412-980-7189', '', '4PM: 9PM', '', 5, '2015-11-04 15:00:10', '03456');
--Indian restaurants
INSERT INTO business_business VALUES (4, 1, 'himanshu.gahlot86@gmail.com', 'Little Delhi', 'little-delhi.jpg', 37.775403, -122.409289, 'Eddy St', '83', 94102, 'San Francisco', 'CA', 'Indian', '', 5, 100, '(415) 398-3173', '', '8AM: 9PM', '', 5, '2015-11-04 15:00:10', '0123456');
INSERT INTO business_business VALUES (5, 1, 'himanshu.gahlot86@gmail.com', 'Shalimar Restaurant', 'shalimar-restaurant.jpg', 37.775403, -122.409289, 'Jones St', '532', 94102, 'San Francisco', 'CA', 'Indian', '', 1, 110, '(415) 928-0333', '', '8AM: 9PM', '', 3, '2015-11-04 15:00:10', '01234');
INSERT INTO business_business VALUES (6, 1, 'himanshu.gahlot86@gmail.com', 'Mela Tandoori Kitchen', 'mela-tandoori.jpg', 37.775403, -122.409289, 'Golden Gate Ave', '536', 94102, 'San Francisco', 'CA', 'Indian', '', 3, 120, '(415) 447-4041', '', '8AM: 1AM', '', 2, '2015-11-04 15:00:10', '23456');
INSERT INTO business_business VALUES (7, 1, 'himanshu.gahlot86@gmail.com', 'Chutney', 'chutney.jpg', 37.775403, -122.409289, 'Jones St', '511', 94102, 'San Francisco', 'CA', 'Indian', '', 5, 130, '(415) 931-5541', '', '8AM: 9PM', '', 4, '2015-11-04 15:00:10', '01234');
INSERT INTO business_business VALUES (8, 1, 'himanshu.gahlot86@gmail.com', 'Amber India', 'amber-india.jpg', 37.775403, -122.409289, 'Yerba Buena Ln', '25', 94102, 'San Francisco', 'CA', 'Indian', '', 4, 140, '(415) 777-0500', '', '8AM: 9PM', '', 1, '2015-11-04 15:00:10', '03456');
INSERT INTO business_business VALUES (9, 1, 'himanshu.gahlot86@gmail.com', 'Lahor Karahi', 'lahore-karahi.jpg', 37.775403, -122.409289, 'OFarrell St', '612', 94102, 'San Francisco', 'CA', 'Indian', '', 2, 150, '(415) 567-8603', '', '8AM: 9PM', '', 1, '2015-11-04 15:00:10', '01234');
INSERT INTO business_business VALUES (10, 1, 'himanshu.gahlot86@gmail.com', 'Red Chilli', 'red-chilli.jpg', 37.775403, -122.409289, 'Jones St', '522', 94102, 'San Francisco', 'CA', 'Indian', '', 1, 160, '(415) 931-3529', '', '8AM: 9PM', '', 2, '2015-11-04 15:00:10', '0123456');
INSERT INTO business_business VALUES (11, 1, 'himanshu.gahlot86@gmail.com', 'Pakwan Restaurant', 'pakwan-restaurant.jpg', 37.775403, -122.409289, '16th St', '3180-82', 94102, 'San Francisco', 'CA', 'Indian', '', 5, 170, '(415) 255-2440', '', '8AM: 3PM', '', 5, '2015-11-04 15:00:10', '3456');
INSERT INTO business_business VALUES (12, 1, 'himanshu.gahlot86@gmail.com', 'Tava India Kitchen', 'tava-india-kitchen.jpg', 37.775403, -122.409289, '2nd St', '163', 94102, 'San Francisco', 'CA', 'Indian', '', 4, 10, '(415) 543-8282', '', '8AM: 4PM', '', 4, '2015-11-04 15:00:10', '012456');
INSERT INTO business_business VALUES (13, 1, 'himanshu.gahlot86@gmail.com', 'The Dosa Brothers', 'dosa-brothers.jpg', 37.775403, -122.409289, 'Market St', '598', 94102, 'San Francisco', 'CA', 'Indian', '', 3, 30, '(415) 378-0984', '', '8AM: 9PM', '', 3, '2015-11-04 15:00:10', '0123456');
INSERT INTO business_business VALUES (14, 1, 'utkarsh.cmu@gmail.com', 'Brenda\'s French Soul Food', 'brendas-french-soul-food.jpg', 37.782895, -122.418962, 'Polk St', '652', 94102, 'San Francisco', 'CA', 'French', '', 4, 60, '(415) 345-8100', '', '8AM: 3PM', '', 2, '2015-12-07 06:45:30', '0123456');

-- Bootstrap for business count
INSERT INTO business_counter VALUES (1, '2015-11-08 15:00:10', 234);
INSERT INTO business_counter VALUES (2, '2015-11-08 15:00:10', 121);
INSERT INTO business_counter VALUES (3, '2015-11-08 15:00:10', 31);
INSERT INTO business_counter VALUES (4, '2015-11-08 15:00:10', 49);
INSERT INTO business_counter VALUES (5, '2015-11-08 15:00:10', 21);
INSERT INTO business_counter VALUES (6, '2015-11-08 15:00:10', 331);
INSERT INTO business_counter VALUES (7, '2015-11-08 15:00:10', 65);
INSERT INTO business_counter VALUES (8, '2015-11-08 15:00:10', 99);
INSERT INTO business_counter VALUES (9, '2015-11-08 15:00:10', 76);
INSERT INTO business_counter VALUES (10, '2015-11-08 15:00:10', 434);
INSERT INTO business_counter VALUES (11, '2015-11-08 15:00:10', 13);
INSERT INTO business_counter VALUES (12, '2015-11-08 15:00:10', 223);
INSERT INTO business_counter VALUES (13, '2015-11-08 15:00:10', 34);
INSERT INTO business_counter VALUES (14, '2015-12-07 07:00:40', 46);


--Bootstrap for business feedback
INSERT INTO user_feedback  VALUES ('some_random_id', 1, 3.5, '2015-11-08 15:00:10');
INSERT INTO user_feedback  VALUES ('some_random_id1', 1, 4, '2015-11-08 15:00:10');
INSERT INTO user_feedback  VALUES ('some_random_id1', 2, 2.5, '2015-11-08 15:00:10');
INSERT INTO user_feedback  VALUES ('some_random_id2', 3, 3, '2015-11-08 15:00:10');
INSERT INTO user_feedback  VALUES ('some_random_id3', 2, 4.5, '2015-11-08 15:00:10');
INSERT INTO user_feedback  VALUES ('some_random_id2', 3, 5, '2015-11-08 15:00:10');
INSERT INTO user_feedback  VALUES ('some_random_id2', 2, 2, '2015-11-08 15:00:10');

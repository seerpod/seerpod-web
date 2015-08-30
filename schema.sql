
-- To create the database:
--   CREATE DATABASE blog;
--   GRANT ALL PRIVILEGES ON seerpod.* TO 'blog'@'localhost' IDENTIFIED BY 'seerpod';
--
-- To reload the tables:
--   mysql --user=seerpod --password=Datadr1ven --database=seerpod < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";


DROP TABLE IF EXISTS restaurant_count;
CREATE TABLE restaurant_count (
    restaurant_id INT NOT NULL,
    time_stamp TIMESTAMP NOT NULL,
    count INT NOT NULL
);



-- I am starting with this, it may require more field for discounts
-- not needed for now
DROP TABLE IF EXISTS restaurants;
CREATE TABLE restaurants (
   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(250) NOT NULL,
   ipath VARCHAR(300),
   lat DECIMAL(10, 8) NOT NULL,
   lng DECIMAL(11, 8) NOT NULL,
   street_address VARCHAR(250) NOT NULL,
   zipcode  INT NOT NULL,
   city VARCHAR(250) NOT NULL,
   state VARCHAR(250) NOT NULL,
   capacity INT
);



-- Bootstrap for dummy data

INSERT INTO restaurants VALUES (1,'Chaat Cafe', 'indian-chaat-cafe.jpg', 37.121, -122.343, '320 3rd St, San Francisco', 94133, 'San Francisco', 'CA', 300);
INSERT INTO restaurants VALUES (2,'Curry Up Now', 'curry-up-truck.jpg', 37.121, -122.343, '659 Valencia St, San Francisco, CA 94110', 94110, 'San Francisco', 'CA', 160);
INSERT INTO restaurants VALUES (3,'BASIL THAI RESTAURANT AND BAR', 'basil.jpg', 37.121, -122.343, '1175 Folsom St, San Francisco, CA 94103', 94103, 'San Francisco', 'CA', 80);
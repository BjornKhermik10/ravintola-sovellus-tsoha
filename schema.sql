BEGIN;

DROP TABLE IF EXISTS Restaurant;
DROP TABLE IF EXISTS Review;


CREATE TABLE Restaurant( id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, description TEXT, opening_hours VARCHAR(50));


INSERT INTO Restaurant (name, description, opening_hours)
VALUES 
('Pizza Palace', 'A cozy place for all your pizza cravings.', 'Mon-Sun: 11am - 10pm'),
('Sushi World', 'Fresh sushi from the best chefs.', 'Mon-Fri: 12pm - 9pm, Sat-Sun: 1pm - 10pm'),
('Burger Haven', 'The best burgers in town!', 'Mon-Fri: 10am - 8pm, Sat: 10am - 11pm');


CREATE TABLE Review( id SERIAL PRIMARY KEY, username VARCHAR(50) NOT NULL, restaurant_id INT NOT NULL, rating INT CHECK (rating >= 1 AND rating <= 5), comment TEXT, FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id) ON DELETE CASCADE);

INSERT INTO Review (username, restaurant_id, rating, comment)
VALUES 
('john_doe', 1, 5, 'Amazing pizza! Best I have ever had.'),
('jane_smith', 2, 4, 'Fresh sushi but a bit overpriced.'),
('mark_taylor', 3, 3, 'Good burgers but nothing special.');

COMMIT;

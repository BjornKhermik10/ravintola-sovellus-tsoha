CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password VARCHAR(1000),
    admin bool DEFAULT FALSE
);

INSERT INTO accounts (username, password, admin)
VALUES 
('john_doe', 'password123', False),
('jane_smith', 'hehehehe', False),
('mark_taylor', 'xdxdxdxd', False);

CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT,
    opening_hours VARCHAR(50)
);

INSERT INTO restaurants (name, description, opening_hours)
VALUES 
('Pizza Palace', 'A cozy place for all your pizza cravings.', 'Mon-Sun: 11am - 10pm'),
('Sushi World', 'Fresh sushi from the best chefs.', 'Mon-Fri: 12pm - 9pm, Sat-Sun: 1pm - 10pm'),
('Burger Haven', 'The best burgers in town!', 'Mon-Fri: 10am - 8pm, Sat: 10am - 11pm'),
('Sushi House', 'Experience authentic sushi and sashimi in a traditional setting.', 'Tue-Sun: 12pm - 10pm'),
('Pizza Express', 'Quick and delicious pizzas delivered to your door.', 'Mon-Sun: 11am - 11pm'),
('Burger King', 'Famous for flame-grilled burgers and crispy fries.', 'Mon-Sun: 10am - 12am'),
('Sushi Stop', 'A casual spot for fresh rolls and bento boxes.', 'Mon-Sun: 11am - 9pm'),
('Italian Bistro', 'Homemade pasta and classic Italian dishes.', 'Wed-Mon: 5pm - 10pm, Closed Tue'),
('Burger Bar', 'Gourmet burgers with a variety of toppings.', 'Mon-Sun: 11am - 10pm'),
('Sushi & More', 'Innovative sushi rolls and a vibrant atmosphere.', 'Mon-Sun: 12pm - 11pm'),
('Pizza Planet', 'Family-friendly pizza joint with all your favorite toppings.', 'Mon-Sun: 11am - 10pm'),
('Taco Town', 'Delicious tacos and Mexican cuisine served fresh daily.', 'Mon-Sun: 11am - 10pm'),
('Vegan Delight', 'Plant-based dishes that even meat lovers will enjoy.', 'Mon-Sun: 10am - 9pm');


CREATE TABLE review (
    review_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    restaurant_id INT REFERENCES restaurants,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT
);


INSERT INTO review (account_id, restaurant_id, rating, comment)
VALUES 
(1, 1, 5, 'Amazing pizza! Best I have ever had at Pizza Palace.'),
(2, 2, 4, 'Fresh sushi at Sushi World, but a bit overpriced.'),
(3, 3, 3, 'Good burgers at Burger Haven, but nothing special.'),
(1, 4, 5, 'Sushi House offers an authentic sushi experience! Highly recommend.'),
(2, 5, 4, 'Pizza Express has delicious pizza with great toppings.'),
(3, 6, 5, 'Burger King has the best flame-grilled burgers in town!'),
(1, 7, 4, 'Loved the innovative rolls at Sushi & More, will definitely return.'),
(2, 8, 3, 'Italian Bistro had good pasta, but the service was slow.'),
(3, 9, 5, 'Gourmet burgers at Burger Bar with a variety of toppings—fantastic!'),
(1, 10, 2, 'Tacos at Taco Town were okay, but I expected more flavor.'),
(2, 11, 5, 'Pizza Planet is family-friendly and has tasty pizza!'),
(3, 12, 4, 'Vegan Delight offers great vegan options, even for non-vegans!'),
(1, 1, 4, 'Pizza Palace is a cozy spot, perfect for families and delicious pizza.'),
(2, 2, 5, 'Sushi World has the freshest fish and great service, loved it!'),
(3, 3, 4, 'Burger Haven is solid, but could use more variety in the menu options.');

CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(255) NOT NULL UNIQUE,
    color_id INT CHECK (color_id BETWEEN 1 AND 5)
);

INSERT INTO groups (group_name, color_id)
VALUES 
('Italian Food', 1),
('Sushi', 2),
('Burgers', 4),
('Vegan', 3);


CREATE TABLE group_restaurants (
    group_id INT,
    restaurant_id INT,
    PRIMARY KEY (group_id, restaurant_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);

INSERT INTO group_restaurants (group_id, restaurant_id)
VALUES 
(1, 1),
(1, 5),
(1, 8),
(2, 2),
(2, 4),
(2, 7),
(3, 3),
(3, 6),
(3, 9), 
(4, 12),
(4, 10);
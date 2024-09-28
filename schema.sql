CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password VARCHAR(1000),
    admin bool DEFAULT FALSE
);


CREATE TABLE web_dev_accounts (
    web_dev_id INT PRIMARY KEY,
    username TEXT UNIQUE,
    FOREIGN KEY (web_dev_id) REFERENCES accounts(account_id)
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
('Burger Haven', 'The best burgers in town!', 'Mon-Fri: 10am - 8pm, Sat: 10am - 11pm');

CREATE TABLE review (
    review_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    restaurant_id INT REFERENCES restaurants,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT
);


INSERT INTO review (account_id, restaurant_id, rating, comment)
VALUES 
(1, 1, 5, 'Amazing pizza! Best I have ever had.'),
(2, 2, 4, 'Fresh sushi but a bit overpriced.'),
(3, 3, 3, 'Good burgers but nothing special.');

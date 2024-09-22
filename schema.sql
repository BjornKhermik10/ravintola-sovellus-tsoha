INSERT INTO Restaurant (name, description, opening_hours)
VALUES 
('Pizza Palace', 'A cozy place for all your pizza cravings.', 'Mon-Sun: 11am - 10pm'),
('Sushi World', 'Fresh sushi from the best chefs.', 'Mon-Fri: 12pm - 9pm, Sat-Sun: 1pm - 10pm'),
('Burger Haven', 'The best burgers in town!', 'Mon-Fri: 10am - 8pm, Sat: 10am - 11pm');


INSERT INTO Review (username, restaurant_id, rating, comment)
VALUES 
('john_doe', 1, 5, 'Amazing pizza! Best I have ever had.'),
('jane_smith', 2, 4, 'Fresh sushi but a bit overpriced.'),
('mark_taylor', 3, 3, 'Good burgers but nothing special.');

/*******************
	  Login
********************/
--Register an Account-- DONE
INSERT INTO users (email_address, first_name, last_name, password) 
VALUES ('PLACEHOLDER@hotmail.com', 'PLACE', 'HOLDER', 'PLCHLDR');
--Get list of locations-- DONE
SELECT name
FROM stations;
--Get User ID on login--
SELECT email_address, balance, is_admin, is_banned
FROM users
WHERE email_address = email_address AND password = password; --should return empty row if password doesn't match, otherwise data all set
/*******************
      Home Page
********************/
--Get User Current Balance (covered above)--
--Top Up Balance-- DONE
UPDATE users
SET balance=balance-200
WHERE email_address = 'PLACEHOLDER@hotmail.com';
--What umbrellas user is currently borrowing-- DONE
SELECT l.start_date,u.colour,u.size,s.name --Can we just use umbrella_id and start_date as a primary key?
FROM loans l, umbrellas u,stations s
WHERE l.borrower = 'PLACEHOLDER@hotmail.com' AND l.umbrella_id = u.id 
AND u.location = s.id AND l.end_date ISNULL;
--Current status of user's umbrellas-- DONE
SELECT u.colour, u.size, s.name
FROM umbrellas u, stations s, loans l
WHERE u.location = s.id AND u.owner = 'PLACEHOLDER@hotmail.com';
--Return Umbrella-- DONE
SELECT l.umbrella_id, l.borrower, u.owner, EXTRACT(DAY from end_date-start_date)+1 as days
FROM loans l, umbrellas u
WHERE id = 1 AND l.umbrella_id = u.id; --collect info

UPDATE umbrellas --set umbrella location
SET location = 1
WHERE id = loans.umbrella_id;

UPDATE loans  --set loan end date--
SET end_date = '2023-01-01 01:23:45'
WHERE id = 1;

UPDATE users --subtract fees
SET balance = balance-days*0.1
WHERE email_address = borrower;

UPDATE users --add credit
SET balance = balance + days*0.07
WHERE email_address = owner;
--Submit Report--
INSERT INTO reports (umbrella_id, reporter, details, date)
VALUES (1,'PLACEHOLDER@hotmail.com', 'umbrella broke', '2023-01-01 01:23:45');
/*******************
  Loan an Umbrella
********************/
--Insert Umbrella Details--
INSERT INTO umbrellas (colour, size, owner, location)
VALUES ('#000000', 1, 'PLACEHOLDER@hotmail.com',1)
/*******************
  Borrow an Umbrella
********************/
--Pick an Umbrella--
SELECT id
FROM umbrellas
WHERE location = 1
AND id NOT IN(
	SELECT umbrella_id
	FROM loans
	WHERE end_date ISNULL);
INSERT INTO loans (umbrella_id, borrower, start_date, end_date)
VALUES (1, 'PLACEHOLDER@hotmail.com','2023-01-01 01:23:45',null); --can we use default null in schema?
/*******************
       Admin
********************/
--Look at Reports--
SELECT * 
FROM reports
WHERE
--Ban Users--
UPDATE users
SET is_banned = TRUE
WHERE email_address = 'PLACEHOLDER@hotmail.com';
--Update Locations and umbrellas--
UPDATE locations
SET name = 'Bukit Merah MRT'
WHERE name = 'Redhill MRT';
UPDATE umbrellas
SET colour = '#123456'
WHERE id = 1;

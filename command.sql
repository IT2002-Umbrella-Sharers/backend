/*******************
	  Login
********************/
--Register an Account--
INSERT INTO users (email_address, first_name, last_name, password) 
VALUES ('PLACEHOLDER@hotmail.com', 'PLACE', 'HOLDER', 'plCHLDR');
--Get list of locations--
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
--Top Up Balance--
UPDATE users
SET balance=balance-200
WHERE email_address = 'PLACEHOLDER@hotmail.com';
--What umbrellas user is currently borrowing--
SELECT l.start_date,u.colour,u.size,s.name
FROM loans l, umbrellas u,stations s
WHERE l.borrower = 'PLACEHOLDER@hotmail.com' AND l.umbrella_id = u.id 
AND u.location = s.id AND l.end_date ISNULL;
--Current status of user's umbrellas--
--Return Umbrella--
--Submit Report--
/*******************
  Loan an Umbrella
********************/
--Select Location--
--Insert Umbrella Details--
/*******************
  Borrow an Umbrella
********************/
--Select a Location--
--Pick an Umbrella--
/*******************
       Admin
********************/
--Look at Reports--
--Ban Users--
--Update Locations and umbrellas--

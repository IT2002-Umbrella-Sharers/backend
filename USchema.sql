/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS users (
	email_address CHAR(64) PRIMARY KEY,
	first_name VARCHAR(32) NOT NULL,
	last_name VARCHAR(32) NOT NULL,
	password VARCHAR(64) NOT NULL,
    balance NUMERIC(100,2) NOT NULL DEFAULT 0,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    is_banned BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS umbrellas (
	id SERIAL PRIMARY KEY,
    colour VARCHAR(7) NOT NULL,
    size INTEGER NOT NULL,
    owner VARCHAR(64) NOT NULL REFERENCES users(email_address)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    location INTEGER NOT NULL REFERENCES stations(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    umbrella_id INTEGER NOT NULL REFERENCES umbrellas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    borrower VARCHAR(64) NOT NULL REFERENCES users(email_address)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    lender VARCHAR(64) NOT NULL REFERENCES users(email_address)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP
    -- CHECK (start_date < end_date)
);

CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    umbrella_id INTEGER NOT NULL REFERENCES umbrellas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    reporter VARCHAR(64) NOT NULL REFERENCES users(email_address)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    details VARCHAR(1024),
    date TIMESTAMP NOT NULL
);

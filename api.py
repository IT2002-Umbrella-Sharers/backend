import json
from flask import Flask, request, Response
import sqlalchemy
from typing import Dict

# a lot of this is assuming you send in info in single variables, I'll work on making general functions for creating statements later

YOUR_POSTGRES_PASSWORD = "1"
connection_string = f"postgresql://postgres:{YOUR_POSTGRES_PASSWORD}@localhost/umbrella"
engine = sqlalchemy.create_engine(
    connection_string
)
db = engine.connect()

def check_result_login(email,password): ##for logging in
    try:
        statement = sqlalchemy.text(f"SELECT * FROM users WHERE email_address = \'{email}\' AND password = \'{password}\';")
        res = db.execute(statement)
        db.commit()
        return (generate_table_return_result(res)) # returns a list containing a single dictionary with user details
    except:
        return "ERROR" #honestly not sure why this is here but just in case - if you obtain from 

def check_result_register(email,password,confirm,first_name,last_name): #need first name last name in frontend btw
    if password != confirm: #check if password is same as confirm? i guess?
        return False
    try:
        statement = sqlalchemy.text(f"INSERT INTO USERS (email_address,first_name,last_name,password) VALUES(\'{email}\',\'{first_name}\',\'{last_name}\',\'{password}\';)")
        db.execute(statement)
        db.commit()
        return True
    except:
        return False #catches if cannot insert into database for whatever reason

def get_locations(): # getting names of current location on login
    try:
        statement = sqlalchemy.text(f"SELECT name FROM stations;")
        res = db.execute(statement)
        db.commit()
        return (generate_table_return_result(res)) # example: [{'name': 'Bedok MRT'}, {'name': 'Tampines MRT'}, {'name': 'City Hall MRT'},...
    except:
        return "ERROR"

def top_up(email,amount):
    try:
        statement = sqlalchemy.text(f"UPDATE users SET balance=balance-{amount} WHERE email_address = \'{email}\';")
        db.execute(statement)
        db.commit()
        return # returns nothing.
    except:
        return "ERROR"

def current_borrows(email):
    try:
        statement = sqlalchemy.text(f"SELECT l.start_date,u.colour,u.size,s.name FROM loans l, umbrellas u,stations s WHERE l.borrower = \'{email}\' AND l.umbrella_id = u.id AND u.location = s.id AND l.end_date ISNULL;")
        res = db.execute(statement)
        db.commit()
        return (generate_table_return_result(res)) #note: Python converts SQL timestamp object into datetime.datetime also this returns the station you borrowed from
    except:
        return "ERROR"

def loaned_umbrellas(email):
    try:
        statement = sqlalchemy.text(f"SELECT u.colour, u.size, s.name FROM umbrellas u, stations s, loans l WHERE u.location = s.id AND u.owner = \'{email}\';")
        res = db.execute(statement)
        db.commit()
        return (generate_table_return_result(res)) #note: Python converts SQL timestamp object into datetime.datetime also this returns the station you borrowed from
    except:
        return "ERROR"
        
def return_umbrella(loan_id,date,return_location): #jesus christ
    try:
        statement = sqlalchemy.text(f"SELECT l.umbrella_id, l.borrower, u.owner, EXTRACT(DAY from end_date-start_date)+1 as days FROM loans l, umbrellas u WHERE l.id = {loan_id} AND l.umbrella_id = u.id;")
        data = db.execute(statement)
        db.commit()
        data = generate_table_return_result(data)
        umbrella_id, borrower_email, owner_email, days = data[0]['umbrella_id'],data[0]['borrower'],data[0]['owner'],data[0]['days']
        statement = sqlalchemy.text(f"UPDATE umbrellas SET location = {return_location} WHERE id = {umbrella_id};\
                                    UPDATE loans SET end_date = \'{date}\' WHERE id = {loan_id};\
                                    UPDATE users SET balance = balance-{int(days)*0.1} WHERE email_address = \'{borrower_email}\';\
                                    UPDATE users SET balance = balance+{int(days)*0.07} WHERE email_address = \'{owner_email}\';")
        data = db.execute(statement)
        db.commit()
        return
    except Exception as e:
        return e

def generate_table_return_result(res): # returns a list containing several dictionaries depending on query size - keys are column names and values are...values
    rows = []
    columns = list(res.keys())
    for row_number, row in enumerate(res):
        rows.append({})
        for column_number, value in enumerate(row):
            rows[row_number][columns[column_number]] = value
    return rows

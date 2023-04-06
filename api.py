import sqlalchemy
# a lot of this is assuming you send in info in single variables, I'll work on making general functions for creating statements later

YOUR_POSTGRES_PASSWORD = "a"
connection_string = f"postgresql://postgres:{YOUR_POSTGRES_PASSWORD}@localhost/umbrella"
engine = sqlalchemy.create_engine(
    connection_string, 
    isolation_level="AUTOCOMMIT"
)
db = engine.connect()

#
# login
#

def check_result_login(email,password): ##for logging in
    try:
        statement = sqlalchemy.text(f"SELECT * FROM users WHERE email_address = \'{email}\' AND password = \'{password}\';")
        res = db.execute(statement)
        res = generate_table_return_result(res)
        if len(res) == 0:
            return False, 400
        return {'user': res[0]}, 200 # returns a list containing a single dictionary with user details
    except Exception as e:
        print(e)
        return False, 400 #honestly not sure why this is here but just in case - if you obtain from 

def check_result_register(email,password,first_name,last_name): #need first name last name in frontend btw
    try:
        statement = sqlalchemy.text(f"INSERT INTO USERS (email_address,first_name,last_name,password) VALUES(\'{email}\',\'{first_name}\',\'{last_name}\',\'{password}\');")
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400 #catches if cannot insert into database for whatever reason

def get_locations(): # getting names of current location on login
    try:
        statement = sqlalchemy.text(f"SELECT name FROM stations;")
        res = db.execute(statement)
        res = generate_table_return_result(res)
        return res, 200 # example: [{'name': 'Bedok MRT'}, {'name': 'Tampines MRT'}, {'name': 'City Hall MRT'},...
    except Exception as e:
        print(e)
        return False, 400
def current_borrows(email):
    try:
        statement = sqlalchemy.text(f"""
            SELECT l.id AS loan_id, u.id AS umbrella_id, uu.first_name, uu.last_name, u.owner,
                s.name AS location_name, l.start_date, u.colour, u.size
            FROM loans l, umbrellas u, stations s, users uu 
            WHERE l.borrower = \'{email}\'
            AND uu.email_address = u.owner
            AND l.umbrella_id = u.id 
            AND u.location = s.id 
            AND l.end_date ISNULL;
        """)
        res = db.execute(statement)
        res = generate_table_return_result(res)
        return res, 200 #note: Python converts SQL timestamp object into datetime.datetime also this returns the station you borrowed from
    except Exception as e:
        print(e)
        return False, 400

def loaned_umbrellas(email):
    try:
        statement = sqlalchemy.text(f"""
            SELECT DISTINCT u.id, u.colour, u.size, s.name AS location, TRUE AS on_loan
            FROM umbrellas u, stations s, loans l
            WHERE u.location = s.id
            AND u.owner = \'{email}\'
            AND u.id = l.umbrella_id
            AND end_date ISNULL
            UNION
            SELECT DISTINCT u.id, u.colour, u.size, s.name AS location, FALSE AS on_loan
            FROM umbrellas u, stations s
            WHERE u.location = s.id
            AND u.owner = \'{email}\'
            AND u.id NOT IN(
	            SELECT u.id
	            FROM loans l, umbrellas u
	            WHERE u.owner = \'{email}\'
	            AND u.id = l.umbrella_id
	            AND end_date ISNULL);
        """)
        res = db.execute(statement)
        res = generate_table_return_result(res)
        return res, 200 #note: Python converts SQL timestamp object into datetime.datetime also this returns the station you borrowed from
    except Exception as e:
        print(e)
        return False, 400
        
def return_umbrella(loan_id,date,location_name): #jesus christ also for this statement to work, date needs to be a string in this format:"YYYY-MM-DD HH:MM:SS", same for the others
    try:
        return_location = get_location_id(location_name)
        statement = sqlalchemy.text(f"""
            UPDATE loans 
            SET end_date = \'{date}\' 
            WHERE id = {loan_id};
        """)
        db.execute(statement)
        statement = sqlalchemy.text(f"""
            SELECT l.umbrella_id, l.borrower, u.owner, EXTRACT(DAY from end_date-start_date)+1 as days 
            FROM loans l, umbrellas u 
            WHERE l.id = {loan_id} 
            AND l.umbrella_id = u.id;
        """)
        data = db.execute(statement)
        data = generate_table_return_result(data)
        umbrella_id, borrower_email, owner_email, days = data[0]['umbrella_id'],data[0]['borrower'],data[0]['owner'],data[0]['days']
        if days is None:
            days = 1
        statement = sqlalchemy.text(f"""
            UPDATE umbrellas 
            SET location = {return_location} 
            WHERE id = {umbrella_id};
            UPDATE users 
            SET balance = balance - {int(days) * 0.1}
            WHERE email_address = \'{borrower_email}\'; 
            UPDATE users 
            SET balance = balance + {int(days) * 0.07}
            WHERE email_address = \'{owner_email}\';
        """)
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400

def make_report(umbrella_id,reporter,details,date):
    try:
        statement = sqlalchemy.text(f"INSERT INTO reports (umbrella_id, reporter, details, date) VALUES ({umbrella_id},\'{reporter}\', \'{details}\', \'{date}\');")
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400  

# 
# loan an umbrella
# 

def get_location_id(location_name):
    try:
        statement = sqlalchemy.text(f"""
            SELECT s.id
            FROM stations s
            WHERE s.name = '{location_name}';
        """)
        res = db.execute(statement).fetchone()
        return res[0]
    except Exception as e:
        print(e)
        return -1

def loan_umbrella(email, colour, size, location_name): #need first name last name in frontend btw
    try:
        location = get_location_id(location_name)
        statement = sqlalchemy.text(f"INSERT INTO umbrellas (colour, size, owner, location) VALUES (\'{colour}\', {size}, \'{email}\',{location});")
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400
    
# 
# borrow an umbrella
# 

def which_umbrella(location_name):
    try:
        location = get_location_id(location_name)
        statement = sqlalchemy.text(f"""
            SELECT u.id, u.colour, u.size, us.first_name || ' ' || us.last_name as name 
            FROM umbrellas u, users us
            WHERE location = {location} 
            AND u.owner = us.email_address
            AND u.id NOT IN (
                SELECT umbrella_id 
                FROM loans 
                WHERE end_date ISNULL 
                AND location = {location});
        """) ## technically, I guess we don't need the second location check...
        res = db.execute(statement)
        res = generate_table_return_result(res)
        return res, 200 #returns umbrellas which aren't on loan from a specific location
    except Exception as e:
        print(e)
        return False, 400 

def borrow_umbrella(umbrella_id,borrower,date):
    try:
        statement = sqlalchemy.text(f"INSERT INTO loans (umbrella_id, borrower, start_date, end_date) VALUES ({umbrella_id}, \'{borrower}\',\'{date}\',null);") 
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400 

# account

def get_balance(id):
    try:
        statement = sqlalchemy.text(f"""
            SELECT u.balance 
            FROM users u
            WHERE u.email_address = '{id}';
        """)
        res = db.execute(statement)
        res = generate_table_return_result(res)
        return res, 200
    except Exception as e:
        print(e)
        return False, 400

def add_balance(id, amount):
    try:
        statement = sqlalchemy.text(f"""
            UPDATE users
            SET balance = balance + {amount}
            WHERE email_address = '{id}';
        """)
        db.execute(statement)
        return True, 200
    except Exception as e:
            print(e)
            return False, 400

# 
# admin
# 

def reports():
    try:
        statement = sqlalchemy.text(f"SELECT * from reports;")
        res = db.execute(statement)
        res = generate_table_return_result(res)
        return res, 200
    except Exception as e:
        print(e)
        return False, 400 

def ban(email):
    try:
        statement = sqlalchemy.text(f"UPDATE users SET is_banned = TRUE WHERE email_address = \'{email}\';") #surprisingly enough boolean isnt caps sensitive...
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400
    
def unban(email):
    try:
        statement = sqlalchemy.text(f"UPDATE users SET is_banned = FALSE WHERE email_address = \'{email}\';")
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400

def update_location(id,name):
    try:
        statement = sqlalchemy.text(f"UPDATE stations SET name=\'{name}\' WHERE id = \'{id}\';")
        db.execute(statement)
        return True, 200
    except Exception as e:
        print(e)
        return False, 400


def generate_table_return_result(res): # returns a list containing several dictionaries depending on query size - keys are column names and values are...values
    rows = []
    columns = list(res.keys())
    for row_number, row in enumerate(res):
        rows.append({})
        for column_number, value in enumerate(row):
            rows[row_number][columns[column_number]] = value
    return rows

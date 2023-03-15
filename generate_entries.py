import pickle
import random
import string
import datetime

def get_name(names):
    return random.choice(names)

def generate_users(n, first_names, last_names, filename):
    def generate_valid_email_address():
        first_name = get_name(first_names)
        last_name = get_name(last_names)
        email = first_name + last_name + random.choice(domain_names)
        while email in emails:
            first_name = get_name(first_names)
            last_name = get_name(last_names)
            email = first_name + last_name + random.choice(domain_names)
        emails.append(email)
        return first_name, last_name, email

    domain_names = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@aol.com", "@msn.com"]
    emails = []
    with open(filename, "w") as f:
        for _ in range(n):
            first_name, last_name, email = generate_valid_email_address()
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            balance = random.random() * 50
            is_admin = "TRUE" if random.randint(0, 100) == 1 else "FALSE"
            is_banned = "TRUE" if random.randint(0, 1000) == 1 else "FALSE"
            f.write(f"INSERT INTO users (email_address, first_name, last_name, password, balance, is_admin, is_banned) VALUES ('{email}', '{first_name}', '{last_name}', '{password}', {balance}, {is_admin}, {is_banned});\n")
    return emails

def generate_stations(filename):
    stations = [
        'Bedok MRT', 'Tampines MRT', 'City Hall MRT', 'Serangoon MRT', 'Sengkang MRT', 'Punggol MRT',
        'Kent Ridge MRT', 'Pioneer MRT', 'Dhoby Ghaut MRT', 'Choa Chu Kang MRT'
    ]
    with open(filename, 'w') as f:
        for station in stations:
            f.write(f"INSERT INTO stations (name) VALUES ('{station}');\n")
    return [i+1 for i in range(len(stations))]

def generate_umbrellas(n, users, locations, filename):
    colours = [
        "#000000", "#C0C0C0", "#808080", "#FFFFFF", "#800000", "#FF0000", "#800080", "#FF00FF",
        "#008000", "#00FF00", "#808000", "#FFFF00", "#000080", "#0000FF", "#008080", "#00FFFF"
    ]
    sizes = [1, 2, 3, 4, 5]
    with open(filename, 'w') as f:
        for _ in range(n):
            colour = random.choice(colours)
            size = random.choice(sizes)
            owner = random.choice(users)
            location = random.choice(locations)
            f.write(f"INSERT INTO umbrellas (colour, size, owner, location) VALUES ('{colour}', {size}, '{owner}', {location});\n")
    
    return [i+1 for i in range(n)]

def generate_loans(n, users, umbrellas, filename):
    start = datetime.datetime(2022, 1, 1)
    end = datetime.datetime(2022, 12, 31)
    with open(filename, 'w') as f:
        for _ in range(n):
            umbrella = random.choice(umbrellas)
            borrower = random.choice(users)
            start_date = random.random() * (end - start) + start
            if random.randint(1, 2) == 1:
                f.write(f"INSERT INTO loans (umbrella_id, borrower, start_date) VALUES ({umbrella}, '{borrower}', '{start_date.strftime('%Y-%m-%d %H:%M:%S')}');\n")
            else:
                end_date = start_date + random.random() * datetime.timedelta(days=7)
                f.write(f"INSERT INTO loans (umbrella_id, borrower, start_date, end_date) VALUES ({umbrella}, '{borrower}', '{start_date.strftime('%Y-%m-%d %H:%M:%S')}', '{end_date.strftime('%Y-%m-%d %H:%M:%S')}');\n")

def generate_reports(n, users, umbrellas, filename):
    start = datetime.datetime(2022, 1, 1)
    end = datetime.datetime(2022, 12, 31)
    faults = ['Handle Broken', 'Hole in Umbrella', 'Spoke Broken', 'Missing', 'Inverted']
    with open(filename, 'w') as f:
        for _ in range(n):
            umbrella = random.choice(umbrellas)
            reporter = random.choice(users)
            fault = random.choice(faults)
            date = random.random() * (end - start) + start
            f.write(f"INSERT INTO reports (umbrella_id, reporter, details, date) VALUES ({umbrella}, '{reporter}', '{fault}', '{date}');\n")

if __name__ == "__main__":
    random.seed(10) # set seed
    with open("first_names", "rb") as fp:
        first_names = pickle.load(fp)
    with open("last_names", "rb") as fp:
        last_names = pickle.load(fp)
    emails = generate_users(50, first_names, last_names, "UUsers.sql")
    station_ids = generate_stations("UStations.sql")
    umbrella_ids = generate_umbrellas(200, emails, station_ids, "UUmbrellas.sql")
    generate_loans(400, emails, umbrella_ids, "ULoans.sql")
    generate_reports(20, emails, umbrella_ids, "UReports.sql")

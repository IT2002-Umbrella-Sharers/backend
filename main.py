from flask import Flask, request
from api import *


app = Flask(__name__, template_folder='html', static_folder='static')

def create_response(data, status):
    return {'data': data}, status

@app.route('/register', methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    res = check_result_register(
        email,
        password,
        firstname,
        lastname
    )
    return create_response(res, 200)

@app.route('/login', methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    res = check_result_login(
        email,
        password
    )
    return create_response(res, 200)

@app.route('/getlocations', methods=["GET"])
def getlocations():
    res = get_locations()
    return create_response(res, 200)

@app.route('/topup', methods=["POST"])
def topup():
    email = request.form['email']
    amount = request.form['amount']
    res = top_up(email, amount)
    return create_response(res, 200)

@app.route('/getborrows', methods=["POST"])
def getborrows():
    email = request.form['email']
    res = current_borrows(email)
    return create_response(res, 200)

@app.route('/getloans', methods=["POST"])
def getloans():
    email = request.form['email']
    res = loaned_umbrellas(email)
    return create_response(res, 200)

@app.route('/returnumbrella', methods=["POST"])
def returnumbrella():
    loanid = request.form['loanid']
    date = request.form['date']
    returnlocation = request.form['returnlocation']
    res = return_umbrella(loanid, date, returnlocation)
    return create_response(res, 200)

@app.route('/makereport', methods=["POST"])
def makereport():
    umbrellaid = request.form['umbrellaid']
    reporter = request.form['reporter']
    details = request.form['details']
    date = request.form['date']
    res = make_report(
        umbrellaid, 
        reporter,
        details,
        date
    )
    return create_response(res, 200)

@app.route('/loanumbrella', methods=["POST"])
def loanumbrella():
    email = request.form['email']
    colour = request.form['colour']
    size = request.form['size']
    location = request.form['location']
    res = loan_umbrella(
        email, 
        colour,
        size,
        location
    )
    return create_response(res, 200)

@app.route('/getumbrella', methods=["POST"])
def getumbrella():
    email = request.form['email']
    colour = request.form['colour']
    size = request.form['size']
    location = request.form['location']
    res = which_umbrella(
        email, 
        colour,
        size,
        location
    )
    return create_response(res, 200)

@app.route('/borrowumbrella', methods=["POST"])
def borrowumbrella():
    umbrellaid = request.form['umbrellaid']
    borrower = request.form['borrower']
    date = request.form['date']
    res = borrow_umbrella(
        umbrellaid, 
        borrower,
        date
    )
    return create_response(res, 200)

@app.route('/getreports', methods=["POST"])
def getreports():
    res = reports()
    return create_response(res, 200)

@app.route('/ban', methods=["POST"])
def ban():
    email = request.form['email']
    res = ban(email)
    return create_response(res, 200)

@app.route('/unban', methods=["POST"])
def unban():
    email = request.form['email']
    res = unban(email)
    return create_response(res, 200)

@app.route('/updatelocation', methods=["POST"])
def updatelocation():
    id = request.form['id']
    name = request.form['name']
    res = update_location(id, name)
    return create_response(res, 200)

@app.route('/<path:path>')
def catch_all(path):
    return f"The path {path} is not found."


if __name__ == '__main__':
    app.run(host="localhost", port=7777, debug=True)

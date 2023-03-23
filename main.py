from flask import Flask, request, Response
from flask_session import Session
from api import *


app = Flask(__name__, template_folder='html', static_folder='static')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

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

@app.route('/borrows', methods=["POST"])
def borrows():
    email = request.form['email']
    res = current_borrows(email)
    return create_response(res, 200)

@app.route('/loans', methods=["POST"])
def loans():
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

@app.route('/<path:path>')
def catch_all(path):
    return f"The path {path} is not found."


if __name__ == '__main__':
    app.run(host="localhost", port=7777, debug=True)

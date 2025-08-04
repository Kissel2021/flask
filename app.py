import sqlite3

from flask import Flask, request, render_template


app = Flask(__name__)


class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


#/user
@app.route('/user', methods=['GET', 'DELETE'])
def user_handler():
    if request.method == 'GET':
        return "Привет, Flask работает!"
    else:
        return 'привет'


#/login
@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        #username = request.form['username']
        password = request.form['password']
        with Database('fin_tracker_bd.db') as cursor:
            result = cursor.execute(f"SELECT * FROM user WHERE email = '{email}' and password = '{password}'")
            data = result.fetchone()
        if data:
            return  f"correct user pair"
        else:
            return f" wrong user pair"


#/register
@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        with Database('fin_tracker_bd.db') as cursor:
            cursor.execute(f"INSERT INTO user(name, surname, password, email) VALUES ('{name}', '{surname}', '{password}', '{email}')")
        return f" account successfully created"


#/cetegory
@app.route('/category', methods=['GET', 'POST'])
def category_list():
    if request.method == 'GET':
        return 'GET'
    else:
        return 'POST'


#/category/<category_id>
@app.route('/category/<category_id>', methods=['GET', 'PATCH', 'DELETE'])
def category_detail(category_id):
    if request.method == 'GET':
        return f" 12, {category_id}"


#/income
@app.route('/income', methods=['GET', 'POST'])
def get_income():
    if request.method == 'GET':
        return 'GET'
    else:
        return 'POST'


#/income/<income_id>
@app.route('/income/<income_id>', methods=['GET', 'PATCH', 'DELETE'])
def income_detail(income_id):
    if request.method == 'GET':
        return f" 22, {income_id}"


#/spend
@app.route('/spend', methods=['GET', 'POST'])
def get_spend():
    if request.method == 'GET':
        return 'GET'
    else:
        return 'POST'


#/spend/<spend_id>
@app.route('/spend/<spend_id>', methods=['GET', 'PATCH', 'DELETE'])
def spend_detail(spend_id):
    return f" 22, {spend_id}"


if __name__ == "__main__":
    app.run(debug=True)
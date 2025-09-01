import sqlite3

from flask import Flask, request, render_template, session, redirect


app = Flask(__name__)
app.secret_key = 'qwefdgyhdtgfjghkghfk34678'
SPEND = 1
INCOME = 2


class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class DBwrapper:
    def insert(self, table, data):
        with Database('fin_tracker_bd.db') as cursor:
            cursor.execute(f"INSERT INTO { table } ({', '.join(data.keys())}) VALUES ({', '.join(['?'] * len(data))})", tuple(data.values()))

    def select(self, table, params=None):
        with Database('fin_tracker_bd.db') as cursor:
            if params:
                result_params = []
                for key, value in params.items():
                    if isinstance(value, list):
                        result_params.append(f"{key} IN ({', '.join(map(str, value))})")
                    else:
                        if isinstance(value, str):
                            result_params.append(f"{key} = '{value}'")
                        else:
                            result_params.append(f"{key} = {value}")
                result_where = ' AND '.join(result_params)
                cursor.execute(f"SELECT * FROM {table} WHERE {result_where}")
            else:
                cursor.execute(f"SELECT * FROM {table}")
            return cursor.fetchall()

    def delete(self, table, where):
        with Database('fin_tracker_bd.db') as cursor:
            conditions = []
            values = []
            for key, value in where.items():
                conditions.append(f"{key} = ?")
                values.append(value)
            sql = f"DELETE FROM {table} WHERE {' AND '.join(conditions)}"
            cursor.execute(sql, tuple(values))

    def update(self, table, data, where):
        with Database('fin_tracker_bd.db') as cursor:
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])

            values = list(data.values()) + list(where.values())

            sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            cursor.execute(sql, tuple(values))

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
        db = DBwrapper()
        data = db.select( 'user', {'email': email, 'password': password})
        '''with Database('fin_tracker_bd.db') as cursor:
            result = cursor.execute(f"SELECT id FROM user WHERE email = '{email}' and password = '{password}'")
            data = result.fetchone()'''
        if data:
            session['user_id'] = data[0]['id']
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
        db = DBwrapper()
        db.insert('user', {'name': name, 'surname': surname, 'password': password, 'email': email})
        '''with Database('fin_tracker_bd.db') as cursor:
            cursor.execute(f"INSERT INTO user(name, surname, password, email) VALUES ('{name}', '{surname}', '{password}', '{email}')") '''
        return f" account successfully created"


#/category
@app.route('/category', methods=['GET', 'POST'])
def category_list():
    if 'user_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            res = db.select('category', {'owner': [session['user_id'], 1]})
            '''data = cursor.execute(
                f"SELECT id, category_name AS name FROM category WHERE owner = {session['user_id']} OR owner = 1"
                #f"SELECT * FROM 'category' WHERE owner = {session['user_id']} OR owner = 1"
            )
            res = data.fetchall()'''
            return render_template("all_categories.html", categories=res)
        else:
            category_name = request.form['category_name']
            category_owner = int(session['user_id'])
            db = DBwrapper()
            db.insert('category', {'category_name': category_name, 'owner': category_owner})
            #cursor.execute(f"INSERT INTO 'category' (category_name, owner) VALUES ('{category_name}', '{owner}')")
            return redirect('/category')


#/category/<category_id>
@app.route('/category/<category_id>', methods=['GET', 'POST'])
def category_detail(category_id):
    if 'user_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            category = db.select("category", {"id": category_id})
            if not category:
                return "Категория не найдена", 404
            return render_template("one_category.html",
                                   category_id=category_id,
                                   category_name=category[0]["category_name"])
        else:

            new_name = request.form['category_name']

            db.update('category',
                      {'category_name': new_name},
                      {'id': category_id, 'owner': session['user_id']})

            return redirect('/category')


#/category/<category_id>/delete
@app.route('/category/<int:category_id>/delete', methods=['GET'])
def delete_category(category_id):
    if 'user_id' in session:
        db = DBwrapper()
        db.delete("category", {"id": category_id, "owner": session["user_id"]})
        return redirect("/category")
    else:
        return redirect("/login")


# /income
@app.route('/income', methods=['GET', 'POST'])
def get_income():
    if 'user_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            res = db.select('"transaction"', {'owner': session['user_id'], 'type': INCOME})
            categories = db.select("category")
            return render_template('dashboard.html',
                                   transactions=res,
                                   categories=categories,
                                   page_type="income")
        else:
            t_description = request.form['description']
            t_category = request.form['category']
            t_amount = float(request.form['amount'])
            t_date = request.form['date']
            owner = session['user_id']
            transaction_type = INCOME

            db.insert("transaction", {
                "description": t_description,
                "category": t_category,
                "date": t_date,
                "owner": owner,
                "type": transaction_type,
                "amount": t_amount
            })
            return redirect('/income')
    else:
        return redirect('/login')


#/income/<income_id>
@app.route('/income/<income_id>', methods=['GET', 'PATCH', 'DELETE'])
def income_detail(income_id):
    if request.method == 'GET':
        return f" 22, {income_id}"


#/spend
@app.route('/spend', methods=['GET', 'POST'])
def get_spend():
    if 'user_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            '''with Database('fin_tracker_bd.db') as cursor:
                data = cursor.execute(
                    f"SELECT * FROM 'transaction' WHERE owner = {session['user_id']} and type = {SPEND}")
                res = data.fetchall()
                categories = cursor.execute("SELECT category_name FROM category").fetchall()'''
            res = db.select('"transaction"', {'owner': session['user_id'], 'type': SPEND})
            categories = db.select("category")
            return render_template('dashboard.html',
                                    transactions=res,
                                    categories=categories,
                                    page_type="spend")
        else:
            #with Database('fin_tracker_bd.db') as cursor:
            t_description = request.form['description']
            t_category = request.form['category']
            t_date = request.form['date']
            t_owner = request.form['user_id']
            t_type = request.form['type']
            t_amount = request.form['amount']
            '''cursor.execute(f"INSERT INTO 'transaction' (description, category, date, owner, type, amount) "
                            f"VALUES ('{t_description}', '{t_category}', '{t_date}', '{t_owner}', '{t_type}', '{t_amount}')")'''

            db.insert('"transaction"', {'description': t_description, 'category': t_category, 'date': t_date, 'owner': t_owner, 'type': t_type, 'amount': t_amount})
        return redirect('/spend')
    else:
        return redirect('/login')


#/spend/<spend_id>
@app.route('/spend/<spend_id>', methods=['GET', 'PATCH', 'DELETE'])
def spend_detail(spend_id):
    return f" 22, {spend_id}"


if __name__ == "__main__":
    app.run(debug=True)
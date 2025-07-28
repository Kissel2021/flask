from flask import Flask, request, render_template


app = Flask(__name__)


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
        username = request.form['username']
        userpassword = request.form['userpassword']
        return f" authorization successfull, {username} {userpassword}"


#/register
@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        userpassword = request.form['userpassword']
        return f" account successfully created, {username} {userpassword}"


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
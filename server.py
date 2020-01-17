from flask import Flask, render_template, make_response, session
from flask import redirect, url_for, escape, request
import data_manager

app = Flask(__name__)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if 'username' in session:
        message = 'Logged in as %s' % escape(session['username'])
        cars = data_manager.get_cars()
        return render_template('index.html',
                               message=message,
                               cars=cars)
    message = 'You are not logged in.'
    return render_template('index.html',
                           message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        cars = request.form['cars']
        # salt = data_manager.get_salt() -- as bcrypt saves it automatically in the hash
        password = data_manager.hash_password(request.form['password'])
        data_manager.register_user(name, username, email, cars, password)
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db_password = data_manager.get_db_password_for_user(request.form['username'])
        if data_manager.verify_password(request.form['password'], db_password):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return 'no'
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # removes the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/messages', methods=['GET', 'POST'])
def display_messages():
    if request.method == 'POST':
        username = session['username']
        message = request.form['message']
        user_id = data_manager.get_user_id_by_username(username)
        data_manager.add_message(message, user_id)
        return redirect(url_for('display_messages'))
    messages = data_manager.get_all_messages()
    return render_template('messages.html',
                           messages=messages)


@app.route('/settings', methods=['GET', 'POST'])
def display_settings():
    if request.method == 'POST':
        theme = request.form['theme']
        redirect_to_index = redirect('/')
        response = make_response(redirect_to_index)
        response.set_cookie('theme', value=theme, max_age=60*60*24*30)
        data_manager.set_user_theme(session['username'], theme)
        return response
    theme = data_manager.get_settings(session['username'])
    return render_template('settings.html',
                           theme=theme)


if __name__ == '__main__':
    app.run(debug=True)

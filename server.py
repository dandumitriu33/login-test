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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # removes the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

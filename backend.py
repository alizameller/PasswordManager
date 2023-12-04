from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'david_stekol'

users = {
    'user1': {
        'password': generate_password_hash('password1'),
        'passwords': {}
    },
    'user2': {
        'password': generate_password_hash('password1'),
        'passwords': {}
    }
}

# Replace this with a secure method to store passwords
passwords = {}


DATABASE = "password_manager.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    return db


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login_', methods=['POST'])
def login_():
    data = request.get_json()
    username = data.get('username')
    masterkey = data.get('password')
    db = get_db()
    cursor = db.execute(f'SELECT password FROM login_table WHERE username = \'{username}\'')
    password = cursor.fetchall()
    if password:
        print(password[0][0])
    # Store the password securely (in a real scenario, this would involve encryption)
    if not password:
        return jsonify({'message': 'User not found'}), 401

    if not check_password_hash(password[0][0], masterkey):
        return jsonify({'message': 'Incorrect password'}), 401

    session['username'] = username
    db.close()
    return jsonify({'message': 'Login successful'})

@app.route('/register_', methods=['POST'])
def register_():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    db = get_db()
    cursor = db.execute(f'SELECT username FROM login_table WHERE username = \'{username}\'')
    user = cursor.fetchall()

    if user:
        return jsonify({'message': 'Username already exists'}), 400


    db.execute('INSERT INTO login_table (username, password) VALUES (?,?)', (username,generate_password_hash(password)))
    db.commit()
    db.close()

    return jsonify({'message': 'Registration successful'})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out'})

@app.route('/save')
def save():
    return render_template('save.html')

@app.route('/save_password', methods=['POST'])
def save_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    website = data.get('website')
    current_user = session['username']

    db = get_db()
    db.execute('INSERT INTO password_table (username,website_username,website, password) VALUES (?,?,?,?)', (current_user,username,website,password))
    db.commit()
    return jsonify({'message': 'Password saved successfully.'})


@app.route('/get_password/<website>', methods=['GET'])
def get_password(website):
    db = get_db()
    current_user = session['username']
    print(current_user)
    cursor = db.execute(f'SELECT website_username, password FROM password_table WHERE website = \'{website}\' AND username = \'{current_user}\'')
    password = cursor.fetchall()
    db.close()
    return render_template('display.html', info=password)

if __name__ == '__main__':
    app.run( debug=True)

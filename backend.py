from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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

    # Store the password securely (in a real scenario, this would involve encryption)
    if username not in users:
        return jsonify({'message': 'User not found'}), 401

    if not check_password_hash(users[username]['password'], masterkey):
        return jsonify({'message': 'Incorrect password'}), 401

    session['username'] = username
    return jsonify({'message': 'Login successful'})

@app.route('/register_', methods=['POST'])
def register_():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'message': 'Username already exists'}), 400

    users[username] = {
        'password': generate_password_hash(password),
        'passwords': {}
    }

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

    # Store the password securely (in a real scenario, this would involve encryption)
    current_user = users[session['username']]
    current_user['passwords'][website] = {'username': username, 'password': password}
    
    return jsonify({'message': 'Password saved successfully.'})

@app.route('/get_passwords')
def get_passwords():
    if 'username' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    current_user = users[session['username']]
    return jsonify(current_user['passwords'])

if __name__ == '__main__':
    app.run(host='192.168.1.114', port=5000, debug=True)

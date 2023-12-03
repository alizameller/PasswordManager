from flask import Flask, render_template, request, jsonify, g
import sqlite3


app = Flask(__name__)

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


@app.route('/save_password', methods=['POST'])
def save_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    website = data.get('website')


    db = get_db()
    db.execute('INSERT INTO password_table (username,website, password) VALUES (?,?,?)', (username,website,password))
    db.commit()
    # Store the password securely (in a real scenario, this would involve encryption)
    #passwords[website] = {'username': username, 'password': password}
    
    return jsonify({'message': 'Password saved successfully.'})


@app.route('/get_password/<website>', methods=['GET'])
def get_password(website):
    db = get_db()
    cursor = db.execute(f'SELECT username, password FROM password_table WHERE website = \'{website}\'')
    password = cursor.fetchall()
    print(password)
    db.close()
    #if website in passwords:
    #    return jsonify(passwords[website])
    #else:
    #    return jsonify({'message': 'Password not found.'})
    return password

if __name__ == '__main__':
    app.run(debug=True)

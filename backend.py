from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for
import sqlite3
import pyotp
import qrcode
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/static')
from base64 import b64encode
app = Flask(__name__)
app.secret_key = 'david_stekol'



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
    if not password:
        
        return jsonify({'message': 'User not found'}), 401

    if not check_password_hash(password[0][0], masterkey):
        return jsonify({'message': 'Incorrect password'}), 401

    session['username'] = username
    session['authenticated'] = False
   
    return jsonify({'message': 'Login successful'})






@app.route('/verify')
def verify():
    return render_template('verify_otp.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    print(session['username'])
    if 'username' in session and not session.get('authenticated'):
        username = session['username']
        db = get_db()
        if username:
            cursor = db.execute(f'SELECT secret FROM login_table WHERE username = \'{username}\'')
            secret_key = cursor.fetchall()
            totp = pyotp.TOTP(secret_key[0][0])
            
            if totp.verify(request.form['otp']):
                # Mark user as authenticated
                session['authenticated'] = True
                return jsonify({'message': 'Login successful with 2FA'})

    return jsonify({'message': 'Invalid OTP or Authentication State'})

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

    secret_key = pyotp.random_base32()
    db.execute('INSERT INTO login_table (username, password,secret) VALUES (?,?,?)', (username,generate_password_hash(password), secret_key))
    db.commit()
    db.close()

    return jsonify({'message': 'Registration successful'})


@app.route('/setup')
def setup():
    db = get_db()
    cursor = db.execute(f'SELECT username,secret FROM login_table ORDER BY rowid DESC LIMIT 1')
    data = cursor.fetchall()
    username = data[0][0]
    totp = pyotp.TOTP(data[0][1])
    totp_url = totp.provisioning_uri(name=username, issuer_name='PasswordManager')
    qr_code = qrcode.make(totp_url)
    buffer = BytesIO()
    qr_code.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    totp_url = f'data:image/png;base64,{encoded_img}'
    return render_template('setup_otp.html',totp_url=totp_url)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('authenticated', None)
    jsonify({'message': 'Logged out'})
    return render_template('logout.html')

@app.route('/save')
def save():
    return render_template('save.html')

@app.route('/save_password', methods=['POST'])
def save_password():
    data = request.get_json()
    website_username = data.get('username')
    password = data.get('password')
    website = data.get('website')
    current_user = session['username']

    db = get_db()
    db.execute(f'INSERT INTO password_table (username,website, password) VALUES (?,?,?) ON CONFLICT(username,website) DO UPDATE SET password=?;', (current_user,website,password,password))
    db.commit()
    db.close()
    return jsonify({'message': 'Password saved successfully.'})

@app.route('/get_password')
def get_pass():
    return render_template('get_password.html')

@app.route('/load_get_password', methods=['POST'])
def load_get_password():
    data = request.get_json()
    website = data.get('website')
    if website: 
        return redirect(url_for('get_password', website=website))
    return render_template('get_password.html')

@app.route('/get_password/<website>', methods=['GET'])
def get_password(website):
    if not 'username' in session:
        return render_template('error.html', message = 'Please Log In To View Password', error_code = 403)
    db = get_db()
    current_user = session['username']

 
    
    #Fixed by going to prepared statements instead
    cursor = db.execute("SELECT password FROM password_table WHERE website = ? AND username = ?;", (website, current_user))
    password = cursor.fetchall()
    db.close()
    if not password:
        return render_template('error.html', message = 'No password found for this website', error_code = 403)
    return render_template('display.html', info=password, website = website)

if __name__ == '__main__':
    # make sure you pip install pyopenssl -- for https purposes
    # ssl_context flag ensures https communication
    app.run(debug=True, host='10.45.26.56', ssl_context='adhoc')

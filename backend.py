from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Replace this with a secure method to store passwords
passwords = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_password', methods=['POST'])
def save_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    website = data.get('website')

    # Store the password securely (in a real scenario, this would involve encryption)
    passwords[website] = {'username': username, 'password': password}
    
    return jsonify({'message': 'Password saved successfully.'})


@app.route('/get_password/<website>', methods=['GET'])
def get_password(website):
    if website in passwords:
        return jsonify(passwords[website])
    else:
        return jsonify({'message': 'Password not found.'})


if __name__ == '__main__':
    app.run(debug=True)

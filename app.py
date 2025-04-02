from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# MySQL database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'password'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'safisha_laundry'

mysql = MySQL(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if not (username and email and phone and password):
        return jsonify({'error': 'All fields are required'}), 400
    
    password_hash = generate_password_hash(password)
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, phone, password_hash) VALUES (%s, %s, %d, %s)", 
                    (username, email, phone, password_hash))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not (username and password):
        return jsonify({'error': 'Username and password are required'}), 400
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    
    if user and check_password_hash(user[0], password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials. Please try again or sign up.'}), 401

@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.json
    fullname = data.get('fullname')
    phone = data.get('phone')
    physical_address = data.get('address')
    collection_date = data.get('collection_date')
    quantity = data.get('quantity')
    clothing_type = data.get('clothing_type')
    
    if not (fullname and phone and physical_address and collection_date and quantity and clothing_type):
        return jsonify({'error': 'All fields are required'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders (fullname, phone, physical_address, collection_date, quantity, clothing_type) VALUES (%s, %s, %s, %s, %s, %s)",
                    (fullname, phone, physical_address, collection_date, quantity, clothing_type))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Order submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)

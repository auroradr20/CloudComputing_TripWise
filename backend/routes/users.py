from flask import request, jsonify
from backend.db import get_db
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint( "users",__name__)

# Registration and login routes for users. 
# Passwords must contain at least one uppercase letter, one digit and be at least 8 characters long.

@users_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user with a username and password.
    """
    data = request.get_json(silent=True)

    if data:
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    if not username or not password:
        return jsonify({'error' : 'Username and password are required'}), 400
    
    valid_upper= False
    valid_digit= False
    valid_length= len(password) >= 8

    if not valid_length:
        return jsonify({'error' : "Password must be at least 8 characters long"}), 400

    for letter in password:
        if letter.isupper():
            valid_upper = True
        if letter.isdigit():
            valid_digit = True

    if not valid_upper or not valid_digit:
        return jsonify({'error' : "Password must contain at least one uppercase letter and one digit"}), 400
    
    # If the password is valid, we hash it and store the user in the database.

    db= get_db()

    existing_user = db.execute(
        'SELECT id FROM users WHERE username = ?', (username,)
    ).fetchone()

    if existing_user is not None:
        return jsonify({'error':'Username already exists'}), 400
    
    hashed_password = generate_password_hash(password)

    cursor = db.execute(
        "INSERT INTO users (username, password) values(?,?)", 
        (username, hashed_password)
    )

    db.commit()
    return jsonify({
        'message' : 'User registered',
        'user_id' : cursor.lastrowid,
        'username' : username
    }), 201

    # Login route that checks the provided username and password against the database?

@users_bp.route("/login", methods=["POST"])
def login():
    """
    Login a user by checking the username and password in the database.
    """
    data = request.get_json(silent=True)

    if data:
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    if not username and not password:
        return jsonify({'error' : 'Username and password are required'}), 400
    
    db= get_db()

    user = db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    

    if user and check_password_hash(user["password"], password):
        return jsonify({
            'message' : 'Login successful',
            'user_id' : user["id"],
            'username' : user["username"]
        }), 200
    
    return jsonify({'error' : 'Invalid username or password'}), 401


def get_id(username):
    """
    This function returns the user id based on username.
    It can be used by other functions like change username.
    """
    db = get_db()
    user = db.execute("SELECT id FROM users WHERE username = ?",(username,)).fetchone()
    if user is None:
        return None
    else:
        return user["id"]
    

@users_bp.route("/change_username", methods=["PUT"])
def change_username():
    """
    This function changes the user name based on user id, only if the user inputs their password correctly.
    """
    old_username = request.form["username"]
    password = request.form["password"]
    new_username = request.form["new_username"]

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (old_username,)).fetchone()
    if user and check_password_hash(user["password"], password):
        user_id = get_id(old_username)
        if user_id is None:
            return "User is not found", 404
        else:
            db.execute("UPDATE users SET username = ? WHERE id = ?",(new_username,user_id))
            db.commit()
            return "Username successfully changed",200
    else:
        return "Password does not match username", 401
    

@users_bp.route("/change_password", methods=["PUT"])
def change_password():
    """
    This function changes the password based on user id, only if the user inputs their password correctly.
    """
    username = request.form["username"]
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]

    # copy paste from the register function, checks whether the password meets requirements
    valid_upper= False
    valid_digit= False
    valid_length= len(new_password) >= 8
    if not valid_length:
        return "Password must be at least 8 characters long"
    for letter in new_password:
        if letter.isupper():
            valid_upper = True
        if letter.isdigit():
            valid_digit = True
    if not valid_upper or not valid_digit:
        return "Password must contain at least one uppercase letter and one digit"


    db = get_db()
    user_id = get_id(username)
    if user_id is None:
        return "User is not found", 404
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user and check_password_hash(user["password"], old_password):
        hashed_password = generate_password_hash(new_password)
        db.execute( "UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
        db.commit()
        return "Password successfully changed",200
    else:
        return "Password does not match username", 401



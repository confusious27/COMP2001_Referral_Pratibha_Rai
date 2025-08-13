# setting up application
from flask import render_template, jsonify, request
from config import connex_app, app
from models import Comment
from authorize import validate_user, get_local_user

# connection to the .env
from dotenv import load_dotenv

load_dotenv()


# reads file to create routes
connex_app.add_api("swagger.yaml")

# for home.html
@app.route("/")
def home():
    comments = Comment.query.all()
    return render_template("home.html", comments=comments)

# to login/verify user credentials
@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    print(f"Received login data: {data}")

    email = data.get('Email') or data.get('email')
    password = data.get('Password') or data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Login is required'}), 400
    # authenticate
    user = validate_user(email, password)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # get local role info from SQL
    local_user = get_local_user(email)
    if not local_user:
        return jsonify({'message': 'User not found locally'}), 404
    
    return jsonify({'message': 'Login successful!', 'auth_user': user, 'local_user': local_user}), 200

# runs app
if __name__=="__main__":
    connex_app.run(host="0.0.0.0", port=8000, debug=True)
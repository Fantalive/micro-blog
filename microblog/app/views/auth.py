from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    return jsonify({"msg": "Welcome to the authentication API"}), 200


@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Handle registration logic
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'msg': 'Email already exists'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'msg': 'Username already exists'}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201
    else:
        return render_template("register.html")


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    
	if request.method == 'POST':
		data = request.get_json()
		email = data.get('email')
		password = data.get('password')

		user = User.query.filter_by(email=email).first()
		if user is None or not user.check_password(password):
			return jsonify({"msg": "Invalid credentials"}), 401

		access_token = create_access_token(identity=user.id)
		return jsonify(access_token=access_token), 200
	else:
		return render_template("login.html")

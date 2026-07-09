from flask import Blueprint, request, jsonify
from application.database import db
from application.models import User, Company, Student
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    from app import bcrypt
    data = request.get_json() or {}
    identifier = data.get('username') or data.get('email')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"message": "Username/email and password are required."}), 400

    # 1. Check if user exists in the User table 
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if user:
        if bcrypt.check_password_hash(user.password, password):
            if user.isBlacklisted:
                return jsonify({"message": "Your account has been blacklisted."}), 403
            
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"role": user.type}
            )
            return jsonify({
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.name,
                    "role": user.type
                }
            }), 200

    # 2. Check if user exists in the Company table (recruiter)
    company = Company.query.filter((Company.username == identifier) | (Company.email == identifier)).first()
    if company:
        if bcrypt.check_password_hash(company.password, password):
            if company.isBlacklisted:
                return jsonify({"message": "Your company account has been blacklisted."}), 403
            if not company.approved:
                return jsonify({"message": "Your company account is pending approval by the admin."}), 403
            
            access_token = create_access_token(
                identity=f"company_{company.id}",
                additional_claims={"role": "recruiter"}
            )
            return jsonify({
                "access_token": access_token,
                "user": {
                    "id": company.id,
                    "username": company.username,
                    "email": company.email,
                    "name": company.name,
                    "role": "recruiter"
                }
            }), 200

    return jsonify({"message": "Invalid username/email or password."}), 401


@auth_bp.route('/api/auth/signup/student', methods=['POST'])
def signup_student():
    from app import bcrypt
    
    data = request.get_json() or {}
    
    # Required fields
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    # Validate presence
    if not all([username, email, password, name]):
        return jsonify({"message": "All fields (username, email, password, name) are required."}), 400

    # Check uniqueness
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "Username or email already exists."}), 400

    if Company.query.filter((Company.username == username) | (Company.email == email)).first():
        return jsonify({"message": "Username or email already exists."}), 400

    try:
        # Create User
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            name=name,
            type='student'
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Student signed up successfully.",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "name": new_user.name,
                "role": new_user.type
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred during signup.", "error": str(e)}), 500

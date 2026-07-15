from flask import Blueprint, request, jsonify
from sqlalchemy import func
from application.database import db
from application.models import User, Company, Student
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

#API for login 
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    from app import bcrypt
    data = request.get_json() or {}
    identifier = (data.get('username') or data.get('email') or '').strip().lower()
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"message": "Username/email and password are required."}), 400

    #search user table first (case-insensitive username/email match)
    user = User.query.filter(
        (func.lower(User.username) == identifier) | (func.lower(User.email) == identifier)
    ).first()
    if user:
        if user.isBlacklisted:
            return jsonify({"message": "Your account has been blacklisted. Please contact the admin."}), 403
        
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Incorrect password. Please try again."}), 401
        
        if user.type not in ['student', 'admin']:
            return jsonify({"message": "Unauthorized role."}), 403
        
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

    #seach company table if no matching user is found 
    #search company table (case-insensitive username/email match)
    company = Company.query.filter(
        (func.lower(Company.username) == identifier) | (func.lower(Company.email) == identifier)
    ).first()
    if company:
        if company.isBlacklisted:
            return jsonify({"message": "Your company account has been blacklisted. Please contact the admin."}), 403
        
        if not bcrypt.check_password_hash(company.password, password):
            return jsonify({"message": "Incorrect password. Please try again."}), 401
        
        if not company.approved: #only approved companies
            return jsonify({"message": "Your company account is pending approval by the admin."}), 403
        
        access_token = create_access_token(
            identity=f"company_{company.id}",
            additional_claims={"role": "recruiter"} #if all validation passes, a JWT token is created
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

    #if neither the user table nor the company table has any record
    return jsonify({"message": "No account found with that username or email."}), 401

#API for student signup
@auth_bp.route('/api/auth/signup/student', methods=['POST'])
def signup_student():
    from app import bcrypt
    
    data = request.get_json() or {}
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not all([username, email, password, name]):
        return jsonify({"message": "All fields (username, email, password, name) are required."}), 400


    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "Username or email already exists."}), 400

    if Company.query.filter((Company.username == username) | (Company.email == email)).first():
        return jsonify({"message": "Username or email already exists."}), 400

    try:
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

#API for company signup
@auth_bp.route('/api/auth/signup/company', methods=['POST'])
def signup_company():
    from app import bcrypt
    
    data = request.get_json() or {}
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not all([username, email, password, name]):
        return jsonify({"message": "All fields (username, email, password, name) are required."}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "Username or email already exists."}), 400

    if Company.query.filter((Company.username == username) | (Company.email == email)).first():
        return jsonify({"message": "Username or email already exists."}), 400

    try:
       
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_company = Company(
            username=username,
            email=email,
            password=hashed_password,
            name=name,
            approved=False
        )
        db.session.add(new_company)
        db.session.commit()

        return jsonify({
            "message": "Company registered successfully. Pending admin approval.",
            "company": {
                "id": new_company.id,
                "username": new_company.username,
                "email": new_company.email,
                "name": new_company.name,
                "approved": new_company.approved
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred during company registration.", "error": str(e)}), 500

#API for logout
@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful."}), 200


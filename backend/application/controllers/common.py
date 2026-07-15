from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from application.models import User, Company, Drive, Application, Student

common_bp = Blueprint('common', __name__)

@common_bp.route('/common/student/profile/<int:id>', methods=['GET'])
@jwt_required()
def get_student_profile(id):
    claims = get_jwt()
    role = claims.get('role')
    identity = get_jwt_identity()

    # Look up user in user table, only matching type='student'
    user = User.query.filter_by(id=id, type='student').first()
    if not user:
        return jsonify({"message": "Student profile not found."}), 404

    student = user.student

    # Security check:
    # - Student can access only their own profile.
    # - Admin can access all profiles.
    # - Company/recruiter can access all profiles.
    if role == 'student':
        if str(user.id) != str(identity):
            return jsonify({"message": "Access forbidden: You can only view your own profile."}), 403
    elif role not in ['admin', 'recruiter']:
        return jsonify({"message": "Access forbidden: Unauthorized role."}), 403

    profile_data = {
        "id": student.id if student else None,
        "user_id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "roll_number": student.roll_number if student else None,
        "branch": student.branch if student else None,
        "year_of_study": student.year_of_study if student else None,
        "cgpa": student.cgpa if student else None,
        "resume": student.resume if student else None,
        "isBlacklisted": user.isBlacklisted,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
    
    return jsonify(profile_data), 200


@common_bp.route('/common/company/profile/<int:id>', methods=['GET'])
@jwt_required()
def get_company_profile(id):
    claims = get_jwt()
    role = claims.get('role')

    if role not in ['admin', 'student', 'recruiter']:
        return jsonify({"message": "Access forbidden: Unauthorized role."}), 403

    company = Company.query.get(id)
    if not company:
        return jsonify({"message": "Company profile not found."}), 404

    profile_data = {
        "id": company.id,
        "username": company.username,
        "email": company.email,
        "name": company.name,
        "approved": company.approved,
        "description": company.description,
        "industry": company.industry,
        "scale": company.scale,
        "headOffice": company.headOffice,
        "website": company.website,
        "logo": company.logo,
        "pocName": company.pocName,
        "pocEmail": company.pocEmail,
        "isBlacklisted": company.isBlacklisted,
        "created_at": company.created_at.isoformat() if company.created_at else None
    }
    
    return jsonify(profile_data), 200


@common_bp.route('/common/drive/profile/<int:id>', methods=['GET'])
@jwt_required()
def get_drive_profile(id):
    claims = get_jwt()
    role = claims.get('role')

    if role not in ['admin', 'student', 'recruiter']:
        return jsonify({"message": "Access forbidden: Unauthorized role."}), 403

    drive = Drive.query.get(id)
    if not drive:
        return jsonify({"message": "Drive profile not found."}), 404

    company = drive.company
    
    applied = False
    is_blacklisted = False
    if role == 'student':
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if user:
            is_blacklisted = user.isBlacklisted
            if user.student:
                app = Application.query.filter_by(student_id=user.student.id, drive_id=drive.id).first()
                if app:
                    applied = True

    profile_data = {
        "id": drive.id,
        "company_id": drive.company_id,
        "company_name": company.name if company else None,
        "company_industry": company.industry if company else None,
        "status": drive.status,
        "title": drive.title,
        "description": drive.description,
        "eligibility": drive.eligibility,
        "batch": drive.batch,
        "branches": drive.branches,
        "deadline": drive.deadline.isoformat() if drive.deadline else None,
        "skillsRequired": drive.skillsRequired,
        "payScale": drive.payScale,
        "location": drive.location,
        "workMode": drive.workMode,
        "interviewRounds": drive.interviewRounds,
        "positions": drive.positions,
        "created_at": drive.created_at.isoformat() if drive.created_at else None,
        "approved": drive.approved,
        "applied": applied,
        "isBlacklisted": is_blacklisted
    }
    
    return jsonify(profile_data), 200



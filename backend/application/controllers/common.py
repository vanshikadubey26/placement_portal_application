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

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from application.models import User, Company, Drive, Application, Student

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/all-students', methods=['GET'])
@jwt_required()
def get_all_students():
    # Access role verification
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    users_query = User.query.filter_by(type='student').all()
    students_list = []
    
    for user in users_query:
        # access related student model via user.student relationship
        s = user.student
            
        students_list.append({
            "id": s.id if s else None,
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "roll_number": s.roll_number if s else None,
            "branch": s.branch if s else None,
            "year_of_study": s.year_of_study if s else None,
            "cgpa": s.cgpa if s else None,
            "resume": s.resume if s else None,
            "isBlacklisted": user.isBlacklisted,
            "created_at": user.created_at.isoformat() if user.created_at else None
        })
        
    return jsonify(students_list), 200


@admin_bp.route('/admin/all-companies', methods=['GET'])
@jwt_required()
def get_all_companies():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    companies = Company.query.all()
    companies_list = [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "industry": c.industry,
            "isBlacklisted": c.isBlacklisted,
            "approved": c.approved,
        }
        for c in companies
    ]

    return jsonify(companies_list), 200


@admin_bp.route('/admin/all-drives', methods=['GET'])
@jwt_required()
def get_all_drives():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    drives = Drive.query.all()
    drives_list = [
        {
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "status": d.status,
            "eligibility": d.eligibility,
            "batch": d.batch,
            "branches": d.branches,
            "deadline": d.deadline.isoformat() if d.deadline else None,
            "skillsRequired": d.skillsRequired,
            "payScale": d.payScale,
            "location": d.location,
            "workMode": d.workMode,
            "interviewRounds": d.interviewRounds,
            "positions": d.positions,
            "company_id": d.company_id,
            "company_name": d.company.name if d.company else None,
            "company_industry": d.company.industry if d.company else None,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in drives
    ]

    return jsonify(drives_list), 200


@admin_bp.route('/admin/all-applications', methods=['GET'])
@jwt_required()
def get_all_applications():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    applications = Application.query.all()
    result = []
    for app in applications:
        student = Student.query.get(app.student_id)
        user = User.query.get(student.user_id) if student else None
        drive = Drive.query.get(app.drive_id)
        company = drive.company if drive else None
        result.append({
            "id": app.id,
            "status": app.status,
            "comment": app.comment,
            "created_at": app.created_at.isoformat() if app.created_at else None,
            "updated_at": app.updated_at.isoformat() if app.updated_at else None,
            "student_id": app.student_id,
            "student_name": user.name if user else None,
            "student_email": user.email if user else None,
            "roll_number": student.roll_number if student else None,
            "drive_id": app.drive_id,
            "drive_title": drive.title if drive else None,
            "company_name": company.name if company else None,
            "company_industry": company.industry if company else None,
        })

    return jsonify(result), 200


@admin_bp.route('/admin/stats', methods=['GET'])
@jwt_required()
def get_admin_stats():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    total_students = User.query.filter_by(type='student').count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_job_postings": total_drives,
        "total_applications": total_applications
    }), 200

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from application.models import User, Company, Drive, Application, Student
from application.database import db 
from application.controllers.redis import get_cache, set_cache, delete_cache

admin_bp = Blueprint('admin', __name__)

# API to fetch all students
@admin_bp.route('/admin/all-students', methods=['GET'])
@jwt_required()
def get_all_students():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    cached_students = get_cache("admin_all_students")
    if cached_students is not None:
        print("CACHE HIT: admin_all_students")
        return jsonify(cached_students), 200
    else:
        print("CACHE MISS: admin_all_students")

    users_query = User.query.filter_by(type='student').all()
    students_list = []
    
    for user in users_query:
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
        
    set_cache("admin_all_students", students_list, timeout=60)
    return jsonify(students_list), 200


#API to fetch all companies
@admin_bp.route('/admin/all-companies', methods=['GET'])
@jwt_required()
def get_all_companies():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    cached_companies = get_cache("admin_all_companies")
    if cached_companies is not None:
        print("CACHE HIT: admin_all_companies")
        return jsonify(cached_companies), 200
    else:
        print("CACHE MISS: admin_all_companies")

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



    set_cache("admin_all_companies", companies_list, timeout=60)
    return jsonify(companies_list), 200

#API to fetch all drives
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
            "approved": d.approved,
        }
        for d in drives
    ]

    return jsonify(drives_list), 200

#API to fetch all applications
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
            "student_user_id": user.id if user else None,
            "student_name": user.name if user else None,
            "student_email": user.email if user else None,
            "roll_number": student.roll_number if student else None,
            "drive_id": app.drive_id,
            "drive_title": drive.title if drive else None,
            "company_name": company.name if company else None,
            "company_industry": company.industry if company else None,
        })

    return jsonify(result), 200

#API to fetch stats for admin dashboard
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

# API to fetch stats for Admin Dashboard
@admin_bp.route('/admin/student/blacklist/<int:user_id>', methods=['PUT'])
@jwt_required()
def student_blacklist(user_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    user.isBlacklisted = not user.isBlacklisted
    db.session.commit()
    delete_cache("admin_all_students")

    return jsonify({"message": f"User {user.name} {'blacklisted' if user.isBlacklisted else 'unblacklisted'} successfully."}), 200

#API to Blacklist Company
@admin_bp.route('/admin/company/blacklist/<int:company_id>', methods=['PUT'])
@jwt_required()
def company_blacklist(company_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403
    
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404
    
    company.isBlacklisted = not company.isBlacklisted
    db.session.commit()
    delete_cache("admin_all_companies")

    return jsonify({"message": f"Company {company.name} {'blacklisted' if company.isBlacklisted else 'unblacklisted'} successfully."}), 200

#API to Approve Company
@admin_bp.route('/admin/company/approve/<int:company_id>', methods=['PUT'])
@jwt_required()
def company_approve(company_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403
    
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404
    
    company.approved = not company.approved
    db.session.commit()
    delete_cache("admin_all_companies")

    return jsonify({"message": f"Company {company.name} {'approved' if company.approved else 'unapproved'} successfully."}), 200

#API to Approve Drive
@admin_bp.route('/admin/drive/approve/<int:drive_id>', methods=['PUT'])
@jwt_required()
def drive_approve(drive_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    drive = Drive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found."}), 404

    drive.approved = not drive.approved
    db.session.commit()

    return jsonify({
        "message": f"Drive {drive.title} {'approved' if drive.approved else 'unapproved'} successfully.",
        "approved": drive.approved
    }), 200
    
#API to Search Students
@admin_bp.route('/admin/students/search', methods=['GET'])
@jwt_required()
def search_students():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    q = request.args.get('q', '').strip()
    query = User.query.filter(User.type == 'student')
    if q:
        query = query.outerjoin(Student, User.id == Student.user_id)
        id_filter = False
        if q.isdigit():
            id_filter = (Student.id == int(q))
            
        query = query.filter(
            User.name.ilike(f"%{q}%") |
            User.email.ilike(f"%{q}%") |
            (Student.roll_number.ilike(f"%{q}%")) |
            id_filter
        )
    
    users = query.all()
    students_list = []
    for user in users:
        s = user.student #retrieve related student object from the User object using SQLAlchemy relationship
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

#API to Search Companies
@admin_bp.route('/admin/companies/search', methods=['GET'])
@jwt_required()
def search_companies():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403
    q = request.args.get('q', '').strip()
    query = Company.query
    if q:
        query = query.filter(
            Company.name.ilike(f"%{q}%") | #search by company name, email, OR industry (case insensitive)
            Company.email.ilike(f"%{q}%") | 
            Company.industry.ilike(f"%{q}%")
        )    
    companies = query.all()
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

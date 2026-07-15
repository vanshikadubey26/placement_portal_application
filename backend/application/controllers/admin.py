from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from application.models import User, Company, Drive, Application, Student, Interview
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
    cache_key = f"admin_search_students_{q}"
    cached_res = get_cache(cache_key)
    if cached_res is not None:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_res), 200
    else:
        print(f"CACHE MISS: {cache_key}")

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
    set_cache(cache_key, students_list, timeout=60)
    return jsonify(students_list), 200

#API to Search Companies
@admin_bp.route('/admin/companies/search', methods=['GET'])
@jwt_required()
def search_companies():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403
    q = request.args.get('q', '').strip()
    cache_key = f"admin_search_companies_{q}"
    cached_res = get_cache(cache_key)
    if cached_res is not None:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_res), 200
    else:
        print(f"CACHE MISS: {cache_key}")

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
    set_cache(cache_key, companies_list, timeout=60)
    return jsonify(companies_list), 200


#API to fetch monthly daily statistics for reports console
@admin_bp.route('/admin/reports/monthly', methods=['GET'])
@jwt_required()
def get_monthly_reports():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only."}), 403

    import datetime
    import calendar

    month_str = request.args.get('month')
    if month_str:
        try:
            year, month = map(int, month_str.split('-'))
        except ValueError:
            return jsonify({"message": "Invalid month format. Use YYYY-MM"}), 400
    else:
        now = datetime.datetime.now()
        year, month = now.year, now.month

    from application.utils import IST
    # Start and End range of the month
    _, last_day = calendar.monthrange(year, month)
    start_date = datetime.datetime(year, month, 1, 0, 0, 0, tzinfo=IST)
    end_date = datetime.datetime(year, month, last_day, 23, 59, 59, tzinfo=IST)

    daily_stats = {day: {"students": 0, "companies": 0, "drives": 0, "applications": 0, "interviews": 0} for day in range(1, 32)}

    # Students
    students_data = User.query.filter(
        User.type == 'student',
        User.created_at >= start_date,
        User.created_at <= end_date
    ).all()
    for s in students_data:
        if s.created_at:
            day = s.created_at.day
            if day in daily_stats:
                daily_stats[day]["students"] += 1

    # Companies
    companies_data = Company.query.filter(
        Company.created_at >= start_date,
        Company.created_at <= end_date
    ).all()
    for c in companies_data:
        if c.created_at:
            day = c.created_at.day
            if day in daily_stats:
                daily_stats[day]["companies"] += 1

    # Drives
    drives_data = Drive.query.filter(
        Drive.created_at >= start_date,
        Drive.created_at <= end_date
    ).all()
    for d in drives_data:
        if d.created_at:
            day = d.created_at.day
            if day in daily_stats:
                daily_stats[day]["drives"] += 1

    # Applications
    apps_data = Application.query.filter(
        Application.created_at >= start_date,
        Application.created_at <= end_date
    ).all()
    for a in apps_data:
        if a.created_at:
            day = a.created_at.day
            if day in daily_stats:
                daily_stats[day]["applications"] += 1

    # Interviews
    interviews_data = Interview.query.filter(
        Interview.created_at >= start_date,
        Interview.created_at <= end_date
    ).all()
    for i in interviews_data:
        if i.created_at:
            day = i.created_at.day
            if day in daily_stats:
                daily_stats[day]["interviews"] += 1

    labels = [f"Day {day}" for day in range(1, 32)]
    students_list = [daily_stats[day]["students"] for day in range(1, 32)]
    companies_list = [daily_stats[day]["companies"] for day in range(1, 32)]
    drives_list = [daily_stats[day]["drives"] for day in range(1, 32)]
    applications_list = [daily_stats[day]["applications"] for day in range(1, 32)]
    interviews_list = [daily_stats[day]["interviews"] for day in range(1, 32)]

    return jsonify({
        "month": f"{year}-{month:02d}",
        "labels": labels,
        "students": students_list,
        "companies": companies_list,
        "drives": drives_list,
        "applications": applications_list,
        "interviews": interviews_list
    }), 200


from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from application.models import User, Student, Drive, Application, Interview, Company
from application.database import db
from datetime import datetime

student_bp = Blueprint('student', __name__)

@student_bp.route('/api/student/profile/status', methods=['GET'])
@jwt_required()
def get_student_profile_status():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
    
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    student = user.student
    return jsonify({
        "hasProfile": student is not None,
        "isBlacklisted": user.isBlacklisted,
        "student": {
            "id": student.id if student else None,
            "roll_number": student.roll_number if student else None,
            "branch": student.branch if student else None,
            "year_of_study": student.year_of_study if student else None,
            "cgpa": student.cgpa if student else None,
            "resume": student.resume if student else None
        } if student else None
    }), 200

@student_bp.route('/api/student/profile', methods=['GET'])
@jwt_required()
def get_student_profile():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    student = user.student
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "roll_number": student.roll_number if student else "",
        "branch": student.branch if student else "",
        "year_of_study": student.year_of_study if student else "",
        "cgpa": student.cgpa if student else "",
        "resume": student.resume if student else ""
    }), 200

@student_bp.route('/api/student/profile', methods=['PUT'])
@jwt_required()
def update_student_profile():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    data = request.get_json() or {}
    
    # Update User info
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    # Update/Create Student info
    student = user.student
    if not student:
        student = Student(user_id=user.id)
        db.session.add(student)

    roll_number = data.get('roll_number')
    if roll_number:
        # Check uniqueness
        existing = Student.query.filter_by(roll_number=roll_number).first()
        if existing and existing.user_id != user.id:
            return jsonify({"message": "Roll number already exists."}), 400
        student.roll_number = roll_number

    student.branch = data.get('branch', student.branch)
    
    year_of_study = data.get('year_of_study')
    if year_of_study is not None:
        try:
            student.year_of_study = int(year_of_study)
        except ValueError:
            pass

    cgpa = data.get('cgpa')
    if cgpa is not None:
        try:
            student.cgpa = float(cgpa)
        except ValueError:
            pass

    student.resume = data.get('resume', student.resume)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database update failed.", "error": str(e)}), 500

    return jsonify({
        "message": "Profile updated successfully.",
        "profile": {
            "name": user.name,
            "email": user.email,
            "roll_number": student.roll_number,
            "branch": student.branch,
            "year_of_study": student.year_of_study,
            "cgpa": student.cgpa,
            "resume": student.resume
        }
    }), 200

@student_bp.route('/api/student/profile/setup', methods=['POST'])
@jwt_required()
def setup_student_profile():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
    
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    data = request.get_json() or {}
    roll_number = data.get('roll_number')
    branch = data.get('branch')
    year_of_study = data.get('year_of_study')
    cgpa = data.get('cgpa')
    resume = data.get('resume')
    
    if not all([roll_number, branch, year_of_study, cgpa]):
        return jsonify({"message": "Roll number, branch, year of study, and CGPA are required."}), 400
    
    # Check if roll number already exists for another student
    existing = Student.query.filter_by(roll_number=roll_number).first()
    if existing and existing.user_id != user_id:
        return jsonify({"message": "Roll number already exists."}), 400
        
    student = user.student
    if not student:
        student = Student(user_id=user_id)
        db.session.add(student)
        
    student.roll_number = roll_number
    student.branch = branch
    student.year_of_study = int(year_of_study)
    student.cgpa = float(cgpa)
    if resume:
        student.resume = resume
        
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to save profile.", "error": str(e)}), 500
        
    return jsonify({"message": "Profile updated successfully.", "student_id": student.id}), 200

@student_bp.route('/api/student/drives', methods=['GET'])
@jwt_required()
def get_eligible_drives():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
        
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = user.student
    
    # Approved drives only
    drives = Drive.query.filter_by(approved=True, status='Hiring').all()
    
    drives_list = []
    for d in drives:
        # Check if already applied
        applied = False
        application_status = None
        if student:
            app = Application.query.filter_by(student_id=student.id, drive_id=d.id).first()
            if app:
                applied = True
                application_status = app.status
                
        drives_list.append({
            "id": d.id,
            "title": d.title,
            "company_name": d.company.name if d.company else "Unknown Company",
            "company_id": d.company_id,
            "description": d.description,
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
            "applied": applied,
            "applicationStatus": application_status
        })
        
    return jsonify(drives_list), 200

@student_bp.route('/api/student/approved-drives', methods=['GET'])
@jwt_required()
def get_approved_drives():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
        
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = user.student
    
    # Approved drives only
    drives = Drive.query.filter_by(approved=True).all()
    
    drives_list = []
    active_count = 0
    closed_count = 0
    now = datetime.now()
    
    for d in drives:
        is_closed = False
        if d.deadline and now > d.deadline:
            is_closed = True
        
        if is_closed:
            closed_count += 1
        else:
            active_count += 1
        applied = False
        application_status = None
        if student:
            app = Application.query.filter_by(student_id=student.id, drive_id=d.id).first()
            if app:
                applied = True
                application_status = app.status
                
        drives_list.append({
            "id": d.id,
            "title": d.title,
            "company_name": d.company.name if d.company else "Unknown Company",
            "company_id": d.company_id,
            "description": d.description,
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
            "applied": applied,
            "applicationStatus": application_status,
            "isClosed": is_closed
        })
        
    return jsonify({
        "drives": drives_list,
        "activeCount": active_count,
        "closedCount": closed_count
    }), 200

@student_bp.route('/api/student/apply/<int:drive_id>', methods=['POST'])
@jwt_required()
def apply_to_drive(drive_id):
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
        
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.isBlacklisted:
        return jsonify({"message": "You cannot apply because your account is blacklisted."}), 403
        
    student = user.student
    if not student:
        return jsonify({"message": "Please set up your profile first before applying."}), 400
        
    drive = Drive.query.get(drive_id)
    if not drive or not drive.approved:
        return jsonify({"message": "Placement drive is not active or not found."}), 404
        
    # Check deadline
    if drive.deadline and datetime.now() > drive.deadline:
        return jsonify({"message": "The application deadline for this drive has passed."}), 400
        
    # Check if already applied
    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        return jsonify({"message": "You have already applied to this drive."}), 400
        
    # Eligibility checks removed (verified manually)

    new_app = Application(
        student_id=student.id,
        drive_id=drive_id,
        status='applied'
    )
    
    try:
        db.session.add(new_app)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to apply.", "error": str(e)}), 500
        
    return jsonify({"message": "Successfully applied to placement drive!"}), 201

@student_bp.route('/api/student/applications', methods=['GET'])
@jwt_required()
def get_student_applications():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
        
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = user.student
    if not student:
        return jsonify([]), 200
        
    apps = Application.query.filter_by(student_id=student.id).all()
    apps_list = []
    for a in apps:
        drive = a.drive
        apps_list.append({
            "id": a.id,
            "drive_id": a.drive_id,
            "driveTitle": drive.title if drive else "Unknown Drive",
            "companyName": drive.company.name if drive and drive.company else "Unknown Company",
            "status": a.status,
            "comment": a.comment,
            "appliedAt": a.created_at.isoformat() if a.created_at else None,
            "updatedAt": a.updated_at.isoformat() if a.updated_at else None
        })
        
    return jsonify(apps_list), 200

@student_bp.route('/api/student/interviews', methods=['GET'])
@jwt_required()
def get_student_interviews():
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
        
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = user.student
    if not student:
        return jsonify([]), 200
        
    apps = Application.query.filter_by(student_id=student.id).all()
    app_ids = [a.id for a in apps]
    if not app_ids:
        return jsonify([]), 200
        
    app_map = {a.id: a for a in apps}
    interviews = Interview.query.filter(Interview.application_id.in_(app_ids)).order_by(Interview.scheduled_at.asc()).all()
    
    interviews_list = []
    for iv in interviews:
        app = app_map.get(iv.application_id)
        drive = app.drive if app else None
        interviews_list.append({
            "id": iv.id,
            "application_id": iv.application_id,
            "application_status": app.status if app else None,
            "driveTitle": drive.title if drive else "Unknown Drive",
            "companyName": drive.company.name if drive and drive.company else "Unknown Company",
            "scheduled_at": iv.scheduled_at.isoformat(),
            "mode": iv.mode,
            "location": iv.location,
            "meeting_link": iv.meeting_link
        })
        
    return jsonify(interviews_list), 200

@student_bp.route('/api/student/application/<int:app_id>/accept-offer', methods=['POST'])
@jwt_required()
def accept_offer(app_id):
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({"message": "Access forbidden: Students only."}), 403
        
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = user.student
    if not student:
        return jsonify({"message": "Student profile not found."}), 404
        
    app = Application.query.get(app_id)
    if not app or app.student_id != student.id:
        return jsonify({"message": "Application not found or access forbidden."}), 404
        
    if app.status != 'Job Offered':
        return jsonify({"message": "No active job offer to accept for this application."}), 400
        
    app.status = 'Offer Accepted'
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to accept offer.", "error": str(e)}), 500
        
    return jsonify({"message": "Offer accepted successfully!", "status": app.status}), 200

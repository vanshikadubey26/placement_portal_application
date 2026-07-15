from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from application.models import Company, Drive, Application, Interview
from application.database import db
from datetime import datetime

company_bp = Blueprint('company', __name__)

@company_bp.route('/api/company/profile', methods=['GET'])
@jwt_required()
def get_company_profile():
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    return jsonify({
        "id": company.id,
        "username": company.username,
        "email": company.email,
        "name": company.name,
        "description": company.description,
        "industry": company.industry,
        "scale": company.scale,
        "headOffice": company.headOffice,
        "website": company.website,
        "logo": company.logo,
        "pocName": company.pocName,
        "pocEmail": company.pocEmail
    }), 200

@company_bp.route('/api/company/profile', methods=['PUT'])
@jwt_required()
def update_company_profile():
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    data = request.get_json() or {}

    # Validations corresponding to String(150) columns


    company.description = data.get('description', company.description)
    company.industry = data.get('industry', company.industry)
    company.scale = data.get('scale', company.scale)
    company.headOffice = data.get('headOffice', company.headOffice)
    company.website = data.get('website', company.website)
    company.logo = data.get('logo', company.logo)
    company.pocName = data.get('pocName', company.pocName)
    company.pocEmail = data.get('pocEmail', company.pocEmail)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database update failed.", "error": str(e)}), 500

    return jsonify({
        "message": "Profile updated successfully.",
        "profile": {
            "name": company.name,
            "description": company.description,
            "industry": company.industry,
            "scale": company.scale,
            "headOffice": company.headOffice,
            "website": company.website,
            "logo": company.logo,
            "pocName": company.pocName,
            "pocEmail": company.pocEmail
        }
    }), 200

@company_bp.route('/api/company/drives', methods=['GET'])
@jwt_required()
def get_company_drives():
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    drives = Drive.query.filter_by(company_id=company.id).all()
    drives_list = []
    for d in drives:
        drives_list.append({
            "id": d.id,
            "title": d.title,
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
            "approved": d.approved,
            "status": d.status
        })

    return jsonify(drives_list), 200

@company_bp.route('/api/company/drive/create', methods=['POST'])
@jwt_required()
def create_company_drive():
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({"message": "Job title is required."}), 400

    deadline_str = data.get('deadline')
    deadline = None
    if deadline_str:
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                deadline = datetime.strptime(deadline_str, fmt)
                break
            except ValueError:
                continue
        if not deadline:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM."}), 400

    new_drive = Drive(
        company_id=company.id,
        title=title,
        description=data.get('description'),
        eligibility=data.get('eligibility'),
        batch=data.get('batch', ''),
        branches=data.get('branches'),
        deadline=deadline,
        skillsRequired=data.get('skillsRequired'),
        payScale=data.get('payScale'),
        location=data.get('location'),
        workMode=data.get('workMode', 'On-site'),
        interviewRounds=data.get('interviewRounds'),
        positions=int(data.get('positions', 1)) if data.get('positions') else 1,
        approved=False,
        status='Unapproved'
    )

    try:
        db.session.add(new_drive)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to save placement drive.", "error": str(e)}), 500

    return jsonify({
        "message": "Placement drive created successfully. Pending admin approval.",
        "drive": {
            "id": new_drive.id,
            "title": new_drive.title,
            "description": new_drive.description,
            "eligibility": new_drive.eligibility,
            "batch": new_drive.batch,
            "branches": new_drive.branches,
            "deadline": new_drive.deadline.isoformat() if new_drive.deadline else None,
            "skillsRequired": new_drive.skillsRequired,
            "payScale": new_drive.payScale,
            "location": new_drive.location,
            "workMode": new_drive.workMode,
            "interviewRounds": new_drive.interviewRounds,
            "positions": new_drive.positions,
            "approved": new_drive.approved,
            "status": new_drive.status
        }
    }), 201

@company_bp.route('/api/company/applications', methods=['GET'])
@jwt_required()
def get_company_applications():
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    drives = Drive.query.filter_by(company_id=company.id).all()
    drive_ids = [d.id for d in drives]
    if not drive_ids:
        return jsonify([]), 200

    apps = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
    apps_list = []
    for a in apps:
        student = a.student
        user = student.user if student else None
        drive = a.drive
        apps_list.append({
            "id": a.id,
            "studentName": user.name if user else "Unknown Student",
            "rollNumber": student.roll_number if student else "N/A",
            "branch": student.branch if student else "N/A",
            "cgpa": student.cgpa if student else 0.0,
            "driveTitle": drive.title if drive else "Unknown Drive",
            "status": a.status,
            "appliedAt": a.created_at.isoformat() if a.created_at else None
        })

    return jsonify(apps_list), 200

@company_bp.route('/api/company/application/<int:app_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(app_id):
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"message": "Application not found."}), 404

    if application.drive.company_id != company.id:
        return jsonify({"message": "Access forbidden: Not your drive's application."}), 403

    data = request.get_json() or {}
    status = data.get('status')
    comment = data.get('comment')
    if not status:
        return jsonify({"message": "Status is required."}), 400

    application.status = status
    if comment is not None:
        application.comment = comment

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update application status.", "error": str(e)}), 500

    return jsonify({
        "message": f"Application status updated to '{status}' successfully.",
        "application_id": application.id,
        "status": application.status,
        "comment": application.comment
    }), 200


@company_bp.route('/api/company/application/<int:app_id>/interview', methods=['POST'])
@jwt_required()
def schedule_interview(app_id):
    """Schedule an interview for a shortlisted application."""
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"message": "Application not found."}), 404

    # Ensure the application belongs to this company's drive
    if application.drive.company_id != company.id:
        return jsonify({"message": "Access forbidden: Not your drive's application."}), 403

    data = request.get_json() or {}

    # Required fields
    scheduled_at_str = data.get('scheduled_at')
    mode = data.get('mode')
    if not scheduled_at_str:
        return jsonify({"message": "scheduled_at is required."}), 400
    if not mode:
        return jsonify({"message": "mode is required."}), 400

    # Parse scheduled_at datetime
    scheduled_at = None
    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            scheduled_at = datetime.strptime(scheduled_at_str, fmt)
            break
        except ValueError:
            continue
    if not scheduled_at:
        return jsonify({"message": "Invalid scheduled_at format. Use YYYY-MM-DDTHH:MM."}), 400

    new_interview = Interview(
        application_id=app_id,
        scheduled_at=scheduled_at,
        mode=mode,
        location=data.get('location'),
        meeting_link=data.get('meeting_link')
    )

    try:
        db.session.add(new_interview)
        # Update the application status to reflect interview has been scheduled
        application.status = 'Interview Scheduled'
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to schedule interview.", "error": str(e)}), 500

    return jsonify({
        "message": "Interview scheduled successfully.",
        "interview": {
            "id": new_interview.id,
            "application_id": new_interview.application_id,
            "scheduled_at": new_interview.scheduled_at.isoformat(),
            "mode": new_interview.mode,
            "location": new_interview.location,
            "meeting_link": new_interview.meeting_link,
            "created_at": new_interview.created_at.isoformat() if new_interview.created_at else None
        },
        "application_status": application.status
    }), 201


@company_bp.route('/api/company/interviews', methods=['GET'])
@jwt_required()
def get_company_interviews():
    """Fetch all interviews scheduled for this company's drives."""
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    # Get all drive ids for this company
    drives = Drive.query.filter_by(company_id=company.id).all()
    drive_ids = [d.id for d in drives]
    if not drive_ids:
        return jsonify([]), 200

    # Get all applications for those drives
    apps = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
    app_ids = [a.id for a in apps]
    if not app_ids:
        return jsonify([]), 200

    # Map application_id -> application for quick lookup
    app_map = {a.id: a for a in apps}

    # Get all interviews for those applications
    interviews = Interview.query.filter(Interview.application_id.in_(app_ids)).order_by(Interview.scheduled_at.asc()).all()

    result = []
    for iv in interviews:
        app = app_map.get(iv.application_id)
        if not app:
            continue
        student = app.student
        user = student.user if student else None
        drive = app.drive
        result.append({
            "id": iv.id,
            "application_id": iv.application_id,
            "application_status": app.status,
            "studentName": user.name if user else "Unknown Student",
            "rollNumber": student.roll_number if student else "N/A",
            "branch": student.branch if student else "N/A",
            "driveTitle": drive.title if drive else "Unknown Drive",
            "scheduled_at": iv.scheduled_at.isoformat(),
            "mode": iv.mode,
            "location": iv.location,
            "meeting_link": iv.meeting_link,
            "created_at": iv.created_at.isoformat() if iv.created_at else None
        })

    return jsonify(result), 200


@company_bp.route('/api/company/application/<int:app_id>/offer-letter', methods=['POST'])
@jwt_required()
def send_offer_letter(app_id):
    """Mark an application as having received an offer letter."""
    claims = get_jwt()
    if claims.get('role') != 'recruiter':
        return jsonify({"message": "Access forbidden: Recruiters only."}), 403

    identity = get_jwt_identity()
    if not identity or not identity.startswith("company_"):
        return jsonify({"message": "Invalid token identity."}), 400

    try:
        company_id = int(identity.split("_")[1])
    except (ValueError, IndexError):
        return jsonify({"message": "Invalid token identity structure."}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found."}), 404

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"message": "Application not found."}), 404

    # Ensure the application belongs to this company's drive
    if application.drive.company_id != company.id:
        return jsonify({"message": "Access forbidden: Not your drive's application."}), 403

    application.status = 'Job Offered'

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to send offer letter.", "error": str(e)}), 500

    return jsonify({
        "message": f"Offer letter sent successfully to application #{app_id}.",
        "application_id": application.id,
        "status": application.status
    }), 200

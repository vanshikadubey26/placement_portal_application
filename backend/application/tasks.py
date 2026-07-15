from application.celery_app import celery
from application.database import db
from application.models import User, Student, Company, Drive, Application, Interview
import datetime
import os
import csv
from application.utils import IST

# Helper to ensure static folders exist
def ensure_folders():
    os.makedirs('static/reports', exist_ok=True)
    os.makedirs('static/exports', exist_ok=True)

@celery.task
def send_interview_reminders():
    """
    Periodic job that runs to send interview reminders to students.
    Checks for interviews scheduled within the next 24 hours.
    """
    now = datetime.datetime.now(IST)
    tomorrow = now + datetime.timedelta(days=1)
    
    interviews = Interview.query.filter(
        Interview.scheduled_at >= now,
        Interview.scheduled_at <= tomorrow
    ).all()
    
    reminders_sent = 0
    print(f"[CELERY BEAT] Running Interview Reminder Job at {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for interview in interviews:
        app = interview.application
        if not app:
            continue
        student = app.student
        if not student:
            continue
        user = student.user
        if not user:
            continue
        drive = app.drive
        company = drive.company if drive else None
        company_name = company.name if company else "Company"
        
        # Email / GChat / SMS mock send logs
        student_email = user.email
        student_name = user.name
        drive_title = drive.title if drive else "Job Posting"
        time_str = interview.scheduled_at.strftime('%Y-%m-%d %H:%M')
        
        print(f"--- INTERVIEW REMINDER SENT ---")
        print(f"Recipient: {student_name} ({student_email})")
        print(f"Channel: Email & SMS & GChat Alert")
        print(f"Message: Dear {student_name}, you have an interview scheduled for the drive '{drive_title}' with {company_name} on {time_str}. Mode: {interview.mode}. Location/Link: {interview.meeting_link or interview.location or 'N/A'}")
        print(f"-------------------------------")
        reminders_sent += 1
        
    return f"Sent {reminders_sent} interview reminders."

@celery.task
def generate_monthly_company_reports():
    """
    Periodic job that runs monthly (e.g. 1st of every month) to generate HTML placement reports for all companies.
    """
    ensure_folders()
    now = datetime.datetime.now(IST)
    # Target previous month
    year = now.year
    month = now.month - 1
    if month == 0:
        month = 12
        year -= 1
        
    companies = Company.query.filter_by(isBlacklisted=False).all()
    reports_generated = 0
    
    for company in companies:
        drives = Drive.query.filter_by(company_id=company.id).all()
        drive_ids = [d.id for d in drives]
        
        total_drives = len(drives)
        total_apps = 0
        total_shortlisted = 0
        total_offered = 0
        
        if drive_ids:
            apps = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
            total_apps = len(apps)
            total_shortlisted = sum(1 for a in apps if a.status.lower() == 'shortlisted')
            total_offered = sum(1 for a in apps if a.status.lower() == 'job offered')
            
        # Generate styled HTML report content
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Recruitment Report - {company.name}</title>
            <style>
                body {{ font-family: 'Inter', sans-serif; padding: 40px; color: #27231E; background: #ffffff; }}
                h1 {{ font-size: 24px; color: #b94a3b; border-bottom: 2px solid #b94a3b; padding-bottom: 10px; margin-top: 0; }}
                .meta {{ margin-bottom: 30px; font-size: 14px; color: #666; }}
                .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }}
                .summary-card {{ background: #fafafa; border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
                .summary-label {{ font-size: 11px; color: #888; text-transform: uppercase; font-weight: 600; }}
                .summary-value {{ font-size: 20px; font-weight: bold; color: #b94a3b; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <h1>LaunchPad Monthly Placement Report</h1>
            <div class="meta">
                <p><strong>Company Name:</strong> {company.name}</p>
                <p><strong>Reporting Period:</strong> {year}-{month:02d}</p>
                <p><strong>Report Generated On:</strong> {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <div class="summary-card">
                    <div class="summary-label">Total Drives Created</div>
                    <div class="summary-value">{total_drives}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Applications Received</div>
                    <div class="summary-value">{total_apps}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Candidates Shortlisted</div>
                    <div class="summary-value">{total_shortlisted}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Job Offers Extended</div>
                    <div class="summary-value">{total_offered}</div>
                </div>
            </div>
            <p>Report saved successfully in HTML & Mock PDF format.</p>
        </body>
        </html>
        """
        
        filename_base = f"company_{company.id}_{year}_{month:02d}"
        
        # Write HTML format
        html_path = f"static/reports/{filename_base}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
            
        # Simulate PDF format (write another copy styled for print)
        pdf_path = f"static/reports/{filename_base}.pdf"
        with open(pdf_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
            
        print(f"[REPORTS JOB] Generated Monthly Report (HTML/PDF) for {company.name} at {html_path}")
        reports_generated += 1
        
    return f"Generated monthly recruitment reports for {reports_generated} companies."

@celery.task
def export_student_applications_csv(student_id):
    """
    Asynchronous CSV export of student application history.
    """
    ensure_folders()
    student = Student.query.get(student_id)
    if not student:
        return "Student not found."
    user = student.user
    
    filename = f"student_applications_{student_id}_{int(datetime.datetime.now().timestamp())}.csv"
    filepath = f"static/exports/{filename}"
    
    apps = Application.query.filter_by(student_id=student_id).all()
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Application ID', 'Drive Title', 'Company Name', 'Applied Date', 'Current Status', 'Comment'])
        
        for app in apps:
            drive = app.drive
            company_name = drive.company.name if drive and drive.company else "N/A"
            drive_title = drive.title if drive else "N/A"
            applied_date = app.created_at.strftime('%Y-%m-%d %H:%M:%S') if app.created_at else "N/A"
            writer.writerow([app.id, drive_title, company_name, applied_date, app.status, app.comment or ''])
            
    print(f"[EXPORT JOB] Student Application History exported to {filepath}")
    print(f"[ALERT] Notification sent to {user.name} ({user.email}): Your applications CSV export is ready for download at /static/exports/{filename}")
    return filename

@celery.task
def export_company_placements_csv(company_id):
    """
    Asynchronous CSV export of company placement history.
    """
    ensure_folders()
    company = Company.query.get(company_id)
    if not company:
        return "Company not found."
        
    filename = f"company_placements_{company_id}_{int(datetime.datetime.now().timestamp())}.csv"
    filepath = f"static/exports/{filename}"
    
    drives = Drive.query.filter_by(company_id=company_id).all()
    drive_ids = [d.id for d in drives]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Application ID', 'Candidate Name', 'Candidate Email', 'Branch', 'CGPA', 'Drive Title', 'Applied Date', 'Pipeline Status'])
        
        if drive_ids:
            apps = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
            for app in apps:
                student = app.student
                student_user = student.user if student else None
                candidate_name = student_user.name if student_user else "N/A"
                candidate_email = student_user.email if student_user else "N/A"
                branch = student.branch if student else "N/A"
                cgpa = student.cgpa if student else "N/A"
                drive_title = app.drive.title if app.drive else "N/A"
                applied_date = app.created_at.strftime('%Y-%m-%d %H:%M:%S') if app.created_at else "N/A"
                writer.writerow([app.id, candidate_name, candidate_email, branch, cgpa, drive_title, applied_date, app.status])
                
    print(f"[EXPORT JOB] Company Placements History exported to {filepath}")
    print(f"[ALERT] Notification sent to {company.name} ({company.pocEmail or company.email}): Your placement CSV export is ready for download at /static/exports/{filename}")
    return filename


@celery.task
def send_single_interview_reminder(interview_id):
    """
    Asynchronous task to send an interview reminder to a student for a single interview.
    """
    interview = Interview.query.get(interview_id)
    if not interview:
        return f"Interview #{interview_id} not found."
    
    app = interview.application
    if not app:
        return "Application not found."
    student = app.student
    if not student:
        return "Student not found."
    user = student.user
    if not user:
        return "User not found."
    
    drive = app.drive
    company = drive.company if drive else None
    company_name = company.name if company else "Company"
    
    student_email = user.email
    student_name = user.name
    drive_title = drive.title if drive else "Job Posting"
    time_str = interview.scheduled_at.strftime('%Y-%m-%d %H:%M')
    
    print(f"--- SINGLE INTERVIEW REMINDER SENT ---")
    print(f"Recipient: {student_name} ({student_email})")
    print(f"Channel: Email & SMS & GChat Alert")
    print(f"Message: Dear {student_name}, this is a reminder for your upcoming interview for the drive '{drive_title}' with {company_name} on {time_str}. Mode: {interview.mode}. Location/Link: {interview.meeting_link or interview.location or 'N/A'}")
    print(f"--------------------------------------")
    return f"Reminder sent successfully for interview #{interview_id}."


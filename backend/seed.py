from datetime import datetime, timedelta

from app import app
from application.database import db
from application.models import Drive




with app.app_context():
    # Optional: Clear existing drives
    Drive.query.delete()

    drives = [
        Drive(
            company_id=1,
            title="Software Development Engineer Intern",
            description="Looking for passionate students with strong programming skills to work on backend and web development projects.",
            eligibility="CGPA >= 7.5",
            batch="2027, 2028",
            branches="CSE, AI, IT, ECE",
            deadline=datetime.now() + timedelta(days=15),
            skillsRequired="Python, Flask, SQL, Git",
            payScale="₹40,000/month",
            location="Bangalore",
            workMode="Hybrid",
            interviewRounds="OA, Technical Interview, HR Interview",
            positions=10,
        ),
        Drive(
            company_id=1,
            title="Data Science Intern",
            description="Work on ML pipelines, data preprocessing, and model deployment.",
            eligibility="CGPA >= 8.0",
            batch="2027",
            branches="CSE, AI, Data Science",
            deadline=datetime.now() + timedelta(days=20),
            skillsRequired="Python, Pandas, Scikit-learn, SQL",
            payScale="₹50,000/month",
            location="Hyderabad",
            workMode="Onsite",
            interviewRounds="Coding Test, Technical Interview",
            positions=6,
        ),
        Drive(
            company_id=1,
            title="Frontend Developer Intern",
            description="Develop modern web interfaces using Vue.js and Tailwind CSS.",
            eligibility="No Active Backlogs",
            batch="2027, 2028",
            branches="CSE, IT",
            deadline=datetime.now() + timedelta(days=10),
            skillsRequired="HTML, CSS, JavaScript, Vue.js",
            payScale="₹35,000/month",
            location="Remote",
            workMode="Remote",
            interviewRounds="Assignment, Technical Interview",
            positions=8,
        ),
        Drive(
            company_id=1,
  
            title="Backend Engineer",
            description="Build scalable REST APIs and database-driven applications.",
            eligibility="CGPA >= 7.0",
            batch="2026, 2027",
            branches="CSE, IT, AI",
            deadline=datetime.now() + timedelta(days=25),
            skillsRequired="Python, Flask, PostgreSQL, Docker",
            payScale="₹12 LPA",
            location="Pune",
            workMode="Hybrid",
            interviewRounds="OA, Technical 1, Technical 2, HR",
            positions=5,
        ),
    ]

    db.session.bulk_save_objects(drives)
    db.session.commit()

    print("Successfully seeded 4 drives.")
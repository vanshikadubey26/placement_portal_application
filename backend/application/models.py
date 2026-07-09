from .database import db
from flask_login import UserMixin
import datetime
from .utils import ist_now


class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(150), unique=True, nullable=False, index=True) 
   email = db.Column(db.String(150), unique=True, nullable=False, index=True)
   password = db.Column(db.String(150), nullable=False)
   name = db.Column(db.String(150), nullable=False)
   type = db.Column(db.String(50), default='user', nullable=False)
   isBlacklisted = db.Column(db.Boolean, default=False)
   created_at = db.Column(db.DateTime, default=ist_now)
   logo = db.Column(db.String(150), nullable=True)
   student = db.relationship('Student', backref='user', lazy=True, uselist=False)


class Student(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
   roll_number = db.Column(db.String(150), unique=True, nullable=False)
   branch = db.Column(db.String(150), nullable=False)
   year_of_study = db.Column(db.Integer, nullable=False)
   cgpa = db.Column(db.Float, nullable=False)
   resume = db.Column(db.String(300), nullable=True)
   applications = db.relationship('Application', backref='student', lazy=True, cascade="all, delete-orphan")
   created_at = db.Column(db.DateTime, default=ist_now)


class Company(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(150), unique=True, nullable=False, index=True) 
   email = db.Column(db.String(150), unique=True, nullable=False, index=True)
   password = db.Column(db.String(150), nullable=False)
   name = db.Column(db.String(150), unique=True, nullable=False)
   approved = db.Column(db.Boolean, default=False, nullable=False)
   description = db.Column(db.Text, nullable=True)
   industry = db.Column(db.String(150), nullable=True)
   scale = db.Column(db.String(150), nullable=True)
   headOffice = db.Column(db.String(150), nullable=True)
   website = db.Column(db.String(150), nullable=True)
   logo = db.Column(db.String(150), nullable=True)
   pocName = db.Column(db.String(150), nullable=True)
   pocEmail = db.Column(db.String(150), nullable=True)
   drives = db.relationship('Drive', backref='company', lazy=True)
   isBlacklisted = db.Column(db.Boolean, default=False)
   created_at = db.Column(db.DateTime, default=ist_now)


class Drive(db.Model):
   id = db.Column(db.Integer, primary_key=True, index=True)
   company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False, index=True)
   status = db.Column(db.String(50), default='Unapproved', nullable=False)
   title = db.Column(db.String(150), nullable=False)
   description = db.Column(db.Text, nullable=True)
   eligibility = db.Column(db.String(150), nullable=True)
   batch = db.Column(db.String(150), nullable=True)
   branches = db.Column(db.String(150), nullable=True)
   deadline = db.Column(db.DateTime, nullable=True)
   skillsRequired = db.Column(db.String(300), nullable=True)
   payScale = db.Column(db.String(150), nullable=True)
   location = db.Column(db.String(150), nullable=True)
   workMode = db.Column(db.String(150), nullable=True)
   interviewRounds = db.Column(db.String(150), nullable=True)
   positions = db.Column(db.Integer, nullable=True)
   applications = db.relationship('Application', backref='drive', lazy=True)
   created_at = db.Column(db.DateTime, default=ist_now)


class Application(db.Model):
   __table_args__ = (
       db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
   )
   id = db.Column(db.Integer, primary_key=True)
 
   student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False, index=True)
   drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
   status = db.Column(db.String(50), default='applied', nullable=False)
   created_at = db.Column(db.DateTime, default=ist_now)
   comment = db.Column(db.Text, nullable=True)
   updated_at = db.Column(db.DateTime, default=ist_now, onupdate=ist_now)
   interviews = db.relationship('Interview', backref='application', lazy=True, cascade="all, delete-orphan")


class Interview(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False, index=True)
   scheduled_at = db.Column(db.DateTime, nullable=False)
   mode = db.Column(db.String(50), nullable=False)
   location = db.Column(db.String(150), nullable=True)
   meeting_link = db.Column(db.String(300), nullable=True)
   created_at = db.Column(db.DateTime, default=ist_now)


#
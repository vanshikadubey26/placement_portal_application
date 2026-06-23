import os


class Config:
   SECRET_KEY = os.environ.get('SECRET_KEY', 'hbfguhiefihdliuj9eui56euijw1256a')
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ppa.sqlite3')
   SQLALCHEMY_TRACK_MODIFICATIONS = False
  
   # Manager Credentials
   ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'manager')
   ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'manager@email.com')
   ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'manager@123')
   ADMIN_NAME = os.environ.get('ADMIN_NAME', 'Vanshika')




from flask import Flask
from flask_bcrypt import Bcrypt
from application.database import db
from application.models import User, Company
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

#Settin up my flask app and configurations

app = Flask(__name__)
app.config.from_object(Config)

#CORS
CORS(app,
    origins=["http://localhost:5173"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

#Extensions
bcrypt = Bcrypt(app)
db.init_app(app)

#JWT Setup
app.config["JWT_SECRET_KEY"] = "gldslb4jhdfs7834hdscva"
jwt = JWTManager(app)

#Database Setup
with app.app_context():
   db.create_all()


   # Create default admin if not exists
   admin_user = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()


   if not admin_user:
       hashed_password = bcrypt.generate_password_hash(
           app.config['ADMIN_PASSWORD']
       ).decode('utf-8')


       admin_user = User(
           username=app.config['ADMIN_USERNAME'],
           email=app.config['ADMIN_EMAIL'],
           password=hashed_password,
           name=app.config['ADMIN_NAME'],
           type='admin'
       )


       db.session.add(admin_user)
       db.session.commit()
       print('Admin created successfully')
   else:
       print('Admin already exists')

#Run App

if __name__ == "__main__":
   app.run(debug=True, port=5555)

#Vanshika
#23f3004102

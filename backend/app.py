# Monkey-patch redis Connection to force RESP2 protocol for older Redis server compatibility
import redis.connection
original_redis_init = redis.connection.Connection.__init__
def new_redis_init(self, *args, **kwargs):
    original_redis_init(self, *args, **kwargs)
    self.protocol = 2
redis.connection.Connection.__init__ = new_redis_init

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
CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)

#Extensions
bcrypt = Bcrypt(app)
db.init_app(app)

# Celery Setup
from application.celery_app import init_celery
celery = init_celery(app)
import application.tasks


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
       # Always sync the admin password to the configured value
       if not bcrypt.check_password_hash(admin_user.password, app.config['ADMIN_PASSWORD']):
           admin_user.password = bcrypt.generate_password_hash(
               app.config['ADMIN_PASSWORD']
           ).decode('utf-8')
           db.session.commit()
           print('Admin password synced to config')
       else:
           print('Admin already exists')

# Import controllers & register blueprints
from application.controllers.system import system_bp
from application.controllers.auth import auth_bp
from application.controllers.admin import admin_bp
from application.controllers.common import common_bp
from application.controllers.company import company_bp
from application.controllers.student import student_bp

app.register_blueprint(system_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(common_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)
#Run App

if __name__ == "__main__":
   app.run(debug=True, port=5555)

#Vanshika
#23f3004102

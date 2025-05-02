from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '*^*&^*&Tufhifyiyfudiitudutidku*(^('
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:010405@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8
app.config['COMMENT_SIZE'] = 20

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name="dq9uzlkor",
    api_key="665584773648615",
    api_secret="skShHU4wUpk0Sqysv18oD4G1uZU",
    secure=True
)

login = LoginManager(app=app)

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
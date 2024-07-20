from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)
    temp = db.Column(db.Float)
    humid = db.Column(db.Float)
    co2 = db.Column(db.Float)
    voc = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
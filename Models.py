from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Fault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    symptoms = db.Column(db.JSON, nullable=False)  # {"engine_cranks": True, ...}
    repair_steps = db.Column(db.Text)
    difficulty = db.Column(db.String(20))
    cost_estimate = db.Column(db.String(50))
    diagram = db.Column(db.String(100))  # Filename in static/diagrams/

class RepairLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fault_id = db.Column(db.Integer, db.ForeignKey('fault.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
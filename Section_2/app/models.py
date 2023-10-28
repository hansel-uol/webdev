from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500), index=True, unique=True)
    start_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    rent = db.Column(db.Float)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=True)
    amount = db.Column(db.Float)

class Expenditure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=True)
    amount = db.Column(db.Float)
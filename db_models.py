from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import cfg

app = Flask(__name__)
# FORMAT: dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = f"{cfg['DB_DIALECT']}://{cfg['DB_USERNAME']}:{cfg['DB_PASSWORD']}@{cfg['DB_HOST']}:{cfg['DB_PORT']}/{cfg['DB_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Province(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    districts = db.relationship('District', backref='province')

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    province_id = db.Column(db.Integer, db.ForeignKey('province.id'))
    sectors = db.relationship('Sector', backref='district')
    
class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    cells = db.relationship('Cell', backref='sector')
    
class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    villages = db.relationship('Village', backref='cell')
    
class Village(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))
    patients = db.relationship('Patient', backref='village')
    
class Health_center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    location = db.Column(db.String(100))
    patients = db.relationship('Patient', backref='health_center')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.String(200))
    village_id = db.Column(db.Integer, db.ForeignKey('village.id'))
    health_center_id = db.Column(db.Integer, db.ForeignKey('health_center.id'))
    blood_tests = db.relationship('Blood_test', backref='patient')
    
class Blood_test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    image = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    malaria_results = db.relationship('Malaria_results', backref='blood_test')
    
class Malaria_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    malaria_status = db.Column(db.String(200))
    parasite_type = db.Column(db.String(200))
    blood_test_id = db.Column(db.Integer, db.ForeignKey('blood_test.id'))
    
class Case_cache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    name = db.Column(db.String(200))
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.String(200))
    village_id = db.Column(db.Integer, db.ForeignKey('village.id'))
    health_center_id = db.Column(db.Integer, db.ForeignKey('health_center.id'))
    malaria_status = db.Column(db.String(200))
    parasite_type = db.Column(db.String(200))
    blood_test_id = db.Column(db.Integer, db.ForeignKey('blood_test.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    country = db.Column(db.String(200))
    institution = db.Column(db.String(200))
    position = db.Column(db.String(200))
    national_id = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    role = db.Column(db.String(200))
    health_center_id = db.Column(db.Integer, db.ForeignKey('health_center.id'))



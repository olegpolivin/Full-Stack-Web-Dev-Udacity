from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "EducationOnlineDB"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Course
'''
class Course(db.Model):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    course = Column(String)
    domain = Column(Integer, db.ForeignKey('domain.id', ondelete = 'CASCADE'), nullable=False)
    platform = Column(Integer, db.ForeignKey('platform.id', ondelete = 'CASCADE'), nullable=False)
    website = Column(String)
    price_per_month = Column(Integer)
    duration_months = Column(Integer)
    university = Column(Integer, db.ForeignKey('university.id', ondelete = 'CASCADE'), nullable=False)
    
    def __init__(self,
                course,
                domain,
                platform,
                website,
                price_per_month,
                duration_months,
                university):
        self.course = course
        self.domain = domain
        self.platform = platform
        self.website = website
        self.price_per_month = price_per_month
        self.duration_months = duration_months
        self.university = university

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'course': self.course,
            'domain': self.domain,
            'platform': self.platform,
            'website': self.website,
            'price_per_month': self.price_per_month,
            'duration_months': self.duration_months,
            'university': self.university
        }

'''
Platforms
'''
class Platform(db.Model):
    __tablename__ = 'platform'

    id = Column(Integer, primary_key=True)
    platform = db.relationship('course', backref='platform', lazy=True, cascade="all, delete")
    
    def __init__(self, platform):
        self.platform = platform

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'platform': self.platform
        }

'''
Universities
'''
class University(db.Model):
    __tablename__ = 'university'

    id = Column(Integer, primary_key=True)
    university = db.relationship('course', backref='university', lazy=True, cascade="all, delete")
    
    def __init__(self, university):
        self.university = university

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'university': self.university
        }

'''
Domains
'''
class Domain(db.Model):
    __tablename__ = 'domain'

    id = Column(Integer, primary_key=True)
    domain = db.relationship('domain', backref='domain', lazy=True, cascade="all, delete")
    
    def __init__(self, domain):
        self.university = domain

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'domain': self.domain
        }

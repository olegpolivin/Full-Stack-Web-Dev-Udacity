from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "EducationOnlineDB"
database_path = "postgres:///{}".format(database_name)

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
    course_name = Column(String)
    domain_id = Column(Integer, db.ForeignKey('domain.id', ondelete = 'CASCADE'), nullable=False)
    platform_id = Column(Integer, db.ForeignKey('platform.id', ondelete = 'CASCADE'), nullable=False)
    website = Column(String)
    price_per_month = Column(Integer)
    duration_months = Column(Integer)

    def __init__(self,
                course_name,
                domain_id,
                platform_id,
                website,
                price_per_month,
                duration_months):
        self.course_name = course_name
        self.domain_id = domain_id
        self.platform_id = platform_id
        self.website = website
        self.price_per_month = price_per_month
        self.duration_months = duration_months

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
            'course_name': self.course_name,
            'domain_id': self.domain_id,
            'platform_id': self.platform_id,
            'website': self.website,
            'price_per_month': self.price_per_month,
            'duration_months': self.duration_months
        }

'''
Platforms
'''
class Platform(db.Model):
    __tablename__ = 'platform'

    id = Column(Integer, primary_key=True)
    course = db.relationship('Course', backref='platform', lazy=True, cascade="all, delete")
    platform_name = Column(String)
    
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
            'platform_name': self.platform_name
        }

'''
Domains
'''
class Domain(db.Model):
    __tablename__ = 'domain'

    id = Column(Integer, primary_key=True)
    course = db.relationship('Course', backref='domain', lazy=True, cascade="all, delete")
    domain_name = Column(String)
    
    def __init__(self, domain_name):
        self.domain_name = domain_name

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
            'domain_name': self.domain_name
        }

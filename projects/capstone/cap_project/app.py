import os
from flask import Flask, request, abort, jsonify
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Course, Platform, University, Domain

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/courses')
  def get_courses():
    print(Course)
    courses = Course.query.all()
    courses = [course.format() for course in courses]
    print(courses)
    return jsonify({
      'success': True,
      'courses': courses,
      'total_courses': len(courses)
      })

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
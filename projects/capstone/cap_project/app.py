from auth.auth import AuthError, requires_auth
from flask import Flask, abort, jsonify, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Course, Platform, Domain
import os

COURSES_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def about_application():
    response = jsonify ({
      'success': True
      })
    return render_template('html/index.html', results=response)

  #----------------------------------------------------------------------------#
  # Endpoints for courses
  #----------------------------------------------------------------------------#

  @app.route('/courses')
  def get_courses():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * COURSES_PER_PAGE
    end = start + COURSES_PER_PAGE

    courses = Course.query.all()
    courses_formatted = [course.format() for course in courses]

    if not len(courses_formatted[start:end]):
      abort(404)

    return jsonify({
      'success': True,
      'courses': courses_formatted,
      'total_courses': len(courses_formatted)
      })

  @app.route('/courses', methods=['POST'])
  @requires_auth('post:new_course')
  def add_course(permission):
    body = request.get_json()
    try:
      course = Course(
        body['course_name'],
        body['domain_id'],
        body['platform_id'],
        body['website'],
        body['price_per_month'],
        body['duration_months'])
      course.insert()

      return jsonify({
        'success': True, 
        'course_id': course.id
      })
    except:
      abort(422)

  @app.route('/courses/<int:course_id>', methods=['DELETE'])
  @requires_auth('delete:course')
  def delete_course(permission, course_id):
    course = Course.query.filter_by(id=course_id).one_or_none()
    if course is None:
      abort(404)
    else:
      course.delete()
      return jsonify({
        'success': True,
        'course_id': course_id})

  #----------------------------------------------------------------------------#
  # Endpoints for domains
  #----------------------------------------------------------------------------#

  @app.route('/domains')
  def get_domains():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 5
    end = start + 5

    domains = Domain.query.all()
    domains_formatted = [domain.format() for domain in domains]

    if not len(domains_formatted[start:end]):
      abort(404)

    return jsonify({
      'success': True,
      'domains': domains_formatted,
      'total_domains': len(domains_formatted)
      })

  @app.route('/domains', methods=['POST'])
  @requires_auth('post:new_domain')
  def add_domain(permission):
    body = request.get_json()
    try:
      domain = Domain(body['domain_name'])
      domain.insert()
      return jsonify({
        'success': True, 
        'domain_id': domain.id
      })
    except:
      abort(422)

  @app.route('/domains/<int:domain_id>', methods=['PATCH'])
  @requires_auth('patch:domain')
  def patch_domain(permission, domain_id):
    domain = Domain.query.filter_by(id=domain_id).one_or_none()
    if domain is None:
      abort(404)
    
    body = request.get_json()
    try:
      domain.domain_name = body['domain_name']
      domain.update()
      return jsonify({
        'success': True, 
        'domain_id': domain_id,
        'new_name': domain.domain_name
      })
    except:
      abort(422)

  @app.route('/domains/<int:domain_id>', methods=['DELETE'])
  @requires_auth('delete:domain')
  def delete_domain(permission, domain_id):
    domain = Domain.query.filter_by(id=domain_id).one_or_none()
    if domain is None:
      abort(404)
    else:
      domain.delete()
      return jsonify({
        'success': True,
        'domain_id': domain_id})

  @app.route('/domains/<int:domain_id>/courses', methods=['GET'])
  def get_courses_for_domain(domain_id):
    courses = Course.query.filter_by(domain_id=domain_id).all()
    if not courses:
      abort(404)
    else:
      courses_formatted = [course.format() for course in courses]
    return jsonify({
      'success': True,
      'courses_for_domain': courses_formatted,
      })

  #----------------------------------------------------------------------------#
  # Endpoints for platforms
  #----------------------------------------------------------------------------#
  # I decided not to create GET, POST, PATCH and DELETE methods for platforms
  # because they would exactly repeat that for domains. Since it does not bring
  # knowledge added, I just use a predefined list of platforms:
  # id 1: Coursera
  # id 2: Udacity
  # id 3: Udemy
  # id 4: Other

  #----------------------------------------------------------------------------#
  # Error handlers
  #----------------------------------------------------------------------------#

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "The request was well-formed but was unable to be followed due to semantic errors."
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "It's not you, it's us"
        }), 500

  @app.errorhandler(AuthError)
  def autherror(AuthError):
      return jsonify({
          "success": False, 
          "error": AuthError.status_code,
          "message": AuthError.error
          }), 401

  return app

APP = create_app()

if __name__ == '__main__':
  # port = int(os.environ.get('PORT'), 5050)
  APP.run(host='0.0.0.0', port=8080, debug=True)

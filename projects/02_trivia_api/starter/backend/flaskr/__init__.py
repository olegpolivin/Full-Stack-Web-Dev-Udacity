import os
from flask import Flask, flash, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    if not len(categories):
      abort(404)

    formatted_categories = {category.id: category.type for category in categories}
    return jsonify({
      'success': True, 
      'categories': formatted_categories
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    
    if not len(formatted_questions[start:end]):
      abort(404)

    categories = Category.query.order_by(Category.type).all()
    formatted_categories = {category.id: category.type for category in categories}
    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'total_questions': len(formatted_questions),
      'categories': formatted_categories
      })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()
    if question is None:
      abort(404)
    else:
      question.delete()
      return jsonify({
        'success': True,
        'question_id': question_id
        })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()
    if body.get('searchTerm'):
      return search_question()
    try:
      q = Question(
        body['question'],
        body['answer'],
        body['category'],
        body['difficulty']
        )
      q.insert()
      return jsonify({
        'success': True, 
        'id': q.id
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_question():
    body = request.get_json()
    searchTerm = body['searchTerm'].lower()
    try:
      questions = Question.query.filter(Question.question.ilike("%{}%".format(searchTerm))).all()
      questions = [q.format() for q in questions]
      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions)
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category_id(category_id):
    category_questions = Question.query.filter_by(category=category_id).all()
    if not category_questions:
      abort(404)
    else:
      category_questions = [q.format() for q in category_questions]
    return jsonify({
      'success': True, 
      'questions': category_questions,
      'total_questions': len(category_questions)
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    category_id = request.get_json()['quiz_category']['id']
    previous_questions = request.get_json()['previous_questions']
    if category_id == 0:
      questions_to_ask = Question.query.filter(~Question.id.in_(previous_questions)).all()
    else:
      questions_to_ask = Question.query.filter_by(category=category_id). \
        filter(~Question.id.in_(previous_questions)).all()

    if not questions_to_ask:
      return jsonify({
        'previousQuestions': previous_questions,
        'question': None
      })

    currentQuestion = random.choice(questions_to_ask).format()
    return jsonify({
        'previousQuestions': currentQuestion['id'],
        'question': currentQuestion
      })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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
      "message": "unprocessable"
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "It's not you, it's us"
        }), 500

  return app

    
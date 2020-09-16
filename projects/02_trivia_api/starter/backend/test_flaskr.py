import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.add_question = {
            'question': 'Do cats like milky way?',
            'answer': 'Kind of',
            'category': 1,
            'difficulty': 4
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # testing @app.route('/categories')
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    
    # testing @app.route('/questions')
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_page_does_not_exist(self):
        res = self.client().get('/questions?page=42')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not found")

    # testing @app.route('/questions/<int:question_id>', methods=['DELETE'])
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/2')
    #     data = json.loads(res.data)
    #     deleted_question = Question.query.filter_by(id=2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['question_id'], 2)
    #     self.assertIsNone(deleted_question)
    
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/2020')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    # testing @app.route('/questions', methods=['POST']) for adding questions
    def test_adding_a_question(self):

        len_before_add = len(Question.query.all())
        res = self.client().post('/questions', json=self.add_question)
        data = json.loads(res.data)
        len_after_add = len(Question.query.all())
        diff = len_after_add - len_before_add

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(diff, 1)
    
    def test_posting_incomplete_model_question(self):
        res = self.client().post('/questions', json = {
            'answer': 'Kind of',
            'category': 1,
            'difficulty': 4
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    # testing @app.route('/questions', methods=['POST']) for search

    # testing @app.route('/categories/<int:category_id>/questions')

    # testing @app.route('/quizzes', methods=['POST'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
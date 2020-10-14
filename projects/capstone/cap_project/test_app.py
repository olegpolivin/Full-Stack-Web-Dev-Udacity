import json
import os
import unittest

from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Course, Domain, Platform

# Students can consult courses and domains
# Platforms can add courses and domains, patch domains
# Administrators can do any request + delete domains and courses

ENV_student_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4MzY2OGE4ZDI1YTIwMDc1YzhhOTNhIiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAyNjU0NDY1LCJleHAiOjE2MDI3NDA4NjUsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.DnyJPDKJL6mfoptQMc6Tuv0QIJdS1k0JzwN9dldvXNOZrg11iOk6FMcvRjGyGw_DC5ZA1jAGyeALbq4GGLiF6OiTFFmxYaZn6_PXmF-nvtJ91LTeZFw2XaC4id1M53-SmUDohK7KNFWHmJIK7KTYVX3G7W_mHKMfoBGWlJnmPUyNWT3EW4X2wk45DGwxNrcQucBXqbdKNlBgmctpUzZfFzMyK7_NKqdOmcmmSwebpGkSr3fSWYBa55Z0i1Ln44RBpyKczsYyb4kzfR1Wxx-xBTyEAE8we38sarN7yOVJ41DxxeqESLo_wW4fRCroqb1LKADp_OWn7HApIVxo-baSpA'
ENV_platform_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4MzcxZDg4ZDI1YTIwMDc1YzhjNzJmIiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAyNjU2NjQzLCJleHAiOjE2MDI3NDMwNDMsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJwYXRjaDpkb21haW4iLCJwb3N0Om5ld19jb3Vyc2UiLCJwb3N0Om5ld19kb21haW4iXX0.KB1R_E2BthRh8SIEClRa50VfGG3ax_Qi_QTTk8DsuAJGpzHoEXWSGUywZhwLESXFTVqWYzwPBHtB1rhAvpznPz2odawOecUmlFK8b7ogja0-wqQ-pp4xfhpi1BWSLxDVkG2z4nbjOtwxgXtKAurd9otDAETGggsyoWjoA9yp76WHhDgkn4MZpr1UzwkVVIwg6qrgWMjWJCUgDpaYnQXykmhxDBAIWZ-O7uYzwgJuNTkewUS5QJ-al07D60qrQ0kB4Ljp1kOGstCJl29S8s3DIjlJnbGv0ZDSMh2HMJvBc6xg3eUz-vu80qfMUjtdi4xUKkqm7FQCyi4PvRUXgAGs1A'
ENV_admin_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4NGFmNDg4MTAyZjcwMDc2NTgzNmM2IiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAyNjU0NTkyLCJleHAiOjE2MDI3NDA5OTIsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y291cnNlIiwiZGVsZXRlOmRvbWFpbiIsInBhdGNoOmRvbWFpbiIsInBvc3Q6bmV3X2NvdXJzZSIsInBvc3Q6bmV3X2RvbWFpbiJdfQ.JGso6laX5bxy5ZSSDD569OG1fZR7g5oQQKBlcUBkS11Y0T1Qpy0CAVH4iEAezRuApd-VjR866vLIdmiNo50OSsAPkIBp5NOJlvk0GOhLpEAyefx4Wu_WSo287aZW8xFHgI_p40y4d7jYNULaH6-Tv_hwf7DiMI6o1Kx9CeLNtSCCr0JqFLeSWDPmeL_RF1ARoOjUJtBATi682-sGcGprCAWiB8u5oa4zL7AHAkMDz3NCoaB6NP39t3_Qtm6yNtFVx6S8eBJht95RlkDIHZnfe9nwuX4KqJC9KPSVnUZ9J4soZvoXUVbq6yiTIrF83RynUPEoTwn5GAjmMSP44n8nog'


class OnlineEducationTestCase(unittest.TestCase):
    """Class to test endpoints of the App
    """
    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "EducationOnlineDBTest"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.add_course = {
            "course_name": "Learn everything in 2 hours",
            "domain_id": 1,
            "platform_id": 2,
            "website": "www.learneverything.com",
            "price_per_month": 1000,
            "duration_months": 1
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    # ---------------
    # Testing courses
    # ---------------

    # testing @app.route('/courses')
    def test_get_courses(self):
        res = self.client().get('/courses')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['courses']))

    def test_404_page_does_not_exist(self):
        res = self.client().get('/courses?page=42')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not found")

    # testing @app.route('/courses', methods=['POST']) for adding courses
    # when permissions are absent or not sufficient
    def test_post_courses_no_token(self):
        res = self.client().post('/courses', json=self.add_course)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No authorization header')

    def test_post_courses_no_permission(self):
        # Incorrect token permissions to do that
        res = self.client().post('/courses',
                                 json=self.add_course,
                                 headers={'Authorization': ENV_student_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You do not have the permission to perform that action')

    def test_post_and_delete_courses_with_enough_permissions(self):
        # Notice that adding course is done by platform,
        # deleting is done by administrator
        res = self.client().post('/courses',
                                 json=self.add_course,
                                 headers={'Authorization': ENV_platform_token})
        data = json.loads(res.data)
        id_to_delete = data['course_id']

        # First we check successful insert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().delete('/courses/'+str(id_to_delete),
                                    headers={'Authorization': ENV_admin_token})
        data = json.loads(res.data)
        deleted_course = Course.query.filter_by(id=id_to_delete).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['course_id'], id_to_delete)
        self.assertIsNone(deleted_course)

    def test_delete_courses_without_enough_permissions(self):

        res = self.client().delete('/courses/'+str(1),
                                    headers={'Authorization': ENV_platform_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'You do not have the permission to perform that action')

    # ---------------
    # Testing domains
    # ---------------

    # testing @app.route('/domains')
    def test_get_domains(self):
        res = self.client().get('/domains')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['domains']))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

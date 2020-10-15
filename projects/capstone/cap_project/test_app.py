import json
import os
import unittest

from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Course, Domain, Platform

# Students can consult courses and domains
# Platforms can add courses and domains, patch domains
# Administrators can do any request + delete domains and courses

ENV_student_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4MzY2OGE4ZDI1YTIwMDc1YzhhOTNhIiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAyNzQ2NjkzLCJleHAiOjE2MDI4MzMwOTMsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.h90QO3nXWocV9zKhzK0OVccAAAQO_cUSgyMdD845RkRlSbajat-mGAd-FV1mHY6RjO4A83-c84rOXdmlsbhgZzg6A3D31Vh4Bl4mjeBxbeXASYwe_pd0sxos2EuGGm84Ga7VB44sW4xdHEJuQqonB4AMhziT3UXSMpPLEmmhSdCVsJjYOI2i4uDemsU5mef8YyfDJpl6tcr4PNQjKakLhjKI8onkCXvbY1hbiDpTLy5yMSWCLQLJh2D0a4Awl1kWTs9kn0Kc89DBz2cSA8gcDVgTnG5LOr51ItT-yl7Wt0Smhi6DeLfJbrEqOEHnvdFaYZImUrVUEevNYO0EYaUxCw'
ENV_platform_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4MzcxZDg4ZDI1YTIwMDc1YzhjNzJmIiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAyNzQ2NzQxLCJleHAiOjE2MDI4MzMxNDEsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJwYXRjaDpkb21haW4iLCJwb3N0Om5ld19jb3Vyc2UiLCJwb3N0Om5ld19kb21haW4iXX0.mZ41Av2ad8MQYV_kK2cTJt08Bt5jcfIlumU1m5ZfL79Fkh5x7sSd-0XMaOtwa70UWZijVbN87FEQURffNL00pPeD7Z7q7qPwB6R6jzUUyXDyOKrzj91bBUDbwAcd4j_kDQRoGJo_4uAzd_1HVNsHqByMv-pzGudp1fVKjf9QxgTjIeoTzSeFcRTHV3MkjUYDYxTzHf06TrusgqWv3IP9TroEclVZX-sdQhW_dj1d2Kia9PyoU_WKHVQRGkk09-DnySVEYldz2j2a2ha4vJ_AMqw_aatmWTPVs_1n-OvozEu6wdOCcJW_oKOJ8sWjFyMJqPWxj-4YgDNrK3aP5uHyWQ'
ENV_admin_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhBOFoxNG9kLUFUbVNPWFRMY1VmXyJ9.eyJpc3MiOiJodHRwczovL29ubGluZWVkdWNhdGlvbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4NGFmNDg4MTAyZjcwMDc2NTgzNmM2IiwiYXVkIjoiQ291cnNlQW5kRG9tYWluIiwiaWF0IjoxNjAyNzQ2Nzc3LCJleHAiOjE2MDI4MzMxNzcsImF6cCI6InRFZXBtbjVKNkxtMmpJak5EUTJNbTE1R05oOXNHNXgwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y291cnNlIiwiZGVsZXRlOmRvbWFpbiIsInBhdGNoOmRvbWFpbiIsInBvc3Q6bmV3X2NvdXJzZSIsInBvc3Q6bmV3X2RvbWFpbiJdfQ.bvCEU6RI6Ow-NnFnPmYa_sG7Ov6dt8HEMMQGYZxnhSqRt8ty9tzwLXEQ817rDnDhZAbBD6OKXZuZCUA_XE95qe41nEr8jgAckfC9VmPsj2dx6fySXJ1eXtgtIu0bQgfVqiEqttTHsFcVMrmO21hCa6Ta7Xhj-HBVrf9Rr_xmyKTsjDmigao7-8OeHKjVvqTvuqgN9l_JVXrpCiJw81f6ZwqxAhThdYx8HKbOGsHbaIycmBu2K3puriFpA9qWOHRjQv99OK_sbiUrW3OJYDbvNQKdhbinV8puwpeIid5T267423znIdXXTEq6xIBBUcqrA-f6RktEfOmj_vAYhrcRsg'


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

        self.add_domain = {
            "domain_name": "Physics",
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

    def test_404_page_does_not_exist(self):
        res = self.client().get('/domains?page=42')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not found")

    # testing @app.route('/domains/<int:domain_id>/courses')
    def test_get_courses_for_given_domain(self):
        res = self.client().get('/domains/1/courses')
        data = json.loads(res.data)
        courses_for_domain = Course.query.filter_by(domain_id=1).all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['courses_for_domain']), len(courses_for_domain))

    def test_404_domain_does_not_exist(self):
        res = self.client().get('/domains/10/courses')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not found")

    # testing @app.route('/domains', methods=['POST'])
    # testing @app.route('/domains', methods=['DELETE'])
    def test_post_and_delete_domains_with_enough_permissions(self):
        # Notice that adding a domain is done by platform,
        # deleting is done by administrator
        res = self.client().post('/domains',
                                 json=self.add_domain,
                                 headers={'Authorization': ENV_platform_token})
        data = json.loads(res.data)
        id_to_delete = data['domain_id']

        # First we check successful insert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().delete('/domains/'+str(id_to_delete),
                                    headers={'Authorization': ENV_admin_token})
        data = json.loads(res.data)
        deleted_domain = Domain.query.filter_by(id=id_to_delete).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(deleted_domain)
    
    def test_delete_domain_without_sufficient_permissions(self):
        res = self.client().delete('/domains/1',
                                    headers={'Authorization': ENV_student_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'You do not have the permission to perform that action')

    # testing @app.route('/domains/<int:domain_id>', methods=['PATCH'])
    def test_patch_domain(self):

        # First I add domain
        res = self.client().post('/domains',
                                 json=self.add_domain,
                                 headers={'Authorization': ENV_platform_token})
        data = json.loads(res.data)
        id_to_patch = data['domain_id']

        # Check successful insert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Patch
        len_data_before_patch = len(Domain.query.all())

        new_domain_name = 'Chemistry'
        res = self.client().patch('/domains/' + str(id_to_patch),
                                  headers={'Authorization': ENV_platform_token},
                                  json={'domain_name': new_domain_name})
        data = json.loads(res.data)
        len_data_after_patch = len(Domain.query.all())

        # Check the patch
        domain = Domain.query.filter_by(domain_name="Chemistry").one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(domain.id, data['domain_id'])
        self.assertEqual(len_data_before_patch, len_data_after_patch)

        # Finally delete the patched id
        res = self.client().delete('/domains/'+str(id_to_patch),
                                    headers={'Authorization': ENV_admin_token})
        data = json.loads(res.data)
        deleted_domain = Domain.query.filter_by(id=id_to_patch).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(deleted_domain)

    def test_patch_with_insufficient_permissions(self):
        new_domain_name = 'Babaka'
        res = self.client().patch('/domains/1',
                                headers={'Authorization': ENV_student_token},
                                json={'domain_name': new_domain_name})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'You do not have the permission to perform that action')

    def test_404_patching_non_existant_domain(self):
        new_domain_name = 'Babaka'
        res = self.client().patch('/domains/20',
                                headers={'Authorization': ENV_admin_token},
                                json={'domain_name': new_domain_name})
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not found")

    def test_422_patching_but_incorrect_request(self):
        new_domain_name = 'Babaka'
        res = self.client().patch('/domains/1',
                                headers={'Authorization': ENV_admin_token},
                                json={'here_is_the_error': new_domain_name})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "The request was well-formed but was unable to be followed due to semantic errors.")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

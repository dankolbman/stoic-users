import json
import unittest
from datetime import datetime

from flask import current_app, url_for
from users import create_app, db
from users.model import User

from test.utils import make_user, api_headers


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_new_user(self):
        """
        Test user creation via REST API
        """
        json_resp = make_user(self.client)
        # check api response
        self.assertEqual(json_resp['status'], 'user registered')
        self.assertEqual(json_resp['username'], 'Dan')
        # check that user is in database
        self.assertEqual(User.query.count(), 1)

        # check malformed query
        resp = self.client.post('/user/',
                                headers=api_headers(),
                                data=json.dumps({'username': 'Dan'}))
        json_resp = json.loads(resp.data.decode('utf-8'))
        # check api response
        self.assertEqual(resp.status, '400 BAD REQUEST')
        self.assertEqual(json_resp['status'], 'missing fields')
        self.assertEqual(json_resp['missing'], ['email', 'password'])

"""
Test cases for the API. In these test cases, we verify that the
API responds correctly to calls of all endpoints.
BLACKBOX TESTING:

    def test_api_builds():
    def test_api_builds_bad():
    def test_api_builds_loop():
    def test_api_pings():
    def test_api_build_status():
    def test_api_build_status_wrong_id():
    def test_api_build_statuses():
    def test_api_accepts_settings_changes():
    def test_api_denies_bad_settings():
    def test_api_blame_list():
    def test_api_rebuilds():

WHITEBOX TESTING:

    Since the API is reaching deeper into the server to do any excecution
    and is not doing any of the lifting itself, there is no logic to white
    box test. We need to be sure that the appropriate piece of data is returned
    or that the correct internal method is triggered, but do not need to examine
    them here.
"""


import unittest
import json
from rosie.models import (
    Build,
    connection
)

class APITest(unittest.TestCase):
    """Test cases for API"""
    @classmethod
    def setUpClass(self):
        """ Create clean instance of DB"""
        self.fake_json = {
            'repository': {
                'url': 'https://github.com/cs181f/rosie',
                'name': 'rosie',
                'description': 'a lightweight CLI server',
                'owner': {
                    'name': 'test_user',
                    'email': 'test@example.com'
                }
            },
            'url': 'https://github.com/cs181f/rosie/commit/faea04357ef207d8f9f5c6a04607c7a53d8dc770',
            'author': {
                'email': 'dunvi.dunvi@gmail.com',
                'name': 'dunvi' },
            'message': 'updating with changes from design review',
            'timestamp': '2012-12-15T20:05:07-08:00',
            'ref': "refs/heads/master",
            'status': 2,
            'error': ''
        }
        self.json = json.dumps(self.fake_json)

    def setUp(self):
        """ Create build objects to test with"""

    def tearDown(self):
        """ Remove all objects from DB and remove it """

    def test_api_builds(self):
        """ Verifies that a good build builds without error """

        build = connection.Build(self.json)
        print build
        id = build.save()
        print id

    def test_api_builds_bad(self):
        """ Verifies that a bad build returns an error and posts the error to
        GitHub """

    def test_api_builds_loop(self):
        """ Verifies that a bad build with an infinite loop times out after the
        hang time in test_settings """

    def test_api_pings(self):
        """ Verifies that it returns true when building and false when free """

    def test_api_build_status(self):
        """ Verifies that when a build is running, returns the status of that
        build and otherwise returns clear."""

    def test_api_build_status_wrong_id(self):
        """ Verifies that an error is returned if an invalid ID is passed to
        the build_status endpoint """

    def test_api_build_statuses(self):
        """ Verifies that build statuses returned match initial set."""

    def test_api_accepts_settings_changes(self):
        """ Verifies that test_settings file is changed"""

    def test_api_denies_bad_settings(self):
        """ Verifies that test_settings file is not changed if settings are
        malformed or incorrect """

    def test_api_blame_list(self):
        """ Verifies that the data returned is the same as data stored"""

    def test_api_rebuilds(self):
        """ Verifies that after adding a failing test, build that passed build()
        now fails."""



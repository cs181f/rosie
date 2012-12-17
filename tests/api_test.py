"""
Test cases for the API. In these test cases, we verify that the
API responds correctly to calls of all endpoints.
BLACKBOX TESTING:

    def test_api_builds():
    def test_api_builds_bad():
    def test_api_pings():
    def test_api_build_id_returns_corrent_information():
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

import flaskext.testing as testing
import unittest
import json
from rosie.api import api
from rosie.models import (
    Build,
    WorkerThread,
    connection
)
from mock import patch
from mongokit import ObjectId

Build = connection.Build

class APITest(testing.TestCase):
    """Test cases for API"""

    def create_app(self):
        return api

    @classmethod
    def setUpClass(self):
        """ Create clean instance of DB"""
        self.fake_json = {'payload': {
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
            'ref': "refs/heads/master"
        } }
        self.json = json.dumps(self.fake_json)

    def setUp(self):
        """ Create build objects to test with"""

    def tearDown(self):
        """ Remove all objects from DB and remove it """
        connection.Build.collection.remove()

    def test_api_builds(self):
        """ Verifies that a good build builds without error """

        response = self.client.post(
           '/build',
            data=self.json,
            content_type='application/json'
        )

        api.worker.join()

        build = Build.find_one(dict(_id=ObjectId(response.json['id'])))

        self.assertEqual(build['status'],1)

    @patch.object(WorkerThread, '_bash_build')
    def test_api_builds_bad(self, mock):
        """ Verifies that a bad build returns an error and posts the error to
        GitHub """

        mock.return_value = "This is an error"

        response = self.client.post(
            '/build',
            data=self.json,
            content_type='application/json'
        )

        api.worker.join()

        build = Build.find_one(dict(_id=ObjectId(response.json['id'])))

        self.assertEqual(build.status ,2)
        mock.assert_called_once()


    @patch.object(WorkerThread, 'is_building')
    def test_api_pings(self, mock):
        """ Verifies that it returns true when building and false when free """

        mock.return_value = True

        response = self.client.get('/ping',)

        self.assertTrue(response.json['building'])

    def test_api_build_id_returns_corrent_information(self):
        """ Verifies that when a build is running, returns the status of that
        build and otherwise returns clear."""

        build = Build()
        build.save()

        response = self.client.get('/builds/%s' % str(build._id))

        self.assertEqual(build._id, ObjectId(response.json['_id']['$oid']))

    def test_api_build_status_wrong_id(self):
        """ Verifies that an error is returned if an invalid ID is passed to
        the build_status endpoint """


        build = Build()
        build.save()

        response = self.client.get('/builds/%s' % '1234')

        self.assertEqual(response.json['error'], 'Invalid Build ID')

    def test_api_builds_returned_corrent(self):
        """ Verifies that build statuses returned match initial set."""

        builds = []
        for i in range(5):
            build = Build()
            build.save()
            builds.append(str(build._id))

        response = self.client.get('/builds')

        self.assertEqual(len(response.json), 5)

        for b in response.json:
            self.assertTrue(builds.count(json.loads(b)['_id']['$oid']) == 1)

    def test_api_blame_list(self):
        """ Verifies that the data returned is the same as data stored"""

        for i in range(15):
            build = Build()
            build.status = 2
            if i < 5:
                build.author.name = 'jessepollak'
            elif i < 10:
                build.author.name = 'dunvi'
            else:
                build.author.name = 'brennenbyrne'

            build.save()

        response = self.client.get('/blame')

        self.assertEqual(response.json['brennenbyrne'], 5)
        self.assertEqual(response.json['jessepollak'], 5)
        self.assertEqual(response.json['dunvi'], 5)

    def test_api_rebuilds(self):
        """ Verifies that after adding a failing test, build that passed build()
        now fails."""

        build = Build()
        build.status = 2
        build.save()

        response = self.client.post('/builds/new', data=dict(build_id=str(build._id)))

        api.worker.join()

        build.reload()

        self.assertEqual(build.status, 1)
        self.assertTrue(api.worker.current_build is None)
        self.assertEqual(response.json['id'], str(build._id))

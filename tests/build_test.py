"""
Test cases for the Build class. Since the Build object
is just an extension of mongokit's Document class and
implements very little on its own, we only need the
following tests:

    def test_empty_build_creation
    def test_build_from_good_json
    def test_build_from_bad_json
    def test_build_insertion
    def test_failed_build_retrieval
    def test_build_retrieval
    def test_multiple_build_retrieval
    def test_update_existing_build

"""

import unittest
import json
from mongokit import Connection
from rosie.models import (
    Build,
    connection
)


class BuildTest(unittest.TestCase):
    """Test cases for Worker Thread"""
    @classmethod
    def setUpClass(self):
        """ Nothing needs to be set up for the whole class.
            The database is set up in the Build class,
            and the connection is embedded in the objects. """

    def setUp(self):
        """ need to set this up? """
        self.connection = connection
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

    def tearDown(self):
        """ Nothing needs to be torn down """

    def test_empty_build_creation(self):
        """ Tests that a new build is created correctly """
        empty_build = Build()

    def test_build_from_good_json(self):
        """ Tests that sample JSON results in a valid Build object that is
            correctly inserted into the database """
        # this is a fake build
        # it doesn't actually point to anything useful :P
        json_build = self.connection.Build(json=self.json)
        # note that validate, embedded in the constructor,
        # will raise exceptions if this is wrong
        # otherwise validate does nothing

    def test_build_from_bad_json(self):
        """ Tests that bad JSON results in a reasonable response
            checks for: reasonable errors """
        json_build = self.connection.Build(json={'fake':'haha'})
        # validate() should fail miserably here

    def test_build_insertion(self):
        """ Tests that a build is successfully inserted """
        test_build = self.connection.Build(json=self.json)
        test_build.save()
        self.assertEqual(self.db.count(), 1)

    def test_failed_build_retrieval(self):
        """ Tests that bad retrieves fail reasonably
            checks for:
                reasonable error given invalid ID
                reasonable errors for database errors """
        # check for both json and id given
        with self.assertRaises(BuildErrorException):
            test_build = self.connection.Build(json=self.json, id=3)
        # check for grabbing from empty list
        with self.assertRaises(BuildErrorException):
            test_build = self.connection.Build(id=3)
        # check for grabbing non-existant thing - note, ids are not numbers
        # but ObjectId objects so this should fail)
        self.connection.Build(json=self.json).save()
        with self.assertRaises(BuildErrorException):
            test_build = self.connection.Build(id=3)

    def test_build_retrieval(self):
        """ Tests that Build objects are correctly retrieved from the
            database given an ID (as would be used by the BuildQueue)
            checks for:
                correct Document retrieved
                valid JSON returned """
        test_build = self.connection.Build(json=self.json)
        saved_id = test_build.save()
        self.fake_json['_id'] = saved_id

        get_by_find = self.Build().find({'_id': saved_id})
        get_by_init = self.Build(id=saved_id)

        self.assertEqual(get_by_find, get_by_init) # check that they got the same thing
        # since we know they both match, we only have to check one of these
        self.assertEqual(get_by_find, json.dump(self.jake_json))

    def test_multiple_build_retrieval(self):
        """ Tests that retrieving multiple builds works correctly """
        # should not be smart enough to tell that matching json is the same build,
        # so we can populate the database with multiple copies of the same build :P
        test_build1_id = self.connection.Build(json=self.json).save()
        test_build2_id = self.connection.Build(json=self.json).save()
        self.connection.Build(json=self.json).save()
        self.connection.Build(json=self.json).save()
        self.connection.Build(json=self.json).save()
        self.connection.Build(json=self.json).save()
        self.connection.Build(json=self.json).save()
        self.connection.Build(json=self.json).save()
        self.connection.Build(json=self.json).save()

        # test that we get the right ones
        get_build1 = self.Build(id=test_build1_id)
        get_build2 = self.Build(id=test_build2_id)
        self.assertNotEqual(get_build1['_id'], get_build2['_id'])
        self.assertEqual(get_build1['_id'], test_build1_id)
        self.assertEqual(get_build2['_id'], test_build2_id)

    def test_update_existing_build(self):
        """ Tests that updating a build with build results works correctly
            checks for:
                correct retrieval of guild
                correct update """
        test_build = self.connection.Build(json=self.json)
        test_build_id = test_build.save()

        error_msg = "an error message here"
        test_build.update_with_results(error_msg)
        check = self.connection.Build(id=test_build_id)
        assertEqual(check['error'],error_msg)


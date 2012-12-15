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
from views import (
    API
)

class APITest(unittest.TestCase):
    """Test cases for API"""
    @classmethod
    def set_up_class(self):
        """ Create clean instance of DB according to test_settings file"""

    def set_up(self):
        """ Create build objects to test with"""

    def tear_down(self):
        """ Remove all objects from DB and remove it """

    def test_api_builds():
        """ Verifies that a good build builds without error """

    def test_api_builds_bad():
        """ Verifies that a bad build returns an error and posts the error to 
        GitHub """

    def test_api_builds_loop():
        """ Verifies that a bad build with an infinite loop times out after the
        hang time in test_settings """

    def test_api_pings():
        """ Verifies that it returns true when building and false when free """

    def test_api_build_status():
        """ Verifies that when a build is running, returns the status of that
        build and otherwise returns clear."""

    def test_api_build_status_wrong_id():
        """ Verifies that an error is returned if an invalid ID is passed to 
        the build_status endpoint """

    def test_api_build_statuses():
        """ Verifies that build statuses returned match initial set."""

    def test_api_accepts_settings_changes():
        """ Verifies that test_settings file is changed"""

    def test_api_denies_bad_settings():
        """ Verifies that test_settings file is not changed if settings are
        malformed or incorrect """

    def test_api_blame_list():
        """ Verifies that the data returned is the same as data stored"""

    def test_api_rebuilds():
        """ Verifies that after adding a failing test, build that passed build()
        now fails."""



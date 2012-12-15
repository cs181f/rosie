"""
Test cases for the Build class. Since the Build object
is just an extension of mongokit's Document class and
implements very little on its own, we only need the
following tests:

BLACKBOX TESTING:
    
    def test_build_creation
    def test_build_retrieval
    def test_multiple_build_retrieval
    def test_build_update

WHITEBOX TESTING:

    def test_build_from_good_json
    def test_build_from_bad_json
    def test_build_from_database
    def test_failed_build_from_database
    def test_update_existing_build
    def test_failed_update_from_database

"""

import unittest
from models import (
    Build
)


class BuildTest(unittest.TestCase):
    """Test cases for Worker Thread"""
    @classmethod
    def setUpClass(self):
        """ Nothing needs to be set up for the whole class.
            The database is set up in the Build class,
            and the connection is imbedded in the objects. """

    def setUp(self,json):
        """ Create a Build object """
        self.Build = Build(json)

    def tearDown(self):
        """ Nothing needs to be torn down """

    # BLACKBOX TESTING
    
    def test_build_creation(self):
        """ Tests that a new build is created correctly """
        
    def test_build_retrieval(self):
        """ Tests that a build is correctly retrieved """
        
    def test_multiple_build_retrieval(self):
        """ Tests that retrieving multiple builds at once
            works correctly """
    
    def test_build_update(self):
        """ Tests that updating builds works correctly """
        
    # WHITEBOX TESTING
        
    def test_build_from_good_json(self):
        """ Tests that sample JSON results in a valid Build object that is
            correctly inserted into the database 
            checks for:
                valid Document created
                inserted into database
                ID returned and correct """
    
    def test_build_from_bad_json(self):
        """ Tests that bad JSON results in a reasonable response 
            checks for: reasonable errors """
            
    def test_build_from_database(self):
        """ Tests that Build objects are correctly retrieved from the
            database given an ID (as would be used by the BuildQueue) 
            checks for:
                correct Document retrieved
                valid JSON returned """
    
    def test_failed_build_from_database(self): 
        """ Tests that bad retrieves fail reasonably
            checks for:
                reasonable error given invalid ID
                reasonable errors for database errors """

    def test_update_existing_build(self):
        """ Tests that updating a build with build results works correctly 
            checks for:
                correct retrieval of guild
                correct update """
    
    def test_failed_update_existing_build(self):
        """ Tests that updating a build incorrectly fails reasonably 
            checks for: reasonable errors """

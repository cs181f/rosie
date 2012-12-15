"""
Test cases for BuildQueue. The functionality of BuildQueue is really
just a wrapper for the Queue class, so not that much testing is necessary.
In these test cases, we just check that our wrappers worker correctly. For this
reason, we do no black box testing.

WHITEBOX TESTING:

    def test_has_builds_returns_correct_true(self):
    def test_has_builds_returns_correct_false(self):
    def test_next_build_returns_if_if_builds(self):
    def test_next_build_returns_false_if_empty(self):
    def test_add_build_adds_build(self):
    def test_can_be_accessed_from_multiple_threads(self):

BLACKBOX TESTING:

    I include no black box tests because this class is essentially a wrapper
    for the Queue class. Therefore, I only need to ensure that my wrapper
    functions correctly call the Queue functions. Since I'm using my
    understanding of the internal class, all those tests are white box tests. Therefore,
    I include no black box tests.
"""

import unittest
from models import (
    BuildQueue
)

class BuildQueueTest(unittest.TestCase):
    """Test cases for Build Queue"""
    @classmethod
    def setUpClass(self):
        """ Nothing needs to be set up for the whole class """

    def setUp(self):
        """ Create a queue and worker thread """
        self.queue = BuildQueue()

    def tearDown(self):
        """ Nothing needs to be torn down """

    def test_has_builds_returns_correct_true(self):
        """ Verifies wrapper for Queue.empty() is correct """
    def test_has_builds_returns_correct_false(self):
        """ Verifies wrapper for Queue.empty() is correct """
    def test_next_build_returns_if_if_builds(self):
        """ Verifies wrapper for Queue.get() is correct """
    def test_next_build_returns_false_if_empty(self):
        """ Verifies wrapper for Queue.get() is correct """
    def test_add_build_adds_build(self):
        """ Verifies wrapper for Queue.push() is correct """
    def test_can_be_accessed_from_multiple_threads(self):
        """ Verifies that the Queue can be accessed and updated
        from multiple threads (ApplicationServer, WorkerThread for example)

        This tests that the BuildQueue can be accessed from both the Application Server
        and the BuildQueue; although, we will test it by creating two
        Threads and updating/modifying a BuildQueue in both of them and checking
        that the state of the BuildQueue is correct after both Threads are terminated
    .
        """


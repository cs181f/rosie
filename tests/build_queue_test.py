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

    def test_has_builds_returns_correct_true(self, Build):
        """ Verifies wrapper for Queue.empty() is correct """
        self.queue.add_build(Build())
        self.queue.add_build(Build())
        self.assertTrue(self.queue.has_builds())

    def test_has_builds_returns_correct_false(self, Build):
        """ Verifies wrapper for Queue.empty() is correct """
        self.assertFalse(self.queue.has_builds())

    def test_next_build_returns_build_id_if_builds(self, Build):
        """ Verifies wrapper for Queue.get() is correct """
        build = Build()
        build._id = 2
        self.queue.add_build(build)
        self.assertEqual(2, self.queue.next_build())

    def test_next_build_raises_exception_if_empty(self, Build):
        """ Verifies wrapper for Queue.get() is correct """
        with self.assertRaises(Queue.Empty):
            self.queue.next_build()

    def test_add_build_adds_build(self, Build):
        """ Verifies wrapper for Queue.push() is correct """
        self.assertFalse(self.queue.has_builds())
        build = Build()
        build._id = 1
        self.queue.add_build(build)
        self.assertTrue(self.queue.has_builds())
        self.assertEqual(1, self.queue.next_build())

    def test_can_be_accessed_from_multiple_threads(self):
        """ Verifies that the Queue can be accessed and updated
        from multiple threads (ApplicationServer, WorkerThread for example)

        This tests that the BuildQueue can be accessed from both the Application Server
        and the BuildQueue; although, we will test it by creating two
        Threads and updating/modifying a BuildQueue in both of them and checking
        that the state of the BuildQueue is correct after both Threads are terminated
    .
        """
    class TestThread(threading.Thread):
            def __init__(self, queue, elements):
                self.queue = queue
                self.elements = elements
                threading.Thread.__init__(self)

            def run(self):
                for el in self.elements:
                    build = Build()
                    build._id = el
                    self.queue.add_build(build)

    lements = range(10)
        thread_1 = TestThread(self.queue, elements[:5])
        thread_2 = TestThread(self.queue, elements[5:])

        thread_1.start()
        thread_2.start()
        thread_1.join()
        thread_2.join()

        while self.queue.has_builds():
            build_id = self.queue.next_build()
            self.assertTrue(elements.count(build_id) == 1)
            elements.remove(build_id)


"""
Test cases for the WorkerThread class. In these test cases, we verify that the
WorkerThread correctly builds, saves results, and updates Github with the correct results.
WHITEBOX TESTING:

    def test_worker_runs_in_seperate_thread(self):
    def test_init_saves_queue(self):
    def test_worker_reads_first_id_if_queue_not_empty(self):
    def test_configs_are_accurately_read(self):
    def test_build_can_be_retrieved(self):

BLACKBOX TESTING:

    def test_build_returns_error_result_if_fail(self):
    def test_build_returns_success_result_if_pass(self):
    def test_build_sent_to_github_if_fail(self):
    def test_build_not_sent_to_github_if_success(self):
    def test_build_can_be_saved_if_success(self):
    def test_build_can_be_saved_if_fail(self):

"""

# Library to enable mocking of classes
from mock import patch, MagicMock, Mock

import unittest
import json
import threading
import subprocess, os
from rosie.models import (
    WorkerThread,
    BuildQueue,
    Build
)
from datetime import datetime

class WorkerThreadTest(unittest.TestCase):
    """Test cases for Worker Thread"""
    @classmethod
    def setUpClass(self):
        """ Nothing needs to be set up for the whole class """

    def setUp(self):
        """ Create a queue and worker thread """
        self.queue = BuildQueue()
        self.thread = WorkerThread(self.queue)

    def tearDown(self):
        """ Nothing needs to be torn down """

    def test_init_saves_queue(self):
        """ Verifies that WorkerThread saves BuildQueue from constructor """
        self.assertEqual(self.thread.queue, self.queue)

    def test_worker_stops_if_queue_empty(self):
        """ Verifies that WorkerThread shuts down if BuildQueue is empty """
        self.thread.start()
        self.thread.join()

    @patch('rosie.models.Build')
    def test_worker_reads_first_id_if_queue_not_empty(self, Build):
        """ Verifies that WorkerThread gets first ID on BuildQueue
        if it is not empty """

        build = Build()
        build._id = 1

        with patch.object(WorkerThread, '_retrieve_build') as mock1:
            mock1.return_value = build
            self.thread = WorkerThread(self.queue)
            self.queue.add_build(build)

            self.thread.start()
            self.thread.join()

        self.assertEqual(self.thread.current_build, build)

    def test_build_can_be_retrieved_success(self):
        """ Verifies that WorkerThread can retrieve Build from Mongo with ID

        SETUP:
            Connect to MongoDB
            Store Build
        """
    def test_build_retrieved_fails_well(self):
        """ Verifies that WorkerThread provides appropriate exception when
        no such Build exists in MongoDB.

        SETUP:
            Connect to MongoDB
        """
    def test_build_returns_error_result_if_fail(self):
        """ Verifies that WorkerThread.build returns a valid error result if
        the build failed
        """
    def test_build_returns_success_result_if_pass(self):
        """ Verifies that WorkerThread.build returns a valid success result if
            the build succeeded
        """
    def test_build_can_be_saved_if_success(self):
        """ Verifies that correct Build is updated in MongoDB on successful build.

        SETUP:
            Connect to MongoDB
            Store Build
        """
    def test_build_can_be_saved_if_fail(self):
        """ Verifies that correct Build is updated in MongoDB on failing build.

        SETUP:
            Connect to MongoDB
            Store Build
        """
    def test_build_sent_to_github_if_fail(self):
        """ Verifies that build failure information is sent to Github as a new
        issue
        """
    def test_build_not_sent_to_github_if_success(self):
        """ Verifies that nothing is sent to Github of build passes.
        """

    def test_builds_builds_in_correct_order(self):
        """ Verifies that when multiple builds are in the BuildQueue, they
        are built in the correct order

        SETUP:
            Connect to MongoDB
            Store multiple builds
            Push builds IDs into BuildQueue
        """



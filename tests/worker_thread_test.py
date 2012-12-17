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
import requests
from rosie.models import (
    WorkerThread,
    BuildQueue,
    Build,
    BuildNotFoundException
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
        build['_id'] = 1

        with patch.object(WorkerThread, '_retrieve_build') as mock1:
            mock1.return_value = build
            self.thread = WorkerThread(self.queue)
            self.queue.add_build(build)

            self.thread.start()
            self.thread.join()

        self.assertEqual(self.thread.current_build, None)

    def test_build_can_be_retrieved_success(self):
        """ Verifies that WorkerThread can retrieve Build from Mongo with ID

        SETUP:
            Mock Build.find_one method
        """

        with patch.object(Build, 'find_one') as mock_method:
            build = Build()
            build['_id'] = 1
            mock_method.return_value = build

            self.queue.add_build(build)

            self.assertEqual(self.thread._retrieve_build(1), build)
            mock_method.assert_called_once_with(dict(_id=1))

    def test_build_retrieved_fails_well(self):
        """ Verifies that WorkerThread provides appropriate exception when
        no such Build exists in MongoDB.

        SETUP:
            Connect to Build.find_one method
        """

        with patch.object(Build, 'find_one') as mock_method:
            mock_method.return_value = None

            with self.assertRaises(BuildNotFoundException):
                self.thread._retrieve_build(1)

        mock_method.assert_called_once_with(dict(_id=1))

    @patch('rosie.models.Build')
    def test_build_returns_error_result_if_fail(self, Build):
        """ Verifies that WorkerThread.build returns a valid error result if
        the build failed
        """
        with patch.object(WorkerThread, '_bash_build') as mock_method:
            build = Build()
            self.thread = WorkerThread(self.queue)

            mock_method.return_value = "There was an error processing your result."

            result = self.thread._build(build)
            self.assertEqual(result, dict(success=False, error=mock_method.return_value))

    def test_build_returns_success_result_if_pass(self):
        """ Verifies that WorkerThread.build returns a valid success result if
            the build succeeded
        """
        with patch.object(WorkerThread, '_bash_build') as mock_method:
            build = Build()
            self.thread = WorkerThread(self.queue)

            mock_method.return_value = True

            result = self.thread._build(build)
            self.assertEqual(result, dict(success=True))

    def test_build_can_be_saved_if_success(self):
        """ Verifies that correct Build is updated in MongoDB on successful build.

        SETUP:
            Mock save on Build
        """

        with patch.object(Build, 'save') as save:
            save.return_value = True
            build = Build()
            build['_id'] = 1

            with patch.object(WorkerThread, '_retrieve_build') as mock1:
                mock1.return_value = build

                with patch.object(WorkerThread, '_bash_build') as mock2:
                    self.thread = WorkerThread(self.queue)
                    self.queue.add_build(build)
                    mock2.return_value = True

                    self.thread.start()
                    self.thread.join()

                    build.save.assert_called_once()
                    self.assertEqual(build.status, 1)

    def test_build_can_be_saved_if_fail(self):
        """ Verifies that correct Build is updated in MongoDB on failing build.

        SETUP:
            Mock save on Build
        """
        with patch.object(Build, 'save') as save:
            save.return_value = True
            build = Build()
            build['_id'] = 1

            with patch.object(WorkerThread, '_retrieve_build') as mock1:
                mock1.return_value = build

                with patch.object(WorkerThread, '_bash_build') as mock2:
                    self.thread = WorkerThread(self.queue)
                    self.queue.add_build(build)
                    mock2.return_value = "There was an error building your build"

                    self.thread.start()
                    self.thread.join()

                    build.save.assert_called_once()
                    self.assertEqual(build.status, 2)
                    self.assertEqual(build.error, mock2.return_value)

    def test_build_sent_to_github_if_fail(self):
        """ Verifies that build failure information is sent to Github as a new
        issue
        """
        with patch.object(Build, 'save') as save:
            save.return_value = True
            build = Build()
            build['_id'] = 1

            with patch.object(WorkerThread, '_retrieve_build') as mock1:
                mock1.return_value = build

                with patch.object(WorkerThread, '_bash_build') as mock2:
                    mock2.return_value = "There was an error processing your build."

                    with patch.object(WorkerThread, '_post_to_github') as mock3:
                        mock3.return_value = True
                        self.thread = WorkerThread(self.queue)
                        self.queue.add_build(build)

                        self.thread.start()
                        self.thread.join()

                        self.thread._post_to_github.assert_called_once_with(build)

    def test_build_not_sent_to_github_if_success(self):
        """ Verifies that nothing is sent to Github of build passes.
        """
        with patch.object(Build, 'save') as save:
            save.return_value = True
            build = Build()
            build['_id'] = 1

            with patch.object(WorkerThread, '_retrieve_build') as mock1:
                mock1.return_value = build

                with patch.object(WorkerThread, '_bash_build') as mock2:
                    mock2.return_value = True

                    with patch.object(WorkerThread, '_post_to_github') as mock3:
                        mock3.return_value = True
                        self.thread = WorkerThread(self.queue)
                        self.queue.add_build(build)

                        self.thread.start()
                        self.thread.join()

                        self.thread._post_to_github.assert_not_called()

    def test_builds_builds_in_correct_order(self):
        """ Verifies that when multiple builds are in the BuildQueue, they
        are built in the correct order

        SETUP:
            Mock multiple builds
        """
        with patch.object(Build, 'save') as save:
            save.return_value = True
            builds = []
            for i in range(5):
                build = Build()
                build['_id'] = i
                builds.append(build)

            with patch.object(WorkerThread, '_retrieve_build') as mock1:
                def side_effect(key):
                    return builds[key]

                mock1.side_effect = side_effect

                with patch.object(WorkerThread, '_bash_build') as mock2:
                    mock2.return_value = True

                    with patch.object(WorkerThread, '_post_to_github') as mock3:
                        mock3.return_value = True
                        self.thread = WorkerThread(self.queue)

                        for b in builds:
                            self.queue.add_build(b)

                        self.thread.start()
                        self.thread.join()

                        for i in range(4):
                            self.assertTrue(builds[i].build_time < builds[i+1].build_time)

    def test_post_to_github_posts_to_correct_url(self):
        configs = dict(GITHUB_ID='github_id', GITHUB_SECRET='github_secret')

        build = Build()
        build.error = "error string"
        build.ref = 'build_ref'

        build.repository.name = 'test_repo'
        build.repository.owner.name = 'jesse'

        self.thread = WorkerThread(self.queue, configs)

        with patch.object(requests, 'post') as mock:
            mock.return_value = True

            self.assertTrue(self.thread._post_to_github(build))

        expected_url = 'https://api.github.com/repos/jesse/test_repo/issues?client_id=github_id&client_secret=github_secret'
        expected_data = {'body': 'error string', 'title': 'Build failure on ref build_ref'}
        mock.assert_called_once_with(expected_url, expected_data)

    def test_post_to_github_without_credentials_returns_false(self):
        configs = dict()

        build = Build()
        build.error = "error string"
        build.ref = 'build_ref'

        build.repository.name = 'test_repo'
        build.repository.owner.name = 'jesse'

        self.thread = WorkerThread(self.queue, configs)

        with patch.object(requests, 'post') as mock:
            mock.return_value = True

            self.assertFalse(self.thread._post_to_github(build))

        mock.assert_not_called()
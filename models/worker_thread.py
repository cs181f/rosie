"""
The WorkerThread class builds Build objects that are in the BuildQueue
asynchronously to the Application Server.

The only data structure used in this class is the BuildQueue class, which
we design in the build_queue.py file.

The basic logic for a WorkerThread is as follows. There is only ever 1 WorkerThread
running at a time. When a new build comes in, the Application Server checks if a
WorkerThread is already running. If it is, the Application Server simply saves the
Build in the database and pushes the Build.id onto the queue. If a WorkerThread is not running,
the Application Server starts a new one with the following code:

    WorkerThread(queue)
    WorkerThread.run()

This WorkerThread will in a seperate thread from the Application Server and
wil automatically terminate when it has finished building all of the builds
in the BuildQueue (i.e. the BuildQueue is empty).

DATABASE CONNECTION:

    The only way the WorkerThread interacts with the database is through the
    Build object. Thus, there is no need to actively maintain another connection
    to the database.

CONFIGURATION:

    Configuration for the WorkerThread is stored in a configuration file
    that is read on startup into the Application Server. The Application Server
    then passes this configuration information to the Worker Thread on initialization.
"""

# Library requirements for the WorkerThread

"""
The threading module is used to enable the WorkerThread to run in
a seperate thread from the Application Server. The WorkerThread
subclasses the threading.Thread class. Documentation can be found at:

http://docs.python.org/2/library/threading.html
"""
import threading

"""
The requests module is used to communicate with the Github API after the build
is done. Documentation for it can be found at:

http://docs.python-requests.org/en/latest/

This module only uses:

    requests.get()
    requests.post()
"""
import requests
from build import connection
from datetime import datetime


class BuildNotFoundException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# WorkerThread inherits from the Python stdlib threading.Thread class.
class WorkerThread(threading.Thread):
    """PUBLIC: Constructor for WorkerThread class

        @param queue is the BuildQueue that contains the Builds to be built
        @param configs is the configuration for the Rosie server
    """
    def __init__(self, queue, configs=dict(), connection=connection):
        # calls standard Thread constructor
        threading.Thread.__init__(self)

        # PRIVATE VARIABLES
        # stores BuildQueue in private variable
        self.configs = configs
        self.queue = queue
        self.github_link = configs.get('github_link', '')
        self.current_build = None
        self.connection = connection
        self.building = False

    def run(self):
        """ PUBLIC: Starts worker in new Thread """
        self.building = True
        while self.queue.has_builds():
            self.current_build = self._retrieve_build(self.queue.next_build())
            result = self._build(self.current_build)
            if result['success']:
                self.current_build['status'] = 1
                self.current_build.save()
            else:
                self.current_build['status'] = 2
                self.current_build['error'] = result['error']
                self.current_build.save()
                self._post_to_github(self.current_build)

        self.current_build = None
        self.building = False

    def is_building(self):
        return self.building

    def _retrieve_build(self, id):
        """ PRIVATE: Retrieves build given build.ID

            @param id is the integer Build.id of the build to be retrieved

            returns a Build object with Build.id == id
        """
        build = self.connection.Build.find_one(dict(_id=id))
        if build is None: raise BuildNotFoundException("Build was not in database.")
        return build

    def _build(self, build):
        """ PRIVATE: wrapper for bash build """
        result = self._bash_build(build)
        build['build_time'] = datetime.now()
        if type(result) == str:
            return dict(success=False, error=result)
        else:
            return dict(success=True)

    def _bash_build(self, build):
        """ PRIVATE: Builds build in bash

        When we 'build' a build, there are three primary steps, all of which we
        'bash out' for, which essentially means we run arbitrary code in the shell
        of the server Rosie is installed:

            1. Run the custom pre-build hook, which is just bash code that
            the user can specify.

            2. Run the test command, which can be any number of different commands,
            such as:

                rake test
                nosetests
                java -cp /usr/share/java/junit.jar org.junit.runner.JUnitCore [test class name]

            3. Run the custom post-build hook, which is just bash code the user
            can specify.

        The obvious concern here is the security risks of running arbitrary code on the
        server. The key point to understand here is that the user is also the owner
        and maintainer of the server Rosie is installed on, so they can do whatever
        they want.

        @param build is the Build object to be built

        returns build results
        """
        return True
        # The original plan was to implement this functionality, but in the end it
        # was too much to do. It would involve 200+ more lines of code (judging from other
        # build functionality in open source CI server), so I just mocked this out as
        # always returning true.
        #
        # I also implemented the BuildQueue, so I think this should be OK.

    def _post_to_github(self, build):
        """ PRIVATE: posts build results to Github

        This method will primarily be using the request module to communicate
        with the Github API.

        @param results is the results information returned by the build method

        returns True if Github is correctly updated, False otherwise
        """

        github_id = self.configs.get('GITHUB_ID', None)
        github_secret = self.configs.get('GITHUB_SECRET', None)

        if not github_id or not github_secret:
            return False

        base_url = "https://api.github.com/repos/%s/%s/issues" % (build.repository.owner.name, build.repository.name)
        auth_string = "?client_id=%s&client_secret=%s" % (github_id, github_secret)
        url = base_url + auth_string

        title = "Build failure on ref %s" % build.ref
        body = build['error']
        data = dict(title=title, body=body)
        return requests.post(url, data)


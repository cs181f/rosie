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
from build import Build

# WorkerThread inherits from the Python stdlib threading.Thread class.
class WorkerThread(threading.Thread()):
    """PUBLIC: Constructor for WorkerThread class

        @param queue is the BuildQueue that contains the Builds to be built
        @param configs is the configuration for the Rosie server
    """
    def __init__(self, queue, configs):
        # calls standard Thread constructor
        threading.Thread.__init__(self)

        # PRIVATE VARIABLES
        # stores BuildQueue in private variable
        self.configs = configs
        self.queue = queue
        self.github_link = configs.github_link
        self.current_build = None

    def run(self):
        """ PUBLIC: Starts worker in new Thread """

    def retrieve_build(id):
        """ PRIVATE: Retrieves build given build.ID

            @param id is the integer Build.id of the build to be retrieved

            returns a Build object with Build.id == id
        """

    def build(build):
        """ PRIVATE: Builds build

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

    def save_build_results(results):
        """ PRIVATE: stores build results in MongoDB

        This method will be easily enabled by the Build object.

        @param results is the results information returned by the build method

        returns True if information is correctly saved, False otherwise
        """

    def post_to_github(results):
        """ PRIVATE: posts build results to Github

        This method will primarily be using the request module to communicate
        with the Github API.

        @param results is the results information returned by the build method

        returns True if Github is correctly updated, False otherwise
        """
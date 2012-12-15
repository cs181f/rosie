"""
The BuildQueue class is the in memory queue that WorkerThreads pull
Builds that need to be built from.

It inherits from the standard Python multithreaded Queue. The BuildQueue
must be multithreaded so that both the Application Server and WorkerThread
can access it, even though they are in seperate threads. All threading abilities
are mediated by the Queue class, which it inherits from. Documentation for the
Queue class can be found at:

http://docs.python.org/2/library/queue.html
"""

# Python stdlib requirements for Queue
import Queue
import datetime

# BuildQueue inherits from standard multithreaded Python Queue
class BuildQueue(Queue):

    """ Constructor for BuildQueue. Takes no arguments.
    """
    def __init__(self):
        # calls standard Queue constructor
        Queue.__init__(self)

    """ PUBLIC: Check whether there are any builds in the queue """
    def has_builds(self):
        # return True or False

    """ PUBLIC: Dequeue Build.id of next build.

    The Build.id of the next build is *removed* from the BuildQueue
    when this is called.
    """
    def next_build(self):
        # returns Build ID of next Build in the queue

    """ PUBLIC: Add a build to the BuildQueue. Accepts a Build object
        but only stores the Build.id in the BuildQueue.

        @param build is the Build object to be added to the BuildQueue
    """
    def add_build(self, build):
        # returns boolean of whether build was successfully added
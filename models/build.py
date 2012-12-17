""" Build Objects
Using the mongokit to control schema and simplify operations
Essentially a nice wrapper to make things as easy as possible
http://namlook.github.com/mongokit/index.html
"""

from mongokit import Document, Connection, IS

class BuildErrorException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# sets up the connection to the database.
connection = Connection()

# creates a schema that will be enforced by mongokit
# MongoKit uses unicode: http://api.mongodb.org/python/current/tutorial.html#a-note-on-unicode-strings
# This is for compliance with the BSON format that it stores data in.
# As a result, all strings will say unicode instead of string.
# We do not need to worry about any of this; MongoKit will handle
# any string to unicode conversions necessary.
@connection.register    # assigns the schema to the database
class Build(Document):
    __collection__ = 'builds'   # database structure
    __database__ = 'rosie'       # database structure

    use_dot_notation = True
    dot_notation_warning = True
    structure = {
        'repository': {
            'url': unicode,     # url to the github repository
            'name': unicode,    # repository name
            'description': unicode,
            'owner': {
                'name': unicode,
                'email': unicode
            }
        },                      # description from github
        'url': unicode,         # url to specific commit
        'author': {             # author of commit
            'email': unicode,   # author's email
            'name': unicode
        },  # author's name
        'message': unicode,     # the commit message describing changes made
        'timestamp': unicode,   # time committed
        'ref': unicode,         # branch information
        'status': IS(0,1,2),    # 0 = processing, 1 = successful, 2 = failed
        'error': unicode        # information about any build errors (optional)
    }

    # these fields will be enforced by mongokit.
    # When self.validate() is called, mongokit checks that these
    #    fields exist and contain legal data.
    required_fields = [
        'repository.url',
        'repository.name',
        'repository.description',
        'url',
        'author.email',
        'author.name',
        'message',
        'timestamp',
        'ref',
        'status',
    ]


    # The following two methods are documented here:
    #    http://namlook.github.com/mongokit/json.html
    """
    self.to_json()
        provided by MongoKit
        returns a json version of the database object
    """

    """
    self.from_json(json)
        provided by MongoKit
        fills a database object with the provided json object
    """

    # uses initializer inherited from Document class

    def create_new_build(self, json):
        self.from_json(json) # provided by mongokit
	self.validate()      # provided by mongokit

    # load
    def load_from_database(self, id):
	""" takes in an id and fills the build document with it """
	if not isinstance(id, ObjectId):
	    raise BuildErrorException("Not a valid ID")
        matches = self.find({'_id': id})
	if matches.count() == 1:
	    self = matches[0]
	elif matches.count() == 0:
	    raise BuildErrorException("Found no matching documents.")
        else:
	    raise BuildErrorException("Found multiple matching documents.")

    # save
    def save(self, *args, **kwargs):
        """ Stores an object in the database.
            Returns the ID to store in the build queue

            While MongoKit contains a save() method, we are
            bypassing it in favor of the PyMongo version in order
            to obtain the internal ID number, which we will use
            in the build queue.
        """
        # calls self.validate()
        self.validate()

        # this is the PyMongo save method:
        return self.collection.save(self, *args, **kwargs)

    # update_with_results
    def update_with_results(self, newstatus, errmsg=None):
	self['status'] = newstatus
	if newstatus == 2: # if the build failed
	    self['error'] = errmsg
	self.save()        # handles validation

    # The following methods are documented here:
    #    http://namlook.github.com/mongokit/query.html

    """
    self.find({'_id': number})
        provided by MongoKit
        finds the build by ID number
    """

    """
    self.find() # with no arguments
        provided by MongoKit
        returns a cursor that will iterate through all of the builds
    """

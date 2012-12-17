"""
This module exposes all of the endpoints of the application programming
interface which will be hit by the external parts of Rosie. This includes
GitHub's Webhooks, the web frontend, and the command line interface.

Each API route is either returning accessible information or saving it and
triggering events, so the complexity of each method is fairly low.
"""

from flask import Flask
from flask import jsonify #translates a dictionary into JSON
                          #(http://flask.pocoo.org/docs/api/)
from flask import (
    json, #parses JSON
    request
)

from models import (
    BuildQueue,
    Build,
    WorkerThread,
    connection
)

from datetime import datetime
from mongokit import ObjectId

api = Flask(__name__)
api.config.from_object('config')

api.worker = None
api.queue = BuildQueue()

Build = connection.Build
###GitHub Webhook###
@api.route('/build', methods=['POST'])
def build():
    """
    The @api.route decorator is a flask function that
    triggers the method when that url is visited, with
    access given to the paramaters passed in the URL.
    http://flask.pocoo.org/docs/api/#api
    """
    #creates Build object and stores it in the database by calling the public
    #constructor
    payload = request.json.get('payload', None)

    if not payload:
        return jsonify(success=False)

    build = connection.Build(payload)
    build['status'] = 0
    build['error'] = ''
    build['build_time'] = datetime.utcnow()
    build.save()

    #stores the build_id in the build queue
    api.queue.add_build(build)

    if (api.worker is None or api.worker.current_build is None):
        api.worker = WorkerThread(api.queue, api.config, connection)
        api.worker.start()
        api.worker.join()

    return jsonify(success=True, id=str(build['_id']))

###HTML Endpoints###

@api.route('/ping', methods=['GET'])
def ping():
    #checks whether the worker is processing a build or free
    if api.worker is None or not api.worker.is_building():
        return jsonify(dict(building=False))
    else:
        return jsonify(dict(building=True, build=api.worker.current_build))
    #returns jsonify(status of server)

@api.route('/builds/<build_id>', methods=['GET'])
def get_build(build_id):
    #looks up the build by its id in the database
    #the variable build_id is passed in the url

    try:
        build = Build.get_from_id(ObjectId(build_id))
    except Exception:
        return jsonify(error="Invalid Build ID")

    if build is None:
        return jsonify(error="Invalid Build ID")

    #looks at the status of the build
    #returns jsonify(status of build)
    return (build.to_json(), 200)

@api.route('/builds', methods=['GET'])
def get_builds():
    #gets all builds in DB using .find() method
    builds = []
    for build in Build.find():
        builds.append(build.to_json())

    #returns data for all builds
    return json.dumps(builds), 200

@api.route('/check_settings', methods=['GET'])
def get_settings():
    return jsonify(api.config)
    #returns the contents of the settings file
    #this is to populate the web interface and
    #to provide information at the command line

@api.route('/blame', methods=['GET'])
def blame():
    bad_people = dict()
    for build in Build.find():
        if build.status == 2:
            if bad_people.get(build.author.name, None) is None:
                bad_people[build.author.name] = 1
            else:
                bad_people[build.author.name] += 1

    return jsonify(bad_people)

@api.route('/builds/new', methods=['POST'])
def rebuild():
    #takes build ID as parameter
    id = request.form.get('build_id', None)

    try:
        build = Build.get_from_id(ObjectId(id))
    except Exception:
        return jsonify(error="Invalid Build ID")

    if build is None:
        return jsonify(error="Invalid Build ID")
    #looks up a build by that ID
    #rebuilds build to see if it fails new tests
    api.queue.add_build(build)

    if (api.worker is None or api.worker.current_build is None):
        api.worker = WorkerThread(api.queue, api.config, connection)
        api.worker.start()

    return jsonify(success=True, id=id)

if __name__ == '__main__':
    api.run()

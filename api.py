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
from flask import json #parses JSON                          
from models import (
    BuildQueue,
    Build,
    WorkerThread
)

api = Flask(__name__)
api.config.from_object('config')

worker = None
queue = BuildQueue()

###GitHub Webhook###

@api.route('/build', methods=['POST']) 
                     #The @api.route decorator is a flask function that 
                     #triggers the method when that url is visited, with
                     #access given to the paramaters passed in the URL.
                     # http://flask.pocoo.org/docs/api/#api
def build():  
    #creates Build object and stores it in the database by calling the public
    #constructor
    build_id = Build(request.form['payload'])
    
    #stores the build_id in the build queue
    queue.add_build(build_id)
    configs = app.open_resource('')
    if (worker is None or worker.current_build is None):
        worker = Worker(queue, api.config)
        worker.start()

###HTML Endpoints###

@api.route('/ping', methods=['GET'])
def ping():
    #checks whether the worker is processing a build or free
    if (worker is None or worker.current_build is None):
        return jsonify(dict(building=False))
    else:
        return jsonify(dict(building=True, build=worker.current_build))
    #returns jsonify(status of server)

@api.route('/builds/<build_id>', methods=['POST'])
def get_build(build_id):
    #looks up the build by its id in the database
    #the variable build_id is passed in the url 
    build = Build.find_one(dict(_id=build_id))

    #looks at the status of the build
    #returns jsonify(status of build)
    return jsonify(build.to_json)

@api.route('/builds', methods=['POST'])
def get_builds():
    #gets all builds in DB using .find() method
    builds = []
    for build in Build.find():
        builds.append(build)

    #returns data for all builds
    return jsonify(builds)

@api.route('/check_settings', methods=['GET'])
def get_settings():
    return jsonify(api.config)
    #returns the contents of the settings file
    #this is to populate the web interface and
    #to provide information at the command line

@api.route('/blame', methods=['POST'])
def blame():
    bad_people = dict(0)
    for build in Build.find():
        if build.error is not None:
            bad_people[build.author.name] += 1

    return jsonify(bad_people)

@api.route('/builds/new', methods=['POST'])
def rebuild():
    #takes build ID as parameter
    id = request.form['build_id']
    #looks up a build by that ID
    #rebuilds build to see if it fails new tests
    queue.add_build(build_id)
    configs = app.open_resource('')
    if (worker is None or worker.current_build is None):
        worker = Worker(queue, api.config)
        worker.start()

if __name__ == '__main__':
    api.run()

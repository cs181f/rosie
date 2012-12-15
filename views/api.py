"""
This module exposes all of the endpoints of the application programming 
interface which will be hit by the external parts of Rosie. This includes
GitHub's Webhooks, the web frontend, and the command line interface.

Each API route is either returning accessible information or saving it and
triggering events, so the complexity of each method is fairly low.
"""
from flask import jsonify #translates a dictionary into JSON 
                          #(http://flask.pocoo.org/docs/api/)
from build import Build

###GitHub Webhook###

@api.route('/build', methods=['POST']) 
                     #The @api.route decorator is a flask function that 
                     #triggers the method when that url is visited, with
                     #access given to the paramaters passed in the URL.
                     # http://flask.pocoo.org/docs/api/#api
def build():
    #parses Github Webhooks data into JSON of bild
    #creates Build object and stores it in the database by calling the public
    #fill method

###HTML Endpoints###

@api.route('/ping', methods=['POST'])
def ping():
    #checks whether the worker is processing a build or free
    #returns jsonify(status of server)

@api.route('/builds/<build_id>', methods=['POST'])
def get_build():
    #looks up the build by its id in the database
    #the variable build_id is passed in the url 
    #looks at the status of the build
    #returns jsonify(status of build)

@api.route('/builds', methods=['POST'])
def get_builds():
    #gets all builds in DB using .find() method
    #returns data for all builds

@api.route('/settings', methods=['POST'])
def settings():
    #accepts settings changes 
    #modifies config file with appropriate changes

@api.route('/check_settings', methods=['GET'])
def get_settings():
    #returns the contents of the settings file
    #this is to populate the web interface and
    #to provide information at the command line

@api.route('/blame', methods=['POST'])
def blame():
    #This endpoint returns that list sorted with the highest number of broken
    #commits first.

@api.route('/builds/new', methods=['POST'])
def rebuild():
    #takes build ID as parameter
    #looks up a build by that ID
    #rebuilds build to see if it fails new tests

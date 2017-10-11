'''
Created on Oct 10, 2017

In order to run this service, 2 ini files are required:
 - local_svc.ini - contains cofig properties for this service. 
                   This currently includes:
                      - HOST - host of the service
                      - PORT - port on which it will listen
                      - USERNAME - see comments below
                      - PASSWORD - see comments below
                      
 - 3rd_party_svc.ini - contains definition of all the Geolocation
        services to be used by this webservice. 
        
        There is no limit to the number of 3rd party services used. 
        No service is hardcoded. Each service must have required set of config 
        properties and the resulting Json messages are dynamically parsed.        
        This enables addition/removal of 3rd party services without 
        making any codechanges, just a config change.
         
        The order of the service definition in the ini file is the 
        order of execution of those services - the fallback. To change
        the order of execution, just change the order of the service 
        specification in the ini file.
        
        If the 3rd party svc call succeeds in converting the adddress,
        the results of this service call will contain the lat/lon as well 
        as the name of the 3rd party service that provided the data. It
        does not contain information why (if any) of previous service calls 
        did not return the data. If no service/data is available, an error 
        message is returned.
         
        For exact field description and additional information, see 
        comments in the 3rd_party_svc.ini file.

************************************************************************************   

REST webservice calls that are supported are defined in this file.

Only GET is currently supported since we are only converting address to lat/lon. 
POST, PUT, DELETE, PATCH calls are not supported and return code 405.
See each call for more details.

Host and port and port can be specified in the local_svc.ini file. This
was intentionally put in a file instead of command line. One can imagine
multiple different files depending on environment (DEV, QA, PROD) having
different hosts and ports. In addition, what is more important, the PROD
configuration MUST reside in a repository (CVS, SVN, GIT, etc) and not
be changeable by hand without oversight.

A simple authentication layer was added to the GET call. In real world,
authentication would use a real auth service, however for the purposes of
this exercise, the username and possword are stored in the ini file (local_svc_props.ini)
401 error is returned when authentication fails. 

************************************************************************************

URI Structure: 
   /TYPE_OF_CALL/API_TYPE/VERSION/MSG_FORMAT
   /api/geocode/v1.0/json
   
/api                   - specifies that this is an api call
/api/geocode           - allows the uri to support multiple different apis in the future, 
                         not just geocode
/api/geocode/v1.0      - allows multiple versions to run in parallel. For example for 
                         backwards compatibility. See note below.
/api/geocode/v1.0/json - specifies the format of expected input/output. If for example, XML 
                         format would later be supported, on the last part of URI would need to change.

Note: fully RESTful apis honor discovery. However for the purposes of this project
this seemed to me as a mute point. So if discovery is off the table, versioning is the
next best accepted practice.

At this point URI is hardcoded below, however proper versioning and multiple
format support is possible given the URI structure. 

************************************************************************************

Logger: currently the configuration is hardcoded in this file. In real life, I would 
to have multiple log files (one per environment: DEV, QA, PROD) that would be read and 
loaded. I did not do this for this project as I deemed it to be out of scope.

@author: Dounaa
'''

#imports
import sys
import logging
import argparse

from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
from utils.cfg_reader import CommandLineReader, ConfigParserBuilder, ConfigLoader
from utils.properties import PropertyFileLoader
from utils.json_parser import JsonPathParser
from utils.constants import SERVER_CONNECTION_INFO, HOST, PORT, USERNAME, PASSWORD, LOGIN_INFO
from websvc.third_party_websvc import ServiceRunner, GeoLocServiceBuilder, ServiceResultProcessor

URI = "/api/geocode/v1.0/json"

'''
Below variables ideally should be defined by Spring (or similar framework). 
This is a poor-man's version. Currently it is here because it's used for 
dependency injection. 
'''
app = Flask(__name__)
auth = HTTPBasicAuth()
cmd_reader = CommandLineReader(argparse.ArgumentParser())
svc_runner = ServiceRunner(GeoLocServiceBuilder(), ServiceResultProcessor(JsonPathParser()))
config_loader = ConfigLoader(PropertyFileLoader(),  ConfigParserBuilder())


'''*********************************************************************************
******************************REST calls below**************************************
*********************************************************************************'''

'''
Main GET service call to convert address to lat/lon. This call is authenticated.

Parameters:
 - address - specifies the address to be looked up. 
        Note: there is currently no validation on this string, and it is passed directly to the 
        3rd party geolocation services.

Returns: json formated message.
'''
@app.route(URI, methods=['GET'])
@auth.login_required
def get_address():
    address = request.args.get('address', default = '', type = str)
    results = svc_runner.run_service(address)
    
    return jsonify({'results': results})

'''
Calls that are currently not supported. Exectuting these will retun 405.
'''
@app.route(URI, methods=['POST'])
@app.route(URI, methods=['PUT'])
@app.route(URI, methods=['DELETE'])
@app.route(URI, methods=['PATCH'])
def unsupported_action():
    return make_response(jsonify({'error': 'Requested action is not supported'}), 405 )
    
'''
404 Error handler
'''
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

'''
Authentication call. Currently retrives username/password from a 
config file. In real world, this would be a call to a real authentication
service.
'''
@auth.get_password
def get_password(username):
    login_info = config_loader.local_svc_props[LOGIN_INFO]
    
    if username == login_info[USERNAME]:
        return login_info[PASSWORD]
    
    return None

'''
Authorization error handler. Returns code 401
'''
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

'''
starts the application
'''
def start_app():
    # setup logger
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    
    # read command line arguments
    cmd_reader.read_command_line(sys.argv[1:])
    
    # load and set configs
    config_loader.load_configs(cmd_reader.local_svc_cfg_file, cmd_reader.third_pty_cfg_file)
    svc_runner.third_party_props = config_loader.third_pty_props
    
    # start the application
    server_info = config_loader.local_svc_props[SERVER_CONNECTION_INFO]
    app.run(host=server_info[HOST], port=server_info[PORT])
    
if __name__ == '__main__':
    start_app()
    
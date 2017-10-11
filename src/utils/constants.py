'''
Created on Oct 9, 2017

Contains all the constants used by the services.

@author: Dounaa
'''

'''
Constants used in the 3rd party config definition file.
'''
#3rd party service URL for the geolocation service
SERVICE_URL = 'ServiceUrl'

#the tag used to specify the serach criteria for the 3rd party service call
SEARCH_TAG = 'SearchTag'

#unique id string used for authentication by the 3rd party
ID_STRING = 'IdString'

#name of the service. This is used in output to signify which service
#returned the results
SERVICE_NAME = 'ServiceName'

#path string to the Latitude value in the result json.
LAT_JSON_PATH = 'LatitudeJsonPath'

#path string to the Longitude value in the result json.
LON_JSON_PATH = 'LongitudeJsonPath'

'''
Constants used in resulting Json messages
'''
LATITUDE = 'Latitude'
LONGITUDE = 'Longitude'

#specifies 3rd party which returned the result
SERVICE_PROVIDER = 'ServiceProvider'

'''*************************************************'''
'''
Below contains constants for web service defintion and 
authentication
'''

SERVER_CONNECTION_INFO = 'ServerConnectionInfo' #config section
PORT = 'Port'
HOST = 'Host'

LOGIN_INFO = 'LoginInfo'    #config section
USERNAME = 'Username'
PASSWORD = 'Password'

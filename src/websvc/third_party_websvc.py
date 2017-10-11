'''
Created on Oct 9, 2017

@author: Dounaa

'''

import sys
import requests

from utils.constants import ID_STRING, SERVICE_URL, SEARCH_TAG, SERVICE_PROVIDER, LAT_JSON_PATH, LON_JSON_PATH, LATITUDE, LONGITUDE,SERVICE_NAME
from utils.json_parser import JsonPathParser


class GeoLocService(object):
    '''
    Service responsible for contacting google
    '''

    def __init__(self, properties):
        '''
        Constructor
        '''
        self.__properties = properties
        
    def call_service(self, address):
        print ('Calling %s service...' %self.__properties[SERVICE_NAME])
        result = None
        
        svc_url = self.__properties[SERVICE_URL] + "?" + self.__properties[ID_STRING] + '&' + self.__properties[SEARCH_TAG]
        full_url = svc_url + address
                                 
        try:
            res = requests.get(full_url)
            result = res.json()
            print(result)
        except:
            print('Error occurred calling %s service. Error: %s' % (self.__properties[SERVICE_NAME], sys.exc_info()))
        
        return result
    

class ServiceRunner(object):
    '''
    '''
 
    @property
    def third_party_props(self):
        return self.__third_party_props
    
    @third_party_props.setter
    def third_party_props(self, value):
        self.__third_party_props = value
  
    
    def run_service(self, address):
        found = False
        result = 'No data available'
        
        for service_name, service_properties in self.__third_party_props.items(): 
            service = GeoLocService(service_properties)
            json_result = service.call_service(address.replace(" ", "+"))
            result = self.__process_service_json(json_result, service_properties)
           
            if (result != None):
                found = True
                break
            
        if (not found) :
            result = "No working geolocation services found."
            
        return result
    
      
    def __process_service_json(self, json_document, service_properties):
        result = {}
        
        lat_path = service_properties[LAT_JSON_PATH]
        lon_path = service_properties[LON_JSON_PATH]
        
        try:
            jparser = JsonPathParser()
            lat = jparser.find_value(lat_path, json_document)
            lon = jparser.find_value(lon_path, json_document)
            
            result[LATITUDE] = lat
            result[LONGITUDE] = lon
            result[SERVICE_PROVIDER] = service_properties[SERVICE_NAME]
            
            print('Service: %s, Lat: %s, Lon: %s' %(service_properties[SERVICE_NAME], lat, lon))
            
        except:
            print('Encountered Json parsing error:', sys.exc_info())
            result = None
        
        return result

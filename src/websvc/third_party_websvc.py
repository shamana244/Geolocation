'''
Created on Oct 9, 2017

This module contains classes that are responsible for connectivity, querying and
processing of 3rd party geolocation services.

GeoLocService: 
    - given a set of configuration properties, constructs a URL and issues an http 
      request to the 3rd party geolocation service.
    - result of the call is coverted to json and then returned
    - if no result is found, or an exception is caught, None is returned
 
GeoLocServiceBuilder:
    - builds GeoLocService
    - used for dependency injection

ServiceRunner: 
    Responsible for execution of multiple 3rd party services until results are
    returned or all services are attempted
    
    1. constructs (using GeoLocServiceBuilder) and calls GeoLocService
    2. processes the resulting json message using ServiceResultProcessor
    3. if no results are found or service throws an exception, moves onto the
       next 3rd party service in the list. If no additional services are available
       returns statement stating so. 

ServiceResultProcessor:
    Responsible for extraction of Lat/Lon fields from service call.
    
    - given a 3rd party service configuration, and a json document result from a service
      call to that service, uses the JsonPathParser to attempt to parse the result.
    - if parsing is successful, constructs a json message with results and the associated
      3rd party provider id.
    - if errors are encountered, returns None
    
    
@author: Dounaa

'''

import requests
import logging

from utils.constants import ID_STRING, SERVICE_URL, SEARCH_TAG, SERVICE_PROVIDER, LAT_JSON_PATH, LON_JSON_PATH, LATITUDE, LONGITUDE,SERVICE_NAME


class GeoLocService(object):
    '''
        - given a set of configuration properties, constructs a URL and issues an http 
          request to the 3rd party geolocation service.
        - result of the call is coverted to json and then returned
        - if no result is found, or an exception is caught, None is returned
    '''

    #constructor
    def __init__(self, properties):
        
        self.__properties = properties
        
    # constructs URL, sends the request and returns corresponding response as Json.
    # if no result is found, or an exception is caught, None is returned
    def call_service(self, address):
        logging.info('Calling %s service...', self.__properties[SERVICE_NAME])
        result = None
        
        #construct URL
        svc_url = self.__properties[SERVICE_URL] + "?" + self.__properties[ID_STRING] + '&' + self.__properties[SEARCH_TAG]
        full_url = svc_url + address
                      
        #issue call           
        try:
            res = requests.get(full_url)
            result = res.json()
            
            logging.debug(result)
            logging.info("...call succeeded")
        except Exception as e:
            logging.warning('Error occurred calling %s service. Error: %s', self.__properties[SERVICE_NAME], str(e))
        
        return result


class GeoLocServiceBuilder(object):
    '''
    Just constructs GeoLocService. This class exists only to help with testing via DI
    '''
    
    #build the GeoLocService using service_properties
    def build(self, service_properties):
        return GeoLocService(service_properties)


class ServiceRunner(object):
    '''
     Responsible for execution of multiple 3rd party services until results are
     returned or all services are attempted
    
     1. constructs (using GeoLocServiceBuilder) and calls GeoLocService
     2. processes the resulting json message using ServiceResultProcessor
     3. if no results are found or service throws an exception, moves onto the
        next 3rd party service in the list. If no additional services are available
        returns statement stating so. 
    '''
 
    #constructor. Takes in a GeoLocServiceBuilder and ServiceResultProcessor as arguments
    def __init__(self, geo_loc_svc_builder, service_result_processor):
        self._gls_builder = geo_loc_svc_builder
        self._processor = service_result_processor
        
    #contains the configuration for the 3rd party geolocation providers
    @property
    def third_party_props(self):
        return self._third_party_props
    
    @third_party_props.setter
    def third_party_props(self, value):
        self._third_party_props = value
  
    
    '''
     1. constructs (using GeoLocServiceBuilder) and calls GeoLocService
     2. processes the resulting json message using ServiceResultProcessor
     3. if no results are found or service throws an exception, moves onto the
        next 3rd party service in the list. If no additional services are available
        returns statement stating so. 
    '''
    def run_service(self, address):
        found = False
        result = 'No data available'
        
        for service_name, service_properties in self._third_party_props.items(): 
            #construct the service
            service = self._gls_builder.build(service_properties)
            
            #call the service 
            json_result = service.call_service(address.replace(" ", "+"))
            
            #process result json
            result = self._processor.process_service_json(json_result, service_properties)
           
            #if results are processes successfully, we are done
            if (result != None):
                found = True
                break
        
        #if no services yielded results, return corresponding message
        if (not found) :
            result = "No working geolocation services found."
            
        return result
    
class ServiceResultProcessor(object):
    '''
    Responsible for extraction of Lat/Lon fields from service call.
    
    - given a 3rd party service configuration, and a json document result from a service
      call to that service, uses the JsonPathParser to attempt to parse the result.
    - if parsing is successful, constructs a json message with results and the associated
      3rd party provider id.
    - if errors are encountered, returns None
    '''
    
    def __init__(self, json_path_parser):
        self._json_path_parser = json_path_parser
        
    #given a json document ad the service properties, extract Lat/Lon from the document
    def process_service_json(self, json_document, service_properties):
        result = {}
        
        logging.info("Parsing json document...")
        #get the expected json path
        lat_path = service_properties[LAT_JSON_PATH]
        lon_path = service_properties[LON_JSON_PATH]
        
        try:
            #extract json values given the path
            lat = self._json_path_parser.find_value(lat_path, json_document)
            lon = self._json_path_parser.find_value(lon_path, json_document)
            
            #construct results
            result[LATITUDE] = lat
            result[LONGITUDE] = lon
            result[SERVICE_PROVIDER] = service_properties[SERVICE_NAME]
            
            logging.info('Parsing succeeded: Service: %s, Lat: %s, Lon: %s', service_properties[SERVICE_NAME], lat, lon)
        
        #handle errors
        except Exception as e:
            logging.warning('Parsing failed: %s', str(e))
            result = None
        
        return result
